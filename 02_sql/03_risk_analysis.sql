-- ============================================================
-- LendInsight | Script 03: Risk Analysis
-- Purpose : Default rates broken down by key risk dimensions
-- Stakeholder: Credit Risk Manager, Loan Officer
-- Run in  : SSMS → lendsight_db
-- ============================================================

USE lendsight_db;

-- ─────────────────────────────────────────────────────────────
-- RISK 1: Default Rate by Loan Grade (A to G)
-- Business Question: Which grade bands are failing most?
-- Insight: Grades E-G are highest risk → used in risk_category logic
-- ─────────────────────────────────────────────────────────────
SELECT
    loan_grade,
    COUNT(*)                                                        AS total_loans,
    SUM(default_flag)                                               AS defaults,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS default_rate_pct,
    CAST(SUM(loan_amnt) AS BIGINT)                                 AS total_exposure_usd
FROM loans
GROUP BY loan_grade
ORDER BY loan_grade;

-- ─────────────────────────────────────────────────────────────
-- RISK 2: Default Rate by Loan Intent (Purpose)
-- Business Question: Which loan purpose has the highest failure rate?
-- ─────────────────────────────────────────────────────────────
SELECT
    loan_intent,
    COUNT(*)                                                        AS total_loans,
    SUM(default_flag)                                               AS defaults,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS default_rate_pct,
    CAST(AVG(loan_amnt) AS DECIMAL(10,2))                          AS avg_loan_usd
FROM loans
GROUP BY loan_intent
ORDER BY default_rate_pct DESC;

-- ─────────────────────────────────────────────────────────────
-- RISK 3: Default Rate by DTI Bracket
-- Business Question: Does higher debt burden mean more defaults?
-- ─────────────────────────────────────────────────────────────
SELECT
    dti_bracket,
    COUNT(*)                                                        AS total_loans,
    SUM(default_flag)                                               AS defaults,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS default_rate_pct,
    CAST(AVG(loan_percent_income) AS DECIMAL(5,3))                 AS avg_dti
FROM loans
GROUP BY dti_bracket
ORDER BY avg_dti;

-- ─────────────────────────────────────────────────────────────
-- RISK 4: Default Rate by Home Ownership Type
-- Business Question: Does housing stability affect default risk?
-- ─────────────────────────────────────────────────────────────
SELECT
    c.person_home_ownership,
    COUNT(*)                                                        AS total_loans,
    SUM(l.default_flag)                                             AS defaults,
    CAST(SUM(l.default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))  AS default_rate_pct,
    CAST(AVG(l.loan_amnt) AS DECIMAL(10,2))                        AS avg_loan_usd
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
GROUP BY c.person_home_ownership
ORDER BY default_rate_pct DESC;

-- ─────────────────────────────────────────────────────────────
-- RISK 5: Default Rate by Income Bracket
-- Business Question: Does income level determine repayment ability?
-- ─────────────────────────────────────────────────────────────
SELECT
    c.income_bracket,
    COUNT(*)                                                        AS total_loans,
    SUM(l.default_flag)                                             AS defaults,
    CAST(SUM(l.default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))  AS default_rate_pct,
    CAST(AVG(c.person_income) AS DECIMAL(10,2))                    AS avg_income_usd
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
GROUP BY c.income_bracket
ORDER BY avg_income_usd;

-- ─────────────────────────────────────────────────────────────
-- RISK 6: Impact of Prior Credit Bureau Default
-- Business Question: Are borrowers with prior defaults more likely to default again?
-- ─────────────────────────────────────────────────────────────
SELECT
    c.cb_default_on_file                                            AS prior_default,
    COUNT(*)                                                        AS total_loans,
    SUM(l.default_flag)                                             AS defaults,
    CAST(SUM(l.default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))  AS default_rate_pct
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
GROUP BY c.cb_default_on_file
ORDER BY c.cb_default_on_file;

-- ─────────────────────────────────────────────────────────────
-- RISK 7: Default Rate by Loan Grade AND Intent (Cross-Analysis)
-- Business Question: Which grade+purpose combination is riskiest?
-- ─────────────────────────────────────────────────────────────
SELECT TOP 15
    loan_grade,
    loan_intent,
    COUNT(*)                                                        AS total_loans,
    SUM(default_flag)                                               AS defaults,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS default_rate_pct
FROM loans
GROUP BY loan_grade, loan_intent
HAVING COUNT(*) >= 50   -- only meaningful segments
ORDER BY default_rate_pct DESC;
