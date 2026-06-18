-- ============================================================
-- LendInsight | Script 04: Segment Analysis
-- Purpose : Risk category deep-dive and customer profiling
-- Stakeholder: Credit Risk Manager, Portfolio Manager
-- Run in  : SSMS → lendsight_db
-- ============================================================

USE lendsight_db;

-- ─────────────────────────────────────────────────────────────
-- SEG 1: Risk Category — Full Performance Summary
-- Business Question: How does each risk tier perform overall?
-- ─────────────────────────────────────────────────────────────
SELECT
    risk_category,
    COUNT(*)                                                        AS total_loans,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS pct_of_portfolio,
    SUM(default_flag)                                               AS total_defaults,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS default_rate_pct,
    CAST(SUM(loan_amnt) AS BIGINT)                                 AS total_exposure_usd,
    CAST(AVG(loan_amnt) AS DECIMAL(10,2))                          AS avg_loan_usd,
    CAST(AVG(loan_int_rate) AS DECIMAL(5,2))                       AS avg_interest_rate_pct
FROM loans
GROUP BY risk_category
ORDER BY
    CASE risk_category WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END;

-- ─────────────────────────────────────────────────────────────
-- SEG 2: Risk Category vs Loan Intent Heatmap
-- Business Question: Where does HIGH risk concentrate by purpose?
-- ─────────────────────────────────────────────────────────────
SELECT
    risk_category,
    loan_intent,
    COUNT(*)                                                        AS loan_count,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS default_rate_pct
FROM loans
GROUP BY risk_category, loan_intent
ORDER BY
    CASE risk_category WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END,
    loan_intent;

-- ─────────────────────────────────────────────────────────────
-- SEG 3: Customer Age Brackets vs Default Rate
-- Business Question: Are younger borrowers riskier?
-- ─────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN c.person_age < 25              THEN 'Under 25'
        WHEN c.person_age BETWEEN 25 AND 34 THEN '25-34'
        WHEN c.person_age BETWEEN 35 AND 44 THEN '35-44'
        WHEN c.person_age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55 and above'
    END                                                             AS age_group,
    COUNT(*)                                                        AS total_loans,
    SUM(l.default_flag)                                             AS defaults,
    CAST(SUM(l.default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))  AS default_rate_pct,
    CAST(AVG(l.loan_amnt) AS DECIMAL(10,2))                        AS avg_loan_usd
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
GROUP BY
    CASE
        WHEN c.person_age < 25              THEN 'Under 25'
        WHEN c.person_age BETWEEN 25 AND 34 THEN '25-34'
        WHEN c.person_age BETWEEN 35 AND 44 THEN '35-44'
        WHEN c.person_age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55 and above'
    END
ORDER BY MIN(c.person_age);

-- ─────────────────────────────────────────────────────────────
-- SEG 4: Employment Length vs Default Rate
-- Business Question: Does job tenure reduce default risk?
-- ─────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN c.person_emp_length < 2              THEN '0-1 years'
        WHEN c.person_emp_length BETWEEN 2 AND 4  THEN '2-4 years'
        WHEN c.person_emp_length BETWEEN 5 AND 9  THEN '5-9 years'
        ELSE '10+ years'
    END                                                             AS emp_tenure,
    COUNT(*)                                                        AS total_loans,
    SUM(l.default_flag)                                             AS defaults,
    CAST(SUM(l.default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))  AS default_rate_pct,
    CAST(AVG(c.person_emp_length) AS DECIMAL(5,1))                 AS avg_emp_years
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
GROUP BY
    CASE
        WHEN c.person_emp_length < 2              THEN '0-1 years'
        WHEN c.person_emp_length BETWEEN 2 AND 4  THEN '2-4 years'
        WHEN c.person_emp_length BETWEEN 5 AND 9  THEN '5-9 years'
        ELSE '10+ years'
    END
ORDER BY MIN(c.person_emp_length);

-- ─────────────────────────────────────────────────────────────
-- SEG 5: Top 10 Riskiest Customer Profiles
-- Business Question: Which customer segment combinations default most?
-- ─────────────────────────────────────────────────────────────
SELECT TOP 10
    l.loan_grade,
    l.loan_intent,
    c.income_bracket,
    l.dti_bracket,
    COUNT(*)                                                        AS loan_count,
    SUM(l.default_flag)                                             AS defaults,
    CAST(SUM(l.default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))  AS default_rate_pct
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
GROUP BY l.loan_grade, l.loan_intent, c.income_bracket, l.dti_bracket
HAVING COUNT(*) >= 20
ORDER BY default_rate_pct DESC;

-- ─────────────────────────────────────────────────────────────
-- SEG 6: Credit History Length vs Default Rate
-- Business Question: Do borrowers with longer credit history default less?
-- ─────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN c.cred_hist_length <= 3             THEN '1-3 years'
        WHEN c.cred_hist_length BETWEEN 4 AND 7  THEN '4-7 years'
        WHEN c.cred_hist_length BETWEEN 8 AND 15 THEN '8-15 years'
        ELSE '15+ years'
    END                                                             AS credit_history_band,
    COUNT(*)                                                        AS total_loans,
    SUM(l.default_flag)                                             AS defaults,
    CAST(SUM(l.default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))  AS default_rate_pct,
    CAST(AVG(c.cred_hist_length) AS DECIMAL(5,1))                  AS avg_history_years
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
GROUP BY
    CASE
        WHEN c.cred_hist_length <= 3             THEN '1-3 years'
        WHEN c.cred_hist_length BETWEEN 4 AND 7  THEN '4-7 years'
        WHEN c.cred_hist_length BETWEEN 8 AND 15 THEN '8-15 years'
        ELSE '15+ years'
    END
ORDER BY MIN(c.cred_hist_length);
