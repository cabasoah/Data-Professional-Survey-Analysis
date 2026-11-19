# Data Professional Survey Analysis (Power BI)

What do data professionals earn, how happy are they, and how hard is it to get into the field? A Power BI dashboard built from 630 survey responses shows that Data Scientists report the highest average salary (about $94k), while salary is the lowest-rated part of the job (4.27 out of 10).

![Power BI dashboard with respondent count (630), average age (29.87), average salary by job title, favorite programming language by job title, country treemap, happiness gauges for salary (4.27) and work/life balance (5.74), average salary by sex, and a donut chart of how hard it was to break into data](./dashboard.png)

## At a glance

| | |
|---|---|
| **Problem** | Summarize pay, job satisfaction and entry difficulty for data professionals in one interactive report |
| **Data** | Online survey of data professionals, Excel file, 630 responses, 28 columns, collected 10–26 June 2022 |
| **Tools** | Power BI Desktop, Power Query (M), Excel (source data), Python (pandas), SQL (SQLite) |
| **Methods** | Data cleaning in Power Query, salary bands converted to numbers, SQL joins to a salary-band lookup table, descriptive statistics (counts, averages, percentages), every dashboard number re-checked in Python |
| **Key result** | Average salary by role ranges from about $27k (students and job seekers) to about $94k (Data Scientists). Satisfaction with salary averages 4.27/10. |

## Key findings

- **Python is the favorite language.** 420 of 630 respondents (66.7%) chose Python. R came second with 101 (16.0%).
- **Pay is the weakest point of the job.** Happiness with salary averages 4.27 out of 10, the lowest of the six areas asked about. It rises with pay: 2.86 for people earning under $40k, 8.15 for people earning $150k–225k.
- **Job title matters for pay.** Data Scientists report the highest average salary, about $94k (25 people). Data Analysts, the largest group (381 people), average about $55k.
- **Getting in is hard for about a third.** 31.7% (200 people) said breaking into data was difficult or very difficult. The most common answer, 42.7%, was "neither easy nor difficult".
- **Most people switched careers.** 59.0% (372 people) moved into data from another field.

Salaries were collected as bands (for example "41k-65k"). Averages use the midpoint of each band, so they are estimates.

## Approach

**Cleaning (Power Query, full script in [scripts/scripts.txt](scripts/scripts.txt))**
- Removed 5 tracking columns (Browser, OS, City, Country, Referrer). They were empty in all 630 rows.
- Cut the free-text part off "Other (please specify)" answers, so those answers group under "Other":
  - Job title: 88 rows changed, 83 distinct values reduced to 7
  - Favorite language: 86 rows changed, 43 values reduced to 6
  - Country: 224 rows changed, 98 values reduced to 5
  - Industry: 205 rows changed, 146 values reduced to 9
  - Ethnicity: 56 rows changed, 45 values reduced to 7
- Turned the 8 salary bands from text into numbers and added an `Average Salary` column (band midpoint, in thousands of USD). The open-ended "225k+" band is treated as 225k.
- Checked for duplicates: 0 duplicate rows and 0 duplicate respondent IDs.
- Left missing answers blank. The happiness questions have 5 to 13 blanks each and education has 52, so averages leave those respondents out.

**Data model**
- One table, `Data Professional Survey`, with no relationships.
- No DAX measures. Visuals use Power BI's built-in Count and Average, renamed inside each visual (for example "Count of Survey Takers" and "Average Age of Survey Taker").

**SQL ([sql/](sql/))**
- [schema.sql](sql/schema.sql) creates a `respondents` table (630 rows) and a `salary_bands` lookup table (8 bands with low, high and midpoint).
- [analysis.sql](sql/analysis.sql) joins the two tables:
  - A LEFT JOIN check that every respondent's band exists in the lookup (0 unmatched).
  - Average salary by job title and by gender (INNER JOIN). The results match the Power BI report.
  - Happiness with salary by salary band.
  - Share of each role earning above $65k.

**Python check ([scripts/verify_metrics.py](scripts/verify_metrics.py))**
- Reads the raw Excel file with pandas, applies the same cleaning as Power Query and prints every number used in this README. They match the dashboard.

**Report**
- One page with 2 KPI cards (respondent count, average age), 2 gauges (happiness with salary and with work/life balance), a bar chart (average salary by job title), a stacked column chart (favorite language by job title), a pie chart (average salary by sex), a donut chart (difficulty breaking into data) and a treemap (respondents by country).

## Limitations and next steps

- Salaries are band midpoints, not exact figures. The top band is capped at 225k.
- Some groups are small (3 Data Architects, 5 Database Developers), so their averages are unreliable.
- 224 of 630 respondents (35.6%) chose "Other" for country, which limits any country-level comparison.
- The country treemap uses Count (Distinct), so every tile is the same size. It should use Count. **TODO:** fix this in the .pbix and re-export dashboard.png.
- The top salary band (225k+) has only 2 people and the $150k–225k band has 13, so the happiness figures for high earners rest on few answers.
- Next step: point Power BI at the SQLite tables so the report uses the same two-table model as the SQL.

## How to reproduce

**Python and SQL** (Python 3.10 or later, run from the repo root):

```
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/verify_metrics.py    # prints all README numbers
python scripts/build_database.py    # builds survey.db and runs sql/analysis.sql
```

`survey.db` can also be opened in any SQLite tool (for example DB Browser for SQLite) to run the queries by hand.

**Power BI**

1. Install [Power BI Desktop](https://www.microsoft.com/power-bi/desktop) (Windows).
2. Open `reports/Final project.pbix`.
3. The query points to a local path on the author's machine. Go to **Transform data > Data source settings > Change Source** and select `datasets/Power BI - Final Project.xlsx`, then click **Refresh**.

There is also a [live version in Power BI Service](https://app.powerbi.com/reportEmbed?reportId=92864413-f15b-4c25-9773-68008be7981f&autoAuth=true&ctid=244e6ed2-339a-47f3-b95c-e45351c198b7). It requires a Microsoft sign-in. Without one, use [dashboard.pdf](dashboard.pdf) or the screenshot above.

## Repo structure

```
.
├── datasets/
│   └── Power BI - Final Project.xlsx   # raw survey data (630 rows)
├── reports/
│   └── Final project.pbix              # Power BI report
├── scripts/
│   ├── scripts.txt                     # Power Query (M) cleaning steps
│   ├── survey_data.py                  # loads and cleans the Excel file (same rules as Power Query)
│   ├── verify_metrics.py               # recomputes every README number
│   └── build_database.py               # loads SQLite and runs the SQL
├── sql/
│   ├── schema.sql                      # respondents + salary_bands tables
│   └── analysis.sql                    # join queries
├── dashboard.png                       # dashboard screenshot
├── dashboard.pdf                       # dashboard export
├── requirements.txt
└── README.md
```
