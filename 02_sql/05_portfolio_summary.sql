-- ============================================================
-- LendInsight | Script 05: Portfolio Summary
-- Purpose : Portfolio composition, exposure, and concentration
-- Stakeholder: Portfolio Manager, Senior Management
-- Run in  : SSMS → lendsight_db
-- ============================================================

USE lendsight_db;

-- ─────────────────────────────────────────────────────────────
-- PORT 1: Total Exposure by Loan Grade
-- Business Question: Where is our capital concentrated?
-- ─────────────────────────────────────────────────────────────
SELECT
    loan_grade,
    COUNT(*)                                                        AS loan_count,
    CAST(SUM(loan_amnt) AS BIGINT)                                 AS total_exposure_usd,
    CAST(SUM(loan_amnt) * 100.0 / SUM(SUM(loan_amnt)) OVER()
         AS DECIMAL(5,2))                                          AS pct_of_total_exposure,
    CAST(AVG(loan_amnt) AS DECIMAL(10,2))                          AS avg_loan_usd,
    CAST(AVG(loan_int_rate) AS DECIMAL(5,2))                       AS avg_rate_pct
FROM loans
GROUP BY loan_grade
ORDER BY loan_grade;

-- ─────────────────────────────────────────────────────────────
-- PORT 2: Average Loan Amount by Loan Intent
-- Business Question: Which loan purpose drives the largest loans?
-- ─────────────────────────────────────────────────────────────
SELECT
    loan_intent,
    COUNT(*)                                                        AS loan_count,
    CAST(AVG(loan_amnt) AS DECIMAL(10,2))                          AS avg_loan_usd,
    CAST(MIN(loan_amnt) AS DECIMAL(10,2))                          AS min_loan_usd,
    CAST(MAX(loan_amnt) AS DECIMAL(10,2))                          AS max_loan_usd,
    CAST(SUM(loan_amnt) AS BIGINT)                                 AS total_exposure_usd
FROM loans
GROUP BY loan_intent
ORDER BY avg_loan_usd DESC;

-- ─────────────────────────────────────────────────────────────
-- PORT 3: Defaulters vs Non-Defaulters — Full Profile Comparison
-- Business Question: How different are the two groups?
-- ─────────────────────────────────────────────────────────────
SELECT
    l.default_flag,
    COUNT(*)                                                        AS loan_count,
    CAST(AVG(c.person_income) AS DECIMAL(10,2))                    AS avg_income_usd,
    CAST(AVG(l.loan_amnt) AS DECIMAL(10,2))                        AS avg_loan_usd,
    CAST(AVG(l.loan_int_rate) AS DECIMAL(5,2))                     AS avg_interest_rate_pct,
    CAST(AVG(l.loan_percent_income) AS DECIMAL(5,3))               AS avg_dti,
    CAST(AVG(c.person_age) AS DECIMAL(5,1))                        AS avg_age,
    CAST(AVG(c.person_emp_length) AS DECIMAL(5,1))                 AS avg_emp_years,
    CAST(AVG(c.cred_hist_length) AS DECIMAL(5,1))                  AS avg_credit_history_yrs
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
GROUP BY l.default_flag;

-- ─────────────────────────────────────────────────────────────
-- PORT 4: Loan Volume by Intent and Grade (Portfolio Matrix)
-- Business Question: How is the portfolio distributed?
-- ─────────────────────────────────────────────────────────────
SELECT
    loan_intent,
    SUM(CASE WHEN loan_grade = 'A' THEN 1 ELSE 0 END)             AS grade_A,
    SUM(CASE WHEN loan_grade = 'B' THEN 1 ELSE 0 END)             AS grade_B,
    SUM(CASE WHEN loan_grade = 'C' THEN 1 ELSE 0 END)             AS grade_C,
    SUM(CASE WHEN loan_grade = 'D' THEN 1 ELSE 0 END)             AS grade_D,
    SUM(CASE WHEN loan_grade = 'E' THEN 1 ELSE 0 END)             AS grade_E,
    SUM(CASE WHEN loan_grade = 'F' THEN 1 ELSE 0 END)             AS grade_F,
    SUM(CASE WHEN loan_grade = 'G' THEN 1 ELSE 0 END)             AS grade_G,
    COUNT(*)                                                        AS total
FROM loans
GROUP BY loan_intent
ORDER BY total DESC;

-- ─────────────────────────────────────────────────────────────
-- PORT 5: Prior Default Customers — Behavioural Risk
-- Business Question: Do prior-defaulters borrow more and repay less?
-- ─────────────────────────────────────────────────────────────
SELECT
    c.cb_default_on_file                                            AS prior_default,
    COUNT(*)                                                        AS total_loans,
    CAST(AVG(l.loan_amnt) AS DECIMAL(10,2))                        AS avg_loan_usd,
    CAST(AVG(l.loan_int_rate) AS DECIMAL(5,2))                     AS avg_rate_pct,
    SUM(l.default_flag)                                             AS current_defaults,
    CAST(SUM(l.default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))  AS current_default_rate_pct
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
GROUP BY c.cb_default_on_file;

-- ─────────────────────────────────────────────────────────────
-- PORT 6: Interest Rate vs Default Rate (Rate Brackets)
-- Business Question: Are higher-rate loans defaulting more?
-- ─────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN loan_int_rate < 8                    THEN 'Below 8%'
        WHEN loan_int_rate BETWEEN 8 AND 11.99    THEN '8-12%'
        WHEN loan_int_rate BETWEEN 12 AND 15.99   THEN '12-16%'
        WHEN loan_int_rate BETWEEN 16 AND 19.99   THEN '16-20%'
        ELSE 'Above 20%'
    END                                                             AS rate_band,
    COUNT(*)                                                        AS loan_count,
    SUM(default_flag)                                               AS defaults,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS default_rate_pct,
    CAST(AVG(loan_int_rate) AS DECIMAL(5,2))                       AS avg_rate_pct
FROM loans
GROUP BY
    CASE
        WHEN loan_int_rate < 8                    THEN 'Below 8%'
        WHEN loan_int_rate BETWEEN 8 AND 11.99    THEN '8-12%'
        WHEN loan_int_rate BETWEEN 12 AND 15.99   THEN '12-16%'
        WHEN loan_int_rate BETWEEN 16 AND 19.99   THEN '16-20%'
        ELSE 'Above 20%'
    END
ORDER BY MIN(loan_int_rate);
