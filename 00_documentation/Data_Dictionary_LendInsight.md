# Data Dictionary
## LendInsight: Lending Business Decision Support System

---

| Field | Detail |
|-------|--------|
| **Document** | Data Dictionary |
| **Project** | LendInsight |
| **Source Dataset** | Credit Risk Dataset — Kaggle (by Laotse) |
| **Version** | 1.0 |
| **Date** | June 2025 |

---

## 1. Source Dataset Overview

| Property | Value |
|----------|-------|
| File Name | `credit_risk_dataset.csv` |
| Raw Row Count | 32,581 |
| Column Count | 12 |
| Target Variable | `loan_status` (renamed to `default_flag` after ETL) |
| Dataset Type | Cross-sectional (no time series) |
| Grain | One row = one loan application |

---

## 2. Original Columns — Full Definitions

### Column: `person_age`
| Property | Value |
|----------|-------|
| **Table** | customers |
| **Data Type** | Integer |
| **Business Meaning** | Age of the loan applicant in years |
| **Role in Analysis** | Demographic risk indicator; younger borrowers may have shorter credit histories |
| **Valid Range** | 18 – 100 (values above 100 treated as errors and removed in ETL) |
| **Sample Values** | 22, 35, 47 |
| **Missing Values** | None |

---

### Column: `person_income`
| Property | Value |
|----------|-------|
| **Table** | customers |
| **Data Type** | Float (USD) |
| **Business Meaning** | Annual gross income of the applicant |
| **Role in Analysis** | Core repayment capacity signal; higher income generally correlates with lower default risk |
| **Valid Range** | > 0 (outliers above 99th percentile capped in ETL) |
| **Sample Values** | 59000, 9600, 65500 |
| **Missing Values** | None |

---

### Column: `person_home_ownership`
| Property | Value |
|----------|-------|
| **Table** | customers |
| **Data Type** | Categorical (string) |
| **Business Meaning** | Borrower's housing status — a proxy for financial stability and collateral |
| **Role in Analysis** | Stability signal; MORTGAGE and OWN typically indicate greater financial commitment and lower risk than RENT |
| **Valid Values** | RENT, OWN, MORTGAGE, OTHER |
| **Sample Values** | RENT, OWN, MORTGAGE |
| **Missing Values** | None |

---

### Column: `person_emp_length`
| Property | Value |
|----------|-------|
| **Table** | customers |
| **Data Type** | Float (years) |
| **Business Meaning** | Number of years the applicant has been employed at current job |
| **Role in Analysis** | Income stability proxy; longer tenure suggests more stable income and lower default risk |
| **Valid Range** | 0 – 41 years |
| **Sample Values** | 5.0, 1.0, 4.0 |
| **Missing Values** | ~2.7% missing — imputed with median in ETL |

---

### Column: `loan_intent`
| Property | Value |
|----------|-------|
| **Table** | loans |
| **Data Type** | Categorical (string) |
| **Business Meaning** | The stated purpose for which the loan is being requested |
| **Role in Analysis** | Segment classification; different loan purposes carry different default patterns |
| **Valid Values** | PERSONAL, EDUCATION, MEDICAL, VENTURE, HOMEIMPROVEMENT, DEBTCONSOLIDATION |
| **Sample Values** | PERSONAL, EDUCATION, MEDICAL |
| **Missing Values** | None |

---

### Column: `loan_grade`
| Property | Value |
|----------|-------|
| **Table** | loans |
| **Data Type** | Categorical (string) |
| **Business Meaning** | Internal risk grading assigned to the loan, from A (lowest risk) to G (highest risk) |
| **Role in Analysis** | Most direct risk signal in the dataset; used as primary input to risk_category segmentation |
| **Valid Values** | A, B, C, D, E, F, G |
| **Sample Values** | D, B, C |
| **Missing Values** | None |

---

### Column: `loan_amnt`
| Property | Value |
|----------|-------|
| **Table** | loans |
| **Data Type** | Float (USD) |
| **Business Meaning** | Amount of money requested by the applicant |
| **Role in Analysis** | Exposure metric; used in portfolio-level aggregation and risk weighting |
| **Valid Range** | > 0 |
| **Sample Values** | 35000, 1000, 5500 |
| **Missing Values** | None |

---

### Column: `loan_int_rate`
| Property | Value |
|----------|-------|
| **Table** | loans |
| **Data Type** | Float (%) |
| **Business Meaning** | Annual interest rate charged on the loan |
| **Role in Analysis** | Risk-adjusted pricing signal; higher grades (E–G) typically receive higher rates |
| **Valid Range** | 5% – 24% approximately |
| **Sample Values** | 16.02, 11.14, 12.87 |
| **Missing Values** | ~9.5% missing — imputed with median in ETL |

---

### Column: `loan_status`
| Property | Value |
|----------|-------|
| **Table** | loans |
| **Data Type** | Binary Integer |
| **Business Meaning** | Outcome of the loan — whether the borrower repaid or defaulted |
| **Renamed To** | `default_flag` after ETL for business clarity |
| **Valid Values** | 0 = Fully Repaid, 1 = Defaulted |
| **Role in Analysis** | **Core target variable** for all default rate calculations and risk analysis |
| **Missing Values** | None |

---

### Column: `loan_percent_income`
| Property | Value |
|----------|-------|
| **Table** | loans |
| **Data Type** | Float (ratio) |
| **Business Meaning** | Loan amount as a percentage of annual income (loan_amnt / person_income) |
| **Role in Analysis** | DTI proxy — measures affordability and debt burden. Higher values indicate greater financial stress |
| **Valid Range** | 0.0 – 1.0+ |
| **Sample Values** | 0.59, 0.10, 0.57 |
| **Missing Values** | None |

---

### Column: `cb_person_default_on_file`
| Property | Value |
|----------|-------|
| **Table** | customers |
| **Data Type** | Categorical (string) |
| **Business Meaning** | Whether the applicant has a prior default recorded on their credit bureau file |
| **Role in Analysis** | Behavioral risk signal — prior default history is a strong predictor of future default |
| **Valid Values** | Y = Yes (prior default exists), N = No prior default |
| **Sample Values** | Y, N |
| **Missing Values** | None |

---

### Column: `cb_person_cred_hist_length`
| Property | Value |
|----------|-------|
| **Table** | customers |
| **Data Type** | Integer (years) |
| **Business Meaning** | Length of the applicant's credit history in years |
| **Role in Analysis** | Credit seniority signal — longer histories generally indicate more predictable repayment behavior |
| **Valid Range** | 2 – 30 years |
| **Sample Values** | 3, 2, 4 |
| **Missing Values** | None |

---

## 3. Derived Columns (Created During ETL)

### Derived Column: `default_flag`
| Property | Value |
|----------|-------|
| **Source Column** | `loan_status` |
| **Logic** | Direct rename — no value transformation |
| **Purpose** | Clearer business language for reporting and dashboard labeling |

---

### Derived Column: `risk_category`
| Property | Value |
|----------|-------|
| **Table** | loans |
| **Data Type** | Categorical (string) |
| **Valid Values** | LOW, MEDIUM, HIGH |
| **Derivation Logic** | See below |
| **Purpose** | Business-interpretable risk tier for segmentation and dashboard filtering |

**Logic:**
```
IF loan_grade IN (A, B) AND loan_percent_income < 0.20  → LOW
IF loan_grade IN (E, F, G) OR loan_percent_income > 0.40 → HIGH
All others                                               → MEDIUM
```

---

### Derived Column: `income_bracket`
| Property | Value |
|----------|-------|
| **Table** | customers |
| **Data Type** | Categorical (string) |
| **Valid Values** | Low Income, Middle Income, Upper-Middle Income, High Income |
| **Derivation Logic** | See below |
| **Purpose** | Groups continuous income into business-readable segments for pivot analysis |

**Logic:**
```
person_income < 30,000                    → Low Income
person_income 30,000 – 59,999            → Middle Income
person_income 60,000 – 99,999            → Upper-Middle Income
person_income ≥ 100,000                  → High Income
```

---

### Derived Column: `dti_bracket`
| Property | Value |
|----------|-------|
| **Table** | loans |
| **Data Type** | Categorical (string) |
| **Valid Values** | Low DTI, Moderate DTI, High DTI, Very High DTI |
| **Derivation Logic** | See below |
| **Purpose** | Converts loan_percent_income ratio into a business-readable affordability label |

**Logic:**
```
loan_percent_income < 0.15               → Low DTI
loan_percent_income 0.15 – 0.29         → Moderate DTI
loan_percent_income 0.30 – 0.50         → High DTI
loan_percent_income > 0.50              → Very High DTI
```

---

## 4. Relational Table Mapping

The flat CSV is split into two logical tables in MySQL:

### Table: `customers`
| Column | Source | Type |
|--------|--------|------|
| customer_id | Generated (AUTO_INCREMENT) | INT PK |
| person_age | person_age | INT |
| person_income | person_income | DECIMAL(12,2) |
| person_home_ownership | person_home_ownership | VARCHAR(20) |
| person_emp_length | person_emp_length | DECIMAL(5,1) |
| cb_default_on_file | cb_person_default_on_file | CHAR(1) |
| cred_hist_length | cb_person_cred_hist_length | INT |
| income_bracket | Derived | VARCHAR(30) |

### Table: `loans`
| Column | Source | Type |
|--------|--------|------|
| loan_id | Generated (AUTO_INCREMENT) | INT PK |
| customer_id | Foreign key → customers | INT FK |
| loan_intent | loan_intent | VARCHAR(30) |
| loan_grade | loan_grade | CHAR(1) |
| loan_amnt | loan_amnt | DECIMAL(12,2) |
| loan_int_rate | loan_int_rate | DECIMAL(5,2) |
| loan_percent_income | loan_percent_income | DECIMAL(6,4) |
| default_flag | loan_status | TINYINT(1) |
| risk_category | Derived | VARCHAR(10) |
| dti_bracket | Derived | VARCHAR(20) |

### Relationship
```
customers.customer_id (PK)  ──<  loans.customer_id (FK)
One customer can have many loans.
```

---

## 5. ETL Quality Log Template

After running the ETL pipeline, the following metrics must be recorded:

| Metric | Value |
|--------|-------|
| Raw row count | |
| Rows removed (duplicates) | |
| Rows removed (age > 100) | |
| Rows with emp_length imputed | |
| Rows with int_rate imputed | |
| Income outliers capped | |
| Final clean row count | |
| Null count post-cleaning | 0 (expected) |

---

*Document Version 1.0 — LendInsight Capstone Project*
