"""Load the cleaned survey into a SQLite database and run the SQL in sql/analysis.sql.

Run from the repo root:
    python scripts/build_database.py

Creates survey.db in the repo root (ignored by git).
"""
import sqlite3

import pandas as pd

from survey_data import REPO_ROOT, clean, load_raw

DB_PATH = REPO_ROOT / "survey.db"
SQL_DIR = REPO_ROOT / "sql"


def load(conn):
    conn.executescript((SQL_DIR / "schema.sql").read_text(encoding="utf-8"))
    df = clean(load_raw()).drop(columns="avg_salary_k")  # salary comes from the join instead
    df.to_sql("respondents", conn, if_exists="append", index=False)
    return len(df)


def run_queries(conn):
    text = (SQL_DIR / "analysis.sql").read_text(encoding="utf-8")
    for block in text.split("-- name:")[1:]:
        title, _, query = block.partition("\n")
        print(f"\n== {title.strip()} ==")
        print(pd.read_sql_query(query, conn).to_string(index=False))


def main():
    with sqlite3.connect(DB_PATH) as conn:
        rows = load(conn)
        print(f"Loaded {rows} respondents into {DB_PATH.name}")
        run_queries(conn)


if __name__ == "__main__":
    main()
