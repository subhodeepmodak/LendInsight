-- ============================================================
-- LendInsight | Script 06: Business Insight Queries
-- Purpose : Advanced queries that directly generate report insights
-- Stakeholder: All — used in Final Report recommendations
-- Run in  : SSMS → lendsight_db
-- ============================================================

USE lendsight_db;

-- ─────────────────────────────────────────────────────────────
-- INSIGHT 1: Grade E-G default rate vs Grade A-B
-- Insight: How much riskier are low-grade loans?
-- ─────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN loan_grade IN ('A','B') THEN 'Low Risk  (Grade A-B)'
        WHEN loan_grade IN ('C','D') THEN 'Mid Risk  (Grade C-D)'
        ELSE                              'High Risk (Grade E-G)'
    END                                                             AS grade_tier,
    COUNT(*)                                                        AS loan_count,
    SUM(default_flag)                                               AS defaults,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS default_rate_pct,
    CAST(SUM(loan_amnt) AS BIGINT)                                 AS total_exposure_usd
FROM loans
GROUP BY
    CASE
        WHEN loan_grade IN ('A','B') THEN 'Low Risk  (Grade A-B)'
        WHEN loan_grade IN ('C','D') THEN 'Mid Risk  (Grade C-D)'
        ELSE                              'High Risk (Grade E-G)'
    END
ORDER BY MIN(loan_grade);

-- ─────────────────────────────────────────────────────────────
-- INSIGHT 2: Very High DTI borrowers — how bad is the default rate?
-- Insight: loan_percent_income > 0.50 = extreme affordability stress
-- ─────────────────────────────────────────────────────────────
SELECT
    dti_bracket,
    COUNT(*)                                                        AS loan_count,
    SUM(default_flag)                                               AS defaults,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS default_rate_pct,
    CAST(AVG(loan_amnt) AS DECIMAL(10,2))                          AS avg_loan_usd
FROM loans
GROUP BY dti_bracket
ORDER BY
    CASE dti_bracket
        WHEN 'Low DTI'       THEN 1
        WHEN 'Moderate DTI'  THEN 2
        WHEN 'High DTI'      THEN 3
        ELSE 4
    END;

-- ─────────────────────────────────────────────────────────────
-- INSIGHT 3: Venture loans — highest risk purpose?
-- Insight: VENTURE typically shows high default in consumer lending
-- ─────────────────────────────────────────────────────────────
SELECT
    loan_intent,
    COUNT(*)                                                        AS total_loans,
    SUM(default_flag)                                               AS defaults,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS default_rate_pct,
    CAST(AVG(loan_int_rate) AS DECIMAL(5,2))                       AS avg_rate_pct,
    CAST(AVG(loan_amnt) AS DECIMAL(10,2))                          AS avg_loan_usd
FROM loans
GROUP BY loan_intent
ORDER BY default_rate_pct DESC;

-- ─────────────────────────────────────────────────────────────
-- INSIGHT 4: Low income + high DTI = compounded risk?
-- Insight: Double risk factor analysis
-- ─────────────────────────────────────────────────────────────
SELECT
    c.income_bracket,
    l.dti_bracket,
    COUNT(*)                                                        AS loan_count,
    SUM(l.default_flag)                                             AS defaults,
    CAST(SUM(l.default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))  AS default_rate_pct
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
GROUP BY c.income_bracket, l.dti_bracket
HAVING COUNT(*) >= 30
ORDER BY default_rate_pct DESC;

-- ─────────────────────────────────────────────────────────────
-- INSIGHT 5: Executive KPI Card — single-row summary
-- Use this output directly for the Power BI Executive Summary page
-- ─────────────────────────────────────────────────────────────
SELECT
    COUNT(*)                                                        AS total_loans,
    CAST(SUM(loan_amnt) / 1000000.0 AS DECIMAL(10,2))             AS total_exposure_M_usd,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))    AS overall_default_rate_pct,
    SUM(CASE WHEN risk_category = 'HIGH' THEN 1 ELSE 0 END)       AS high_risk_loans,
    CAST(AVG(loan_amnt) AS DECIMAL(10,2))                          AS avg_loan_usd,
    CAST(AVG(loan_int_rate) AS DECIMAL(5,2))                       AS avg_interest_rate_pct,
    CAST(SUM(CASE WHEN default_flag = 1 THEN loan_amnt ELSE 0 END)
         / 1000000.0 AS DECIMAL(10,2))                             AS defaulted_exposure_M_usd
FROM loans;
