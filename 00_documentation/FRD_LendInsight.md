# Functional Requirements Document (FRD)
## LendInsight: Lending Business Decision Support System

---

| Field | Detail |
|-------|--------|
| **Document Title** | Functional Requirements Document |
| **Project Name** | LendInsight — Lending Business Decision Support System |
| **Prepared By** | Subhodeep Modak |
| **Role** | Business / Data Analyst |
| **Version** | 1.0 |
| **Date** | June 2025 |
| **Status** | Final |

---

## 1. Purpose

This document defines the functional specifications of the LendInsight system. While the BRD describes *what the business needs*, this FRD describes| FR-07 | The system must classify customers into risk categories (Low / Medium / High) based on loan grade and DTI |the required outputs, calculations, filters, and behavior of every system component.

---

## 2. Data Source Specification

### 2.1 Source Dataset

| Field | Detail |
|-------|--------|
| **Source** | Kaggle — Credit Risk Dataset by Laotse |
| **Format** | CSV |
| **File Name** | `credit_risk_dataset.csv` |
| **Row Count (raw)** | ~32,581 rows |
| **Target Variable** | `loan_status` (1 = default, 0 = fully repaid) |

### 2.2 Data Dictionary

| Column Name | Data Type | Business Meaning | Role |
|-------------|-----------|-----------------|------|
| `person_age` | Integer | Borrower's age in years | Demographic risk factor |
| `person_income` | Float | Annual income (USD) | Repayment capacity |
| `person_home_ownership` | Categorical | RENT / OWN / MORTGAGE / OTHER | Collateral stability signal |
| `person_emp_length` | Float | Employment tenure (years) | Income stability proxy |
| `loan_intent` | Categorical | Loan purpose: PERSONAL, EDUCATION, MEDICAL, VENTURE, HOMEIMPROVEMENT, DEBTCONSOLIDATION | Segment classification |
| `loan_grade` | Categorical | Risk grade A (lowest) to G (highest) | Internal risk rating |
| `loan_amnt` | Float | Loan amount requested (USD) | Exposure per borrower |
| `loan_int_rate` | Float | Annual interest rate (%) | Risk-adjusted pricing |
| `loan_status` | Binary | 0 = fully repaid, 1 = defaulted | **Core target variable** |
| `loan_percent_income` | Float | Loan amount / Annual income | DTI proxy — affordability |
| `cb_person_default_on_file` | Categorical | Y / N — prior default on credit bureau | Historical behavior signal |
| `cb_person_cred_hist_length` | Integer | Credit history length (years) | Credit seniority |

---

## 3. ETL Pipeline Requirements

### 3.1 Extract

| Requirement | Detail |
|------------|--------|
| ETL-01 | Load raw CSV from `01_data/raw/credit_risk_dataset.csv` |
| ETL-02 | Log raw row count and column count at load time |
| ETL-03 | Display null count per column before any cleaning |

### 3.2 Transform

| Requirement | Detail |
|------------|--------|
| ETL-04 | Remove duplicate rows |
| ETL-05 | Handle missing values in `person_emp_length`: impute with median |
| ETL-06 | Handle missing values in `loan_int_rate`: impute with median |
| ETL-07 | Remove rows where `person_age` > 100 (data entry errors) |
| ETL-08 | Cap `person_income` outliers at 99th percentile |
| ETL-09 | Standardize all text columns to UPPERCASE |
| ETL-10 | Rename `loan_status` → `default_flag` for business clarity |
| ETL-11 | Create derived column: `risk_category` (LOW / MEDIUM / HIGH) — see logic below |
| ETL-12 | Create derived column: `income_bracket` — see logic below |
| ETL-13 | Create derived column: `dti_bracket` — see logic below |
| ETL-14 | Log post-cleaning row count and null check |


**Derived Column Logic:**

`risk_category`:
```
IF loan_grade IN (A, B) AND loan_percent_income < 0.20 → 'LOW'
IF loan_grade IN (C, D) OR loan_percent_income BETWEEN 0.20 AND 0.40 → 'MEDIUM'
IF loan_grade IN (E, F, G) OR loan_percent_income > 0.40 → 'HIGH'
```

`income_bracket`:
```
IF person_income < 30,000 → 'Low Income'
IF person_income BETWEEN 30,000 AND 60,000 → 'Middle Income'
IF person_income BETWEEN 60,000 AND 100,000 → 'Upper-Middle Income'
IF person_income > 100,000 → 'High Income'
```

`dti_bracket`:
```
IF loan_percent_income < 0.15 → 'Low DTI'
IF loan_percent_income BETWEEN 0.15 AND 0.30 → 'Moderate DTI'
IF loan_percent_income BETWEEN 0.30 AND 0.50 → 'High DTI'
IF loan_percent_income > 0.50 → 'Very High DTI'
```

### 3.3 Load

| Requirement | Detail |
|------------|--------|
| ETL-15 | Save cleaned dataset to `01_data/clean/credit_risk_cleaned.csv` |
| ETL-16 | Load cleaned data into MySQL table `lendsight_db.loans` |
| ETL-17 | Produce a summary log: rows removed, nulls imputed, outliers capped |

---

## 4. Relational Data Model

### 4.1 Tables

The flat CSV will be modeled into the following relational tables in MySQL:

**Table: `customers`**
```
customer_id         INT PRIMARY KEY AUTO_INCREMENT
person_age          INT
person_income       DECIMAL(12,2)
person_home_ownership VARCHAR(20)
person_emp_length   DECIMAL(5,1)
cb_default_on_file  CHAR(1)
cred_hist_length    INT
income_bracket      VARCHAR(30)
```

**Table: `loans`**
```
loan_id             INT PRIMARY KEY AUTO_INCREMENT
customer_id         INT FOREIGN KEY → customers.customer_id
loan_intent         VARCHAR(30)
loan_grade          CHAR(1)
loan_amnt           DECIMAL(12,2)
loan_int_rate       DECIMAL(5,2)
loan_percent_income DECIMAL(5,4)
default_flag        TINYINT(1)
risk_category       VARCHAR(10)
dti_bracket         VARCHAR(20)
```

### 4.2 Relationships
- 1 Customer → Many Loans (`customer_id` is the join key)

---

## 5. SQL Analysis Requirements

Each SQL script must produce a named business output. Results must be exportable as CSV for use in Excel and Power BI.

| Script File | Query | Output |
|------------|-------|--------|
| `03_kpi_queries.sql` | Overall default rate | Single metric |
| `03_kpi_queries.sql` | Total loan volume | Single metric |
| `03_kpi_queries.sql` | Total portfolio exposure (SUM loan_amnt) | Single metric |
| `03_kpi_queries.sql` | Average loan amount | Single metric |
| `03_kpi_queries.sql` | Prior default rate (cb_default = Y) | Single metric |
| `04_risk_analysis.sql` | Default rate by loan grade | Table: grade, count, defaults, rate |
| `04_risk_analysis.sql` | Default rate by loan intent | Table: intent, count, defaults, rate |
| `04_risk_analysis.sql` | Default rate by income bracket | Table: bracket, count, defaults, rate |
| `04_risk_analysis.sql` | Default rate by DTI bracket | Table: bracket, count, defaults, rate |
| `04_risk_analysis.sql` | Default rate by home ownership type | Table: ownership, count, defaults, rate |
| `05_segment_analysis.sql` | Default rate by risk_category | Table: category, count, defaults, rate |
| `05_segment_analysis.sql` | Risk category distribution | Table: category, count, % of total |
| `05_segment_analysis.sql` | Top 10 riskiest customer profiles | Table: grade, intent, income_bracket, default_rate |
| `06_portfolio_summary.sql` | Total exposure by loan grade | Table: grade, total_exposure, % of portfolio |
| `06_portfolio_summary.sql` | Avg loan amount by loan intent | Table: intent, avg_loan |
| `06_portfolio_summary.sql` | Prior default customers: avg loan amount vs others | Comparison table |

---

## 6. Excel Workbook Requirements

**File**: `04_excel/LendInsight_Analysis.xlsx`

| Sheet Name | Content | Source |
|-----------|---------|--------|
| `Raw Data` | Full cleaned CSV imported | `credit_risk_cleaned.csv` |
| `KPI Summary` | All top-level KPIs in one view (default rate, total loans, exposure, avg loan, prior default %) | Manual formulas + SQL output |
| `Default by Segment` | Pivot table: default rate by loan_grade and loan_intent | Raw Data pivot |
| `Income & Risk` | Pivot table: income_bracket vs default rate | Raw Data pivot |
| `Portfolio Composition` | Pivot table: loan_amnt by loan_grade and loan_intent | Raw Data pivot |
| `Charts` | At minimum 4 charts: default by grade (bar), default by intent (bar), risk segment donut, income vs default (bar) | From pivot sheets |

---

## 7. Python Analysis Requirements

### 7.1 Notebook: `01_data_exploration.ipynb`
| Requirement | Output |
|------------|--------|
| Load and preview cleaned CSV | Head, shape, dtypes |
| Null value analysis | Heatmap or table |
| Descriptive statistics | df.describe() |
| Target variable distribution | Bar chart: default vs non-default counts |
| Business commentary on each column | Markdown cells |

### 7.2 Notebook: `02_eda_visualizations.ipynb`
| Chart | Question Answered |
|-------|-----------------|
| Default rate by loan_grade (bar) | Which grades are riskiest? |
| Default rate by loan_intent (bar) | Which loan purposes fail most? |
| Income distribution: defaulters vs non-defaulters (histogram overlay) | Does income predict default? |
| loan_amnt vs default_flag (box plot) | Do bigger loans default more? |
| loan_percent_income buckets vs default rate (bar) | DTI proxy analysis |
| Credit history length vs default rate (line/bar) | Does seniority reduce risk? |
| Correlation heatmap (numeric columns) | What drives default? |
| Home ownership vs default rate (bar) | Does housing stability matter? |

### 7.3 Notebook: `03_risk_segmentation.ipynb`
| Requirement | Output |
|------------|--------|
| Apply risk_category logic (LOW / MEDIUM / HIGH) | New column in dataframe |
| Default rate per risk category | Validation bar chart |
| Risk category distribution | Donut chart |
| Cross-tab: risk_category vs loan_intent | Heatmap |
| Export segmented dataset | `credit_risk_segmented.csv` |



---

## 8. Power BI Dashboard Requirements

**File**: `05_powerbi/LendInsight_Dashboard.pbix`

### Page 1: Executive Summary
| Visual | Type | Fields |
|--------|------|--------|
| Total Loans | KPI Card | COUNT(loan_id) |
| Total Exposure | KPI Card | SUM(loan_amnt) |
| Overall Default Rate | KPI Card | SUM(default_flag)/COUNT(loan_id) × 100 |
| High-Risk Count | KPI Card | COUNT where risk_category = HIGH |
| Avg Loan Amount | KPI Card | AVG(loan_amnt) |
| Default Rate by Loan Grade | Bar chart | loan_grade vs default rate |
| Loan Intent Distribution | Donut chart | loan_intent |

### Page 2: Risk Analysis
| Visual | Type | Fields |
|--------|------|--------|
| Default Rate by Grade (color-coded) | Clustered bar | loan_grade, default_flag |
| Default Rate by Intent | Horizontal bar | loan_intent, default_flag |
| Risk Category Split | Donut | risk_category, count |
| Income Bracket vs Default Rate | Bar | income_bracket, default_flag |
| Prior Default % | KPI Card | cb_default_on_file = Y % |

### Page 3: Portfolio Analysis
| Visual | Type | Fields |
|--------|------|--------|
| Total Exposure by Loan Grade | Stacked bar | loan_grade, loan_amnt |
| Loan Amount Distribution | Histogram | loan_amnt |
| Avg Interest Rate by Grade | Line chart | loan_grade, loan_int_rate |
| Home Ownership vs Loan Volume | Bar | home_ownership, count |

### Page 4: Customer Segmentation
| Visual | Type | Fields |
|--------|------|--------|
| Risk Segment Count + % | Table | risk_category, count, % |
| Credit History by Risk Segment | Bar | risk_category, avg(cred_hist_length) |
| Income by Risk Segment | Box/Bar | risk_category, avg(person_income) |
| Defaulters vs Non-Defaulters Profile | Comparison table | avg income, avg loan, avg rate |

### Page 5: High-Risk Customer Deep Dive
| Visual | Type | Fields |
|--------|------|--------|
| High-Risk Customer Count | KPI Card | COUNT where risk_category = HIGH |
| High-Risk Default Rate | KPI Card | Default rate within HIGH segment |
| Top High-Risk Profiles | Filtered table | loan_grade, loan_intent, income_bracket, default_flag |
| High-Risk vs Low-Risk: Avg Loan Amount | Clustered bar | risk_category, avg(loan_amnt) |
| High-Risk vs Low-Risk: Avg Interest Rate | Clustered bar | risk_category, avg(loan_int_rate) |
| High-Risk Segment by Loan Intent | Bar | loan_intent, count (filtered to HIGH) |

### Dashboard Filters (on all pages)
- Slicer: `loan_grade`
- Slicer: `loan_intent`
- Slicer: `person_home_ownership`
- Slicer: `risk_category`

---

## 9. Report Requirements

**File**: `06_report/LendInsight_Final_Report.pdf`

| Section | Required Content |
|---------|----------------|
| Executive Summary | 1-page overview of problem, approach, and top 3 findings |
| Business Problem | FR-aligned description of 4 problems |
| Data Description | Dataset source, columns, size, limitations |
| Methodology | ETL, SQL, Excel, Python, Power BI — explained in plain English |
| Key Findings | Min. 5 findings in Observation → Interpretation → Impact → Action format |
| Dashboard Overview | Screenshots of all 5 Power BI pages |
| Recommendations | Min. 4 actionable business recommendations |
| Limitations | What the system cannot do / dataset gaps |
| Future Scope | What could be added in a real production version |
| Appendix | ER diagram, data dictionary, SQL query listing |

---

## 10. Acceptance Criteria

| Component | Acceptance Standard |
|-----------|-------------------|
| ETL | Zero nulls in cleaned output; row count logged before and after |
| SQL | All 15+ queries return results; outputs match between SQL and Python |
| Excel | Pivot tables refresh without error; all charts display correctly |
| Python (3 notebooks) | All notebooks run top-to-bottom without errors |

| Power BI | All 5 pages load; all slicers filter all visuals |
| Report | Readable without opening any code file |
| GitHub | Repo navigable in under 2 minutes |

---

*Document Version 1.0 — LendInsight Capstone Project*
