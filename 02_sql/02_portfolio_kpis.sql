-- ============================================================
-- LendInsight | Script 02: Portfolio KPIs
-- Purpose : Top-level business metrics for Executive Summary
-- Stakeholder: Senior Management, Credit Risk Manager
-- Run in  : SSMS → lendsight_db
-- ============================================================

USE lendsight_db;

-- ─────────────────────────────────────────────────────────────
-- KPI 1: Overall Default Rate
-- Business Question: What % of our loans have defaulted?
-- ─────────────────────────────────────────────────────────────
SELECT
    COUNT(*)                                                         AS total_loans,
    SUM(default_flag)                                                AS total_defaults,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))     AS default_rate_pct
FROM loans;

-- ─────────────────────────────────────────────────────────────
-- KPI 2: Total Portfolio Exposure
-- Business Question: How much capital is at risk?
-- ─────────────────────────────────────────────────────────────
SELECT
    COUNT(*)                                                         AS total_loans,
    CAST(SUM(loan_amnt) AS BIGINT)                                  AS total_exposure_usd,
    CAST(AVG(loan_amnt) AS DECIMAL(10,2))                           AS avg_loan_amount_usd,
    CAST(MIN(loan_amnt) AS DECIMAL(10,2))                           AS min_loan_usd,
    CAST(MAX(loan_amnt) AS DECIMAL(10,2))                           AS max_loan_usd
FROM loans;

-- ─────────────────────────────────────────────────────────────
-- KPI 3: Average Interest Rate
-- Business Question: What is our average risk-adjusted pricing?
-- ─────────────────────────────────────────────────────────────
SELECT
    CAST(AVG(loan_int_rate) AS DECIMAL(5,2))                        AS avg_interest_rate_pct,
    CAST(MIN(loan_int_rate) AS DECIMAL(5,2))                        AS min_rate_pct,
    CAST(MAX(loan_int_rate) AS DECIMAL(5,2))                        AS max_rate_pct
FROM loans;

-- ─────────────────────────────────────────────────────────────
-- KPI 4: Prior Default Rate (Credit Bureau Signal)
-- Business Question: How many borrowers already had a prior default?
-- ─────────────────────────────────────────────────────────────
SELECT
    cb_default_on_file,
    COUNT(*)                                                         AS customer_count,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2))  AS pct_of_total
FROM customers
GROUP BY cb_default_on_file;

-- ─────────────────────────────────────────────────────────────
-- KPI 5: High-Risk Customer Count & Percentage
-- Business Question: What share of portfolio is HIGH risk?
-- ─────────────────────────────────────────────────────────────
SELECT
    risk_category,
    COUNT(*)                                                         AS count,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2))  AS pct_of_portfolio,
    CAST(SUM(loan_amnt) AS BIGINT)                                  AS total_exposure_usd,
    CAST(SUM(default_flag) * 100.0 / COUNT(*) AS DECIMAL(5,2))     AS default_rate_pct
FROM loans
GROUP BY risk_category
ORDER BY
    CASE risk_category WHEN 'HIGH' THEN 1 WHEN 'MEDIUM' THEN 2 ELSE 3 END;

-- ─────────────────────────────────────────────────────────────
-- KPI 6: Defaulted Loan Exposure
-- Business Question: How much money is tied up in defaulted loans?
-- ─────────────────────────────────────────────────────────────
SELECT
    default_flag,
    COUNT(*)                                                         AS loan_count,
    CAST(SUM(loan_amnt) AS BIGINT)                                  AS exposure_usd,
    CAST(AVG(loan_amnt) AS DECIMAL(10,2))                           AS avg_loan_usd
FROM loans
GROUP BY default_flag;
