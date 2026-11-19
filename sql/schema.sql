-- Two tables: one row per respondent, plus a lookup table for the salary bands.
DROP TABLE IF EXISTS respondents;
DROP TABLE IF EXISTS salary_bands;

CREATE TABLE salary_bands (
    salary_band  TEXT PRIMARY KEY,   -- text exactly as it appears in the survey, e.g. '41k-65k'
    band_order   INTEGER NOT NULL,   -- 1 = lowest band, for sorting
    low_k        INTEGER NOT NULL,
    high_k       INTEGER NOT NULL,   -- '225k+' has no upper bound; capped at 225 as in Power Query
    midpoint_k   REAL    NOT NULL
);

INSERT INTO salary_bands (salary_band, band_order, low_k, high_k, midpoint_k) VALUES
    ('0-40k',     1,   0,  40,  20.0),
    ('41k-65k',   2,  41,  65,  53.0),
    ('66k-85k',   3,  66,  85,  75.5),
    ('86k-105k',  4,  86, 105,  95.5),
    ('106k-125k', 5, 106, 125, 115.5),
    ('125k-150k', 6, 125, 150, 137.5),
    ('150k-225k', 7, 150, 225, 187.5),
    ('225k+',     8, 225, 225, 225.0);

CREATE TABLE respondents (
    unique_id              TEXT PRIMARY KEY,
    date_taken             TEXT,
    role                   TEXT,
    switched_careers       TEXT,
    salary_band            TEXT REFERENCES salary_bands (salary_band),
    industry               TEXT,
    favorite_language      TEXT,
    happy_salary           INTEGER,
    happy_work_life        INTEGER,
    happy_coworkers        INTEGER,
    happy_management       INTEGER,
    happy_upward_mobility  INTEGER,
    happy_learning         INTEGER,
    difficulty             TEXT,
    gender                 TEXT,
    age                    INTEGER,
    country                TEXT,
    education              TEXT,
    ethnicity              TEXT
);
