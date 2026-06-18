-- ============================================================
-- LendInsight | Script 01: Data Verification
-- Purpose : Confirm ETL loaded correctly before analysis
-- Run in  : SSMS → lendsight_db
-- ============================================================

USE lendsight_db;

-- 1. Row counts
SELECT 'customers' AS tbl, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'loans',            COUNT(*)               FROM loans;

-- 2. Column overview: customers
SELECT TOP 5 * FROM customers;

-- 3. Column overview: loans
SELECT TOP 5 * FROM loans;

-- 4. Null check: customers
SELECT
    SUM(CASE WHEN person_age          IS NULL THEN 1 ELSE 0 END) AS age_nulls,
    SUM(CASE WHEN person_income       IS NULL THEN 1 ELSE 0 END) AS income_nulls,
    SUM(CASE WHEN person_emp_length   IS NULL THEN 1 ELSE 0 END) AS emp_nulls,
    SUM(CASE WHEN income_bracket      IS NULL THEN 1 ELSE 0 END) AS bracket_nulls
FROM customers;

-- 5. Null check: loans
SELECT
    SUM(CASE WHEN loan_amnt           IS NULL THEN 1 ELSE 0 END) AS amnt_nulls,
    SUM(CASE WHEN loan_int_rate       IS NULL THEN 1 ELSE 0 END) AS rate_nulls,
    SUM(CASE WHEN default_flag        IS NULL THEN 1 ELSE 0 END) AS flag_nulls,
    SUM(CASE WHEN risk_category       IS NULL THEN 1 ELSE 0 END) AS risk_nulls
FROM loans;

-- 6. Default flag distribution
SELECT
    default_flag,
    COUNT(*)                                            AS loan_count,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS pct
FROM loans
GROUP BY default_flag;

-- 7. Loan grade distribution
SELECT loan_grade, COUNT(*) AS count
FROM loans
GROUP BY loan_grade
ORDER BY loan_grade;

-- 8. Risk category distribution
SELECT risk_category, COUNT(*) AS count
FROM loans
GROUP BY risk_category;
