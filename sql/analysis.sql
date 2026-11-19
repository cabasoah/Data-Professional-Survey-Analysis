-- Each query below starts with a name line, which scripts/build_database.py prints as its title.

-- name: Data check: respondents whose salary band has no match in the lookup (LEFT JOIN, expect 0)
SELECT COUNT(*) AS unmatched_respondents
FROM respondents AS r
LEFT JOIN salary_bands AS b ON b.salary_band = r.salary_band
WHERE b.salary_band IS NULL;

-- name: Average salary by job title (INNER JOIN to the band lookup)
SELECT r.role,
       COUNT(*)                      AS respondents,
       ROUND(AVG(b.midpoint_k), 2)   AS avg_salary_k
FROM respondents AS r
JOIN salary_bands AS b ON b.salary_band = r.salary_band
GROUP BY r.role
ORDER BY avg_salary_k DESC;

-- name: Average salary by gender
SELECT r.gender,
       COUNT(*)                      AS respondents,
       ROUND(AVG(b.midpoint_k), 2)   AS avg_salary_k
FROM respondents AS r
JOIN salary_bands AS b ON b.salary_band = r.salary_band
GROUP BY r.gender;

-- name: Happiness with salary by salary band (does higher pay mean happier?)
SELECT b.salary_band,
       COUNT(r.unique_id)                AS respondents,
       ROUND(AVG(r.happy_salary), 2)     AS avg_happy_salary
FROM salary_bands AS b
LEFT JOIN respondents AS r ON r.salary_band = b.salary_band
GROUP BY b.salary_band, b.band_order
ORDER BY b.band_order;

-- name: Share of each role earning above 65k
SELECT r.role,
       COUNT(*) AS respondents,
       ROUND(100.0 * SUM(CASE WHEN b.low_k > 65 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_above_65k
FROM respondents AS r
JOIN salary_bands AS b ON b.salary_band = r.salary_band
GROUP BY r.role
ORDER BY pct_above_65k DESC;
