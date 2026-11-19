"""Recompute the dashboard and README numbers from the raw Excel file.

Run from the repo root:
    python scripts/verify_metrics.py
"""
import pandas as pd

from survey_data import HAPPINESS_AREAS, RENAME, HAPPY, SPLIT_ON, clean, load_raw


def pct(part, whole):
    return f"{part / whole * 100:.1f}%"


def main():
    raw = load_raw()
    df = clean(raw)
    n = len(df)

    print("== Data ==")
    print(f"Rows x columns: {raw.shape[0]} x {raw.shape[1]}")
    dates = pd.to_datetime(raw["Date Taken (America/New_York)"])
    print(f"Date range: {dates.min():%Y-%m-%d} to {dates.max():%Y-%m-%d}")

    print("\n== Cleaning checks ==")
    empty = [c for c in raw.columns if raw[c].isna().all()]
    print(f"Columns empty in every row ({len(empty)}): {', '.join(empty)}")
    print(f"Duplicate rows: {raw.duplicated().sum()}")
    print(f"Duplicate respondent IDs: {raw['Unique ID'].duplicated().sum()}")
    original = {v: k for k, v in RENAME.items()}
    for col, delim in SPLIT_ON.items():
        before = raw[original[col]].astype(str)
        changed = before.str.contains(delim, regex=False).sum()
        print(f"{col}: {changed} rows trimmed, {before.nunique()} -> {df[col].nunique()} distinct values")
    blanks = raw[[HAPPY.format(a) for a in HAPPINESS_AREAS]].isna().sum()
    print(f"Blank happiness answers per question: {blanks.min()} to {blanks.max()}")
    print(f"Blank education answers: {raw['Q12 - Highest Level of Education'].isna().sum()}")
    print(f"Salary bands: {df['salary_band'].nunique()}")

    print("\n== Dashboard cards and gauges ==")
    print(f"Count of survey takers: {df['unique_id'].count()}")
    print(f"Average age: {df['age'].mean():.2f}")
    for area in HAPPINESS_AREAS:
        print(f"Happiness with {area}: {raw[HAPPY.format(area)].mean():.2f} / 10")

    print("\n== Favorite programming language ==")
    for lang, count in df["favorite_language"].value_counts().items():
        print(f"{lang}: {count} ({pct(count, n)})")

    print("\n== Difficulty breaking into data ==")
    for answer, count in df["difficulty"].value_counts().items():
        print(f"{answer}: {count} ({pct(count, n)})")
    hard = df["difficulty"].isin(["Difficult", "Very Difficult"]).sum()
    print(f"Difficult or very difficult: {hard} ({pct(hard, n)})")

    print("\n== Average salary (band midpoint, $k) ==")
    by_role = df.groupby("role")["avg_salary_k"].agg(["mean", "count"])
    for role, row in by_role.sort_values("mean", ascending=False).iterrows():
        print(f"{role}: {row['mean']:.2f} (n={int(row['count'])})")
    for gender, value in df.groupby("gender")["avg_salary_k"].mean().items():
        print(f"{gender}: {value:.2f}")

    print("\n== Other ==")
    switched = (df["switched_careers"] == "Yes").sum()
    print(f"Switched careers into data: {switched} ({pct(switched, n)})")
    other_country = (df["country"] == "Other").sum()
    print(f"Country 'Other': {other_country} ({pct(other_country, n)})")


if __name__ == "__main__":
    main()
