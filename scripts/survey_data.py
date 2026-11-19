"""Load the raw survey Excel file and apply the same cleaning as the Power Query script (scripts.txt)."""
import re
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCEL_PATH = REPO_ROOT / "datasets" / "Power BI - Final Project.xlsx"
SHEET = "Data Professional Survey"

HAPPY = "Q6 - How Happy are you in your Current Position with the following? ({})"
HAPPINESS_AREAS = [
    "Salary",
    "Work/Life Balance",
    "Coworkers",
    "Management",
    "Upward Mobility",
    "Learning New Things",
]

# Short names used in the cleaned table and the SQLite database.
RENAME = {
    "Unique ID": "unique_id",
    "Date Taken (America/New_York)": "date_taken",
    "Q1 - Which Title Best Fits your Current Role?": "role",
    "Q2 - Did you switch careers into Data?": "switched_careers",
    "Q3 - Current Yearly Salary (in USD)": "salary_band",
    "Q4 - What Industry do you work in?": "industry",
    "Q5 - Favorite Programming Language": "favorite_language",
    HAPPY.format("Salary"): "happy_salary",
    HAPPY.format("Work/Life Balance"): "happy_work_life",
    HAPPY.format("Coworkers"): "happy_coworkers",
    HAPPY.format("Management"): "happy_management",
    HAPPY.format("Upward Mobility"): "happy_upward_mobility",
    HAPPY.format("Learning New Things"): "happy_learning",
    "Q7 - How difficult was it for you to break into Data?": "difficulty",
    "Q9 - Male/Female?": "gender",
    "Q10 - Current Age": "age",
    "Q11 - Which Country do you live in?": "country",
    "Q12 - Highest Level of Education": "education",
    "Q13 - Ethnicity": "ethnicity",
}

# Power Query keeps only the text before these characters, which folds
# "Other (Please Specify): ..." free text into "Other".
SPLIT_ON = {
    "role": "(",
    "favorite_language": ":",
    "country": "(",
    "industry": "(",
    "ethnicity": "(",
}


def load_raw(path=EXCEL_PATH):
    return pd.read_excel(path, sheet_name=SHEET)


def band_bounds(band):
    """'41k-65k' -> (41, 65); '225k+' -> (225, 225). Same rule as Power Query."""
    parts = re.split(r"(?<=\d)(?=\D)", band)
    low = int(parts[0])
    high = int(parts[1].replace("k", "").replace("-", "").replace("+", "225"))
    return low, high


def clean(raw):
    df = raw[list(RENAME)].rename(columns=RENAME).copy()
    for col, delim in SPLIT_ON.items():
        df[col] = df[col].astype(str).str.split(delim, n=1, regex=False).str[0].str.strip()
    df["date_taken"] = pd.to_datetime(df["date_taken"]).dt.date.astype(str)
    bounds = df["salary_band"].map(band_bounds)
    df["avg_salary_k"] = bounds.map(lambda b: (b[0] + b[1]) / 2)
    return df
