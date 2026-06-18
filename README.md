# LendInsight — Lending Business Decision Support System

> A full-stack business intelligence capstone project simulating the analytical workflow of an Associate Business/Data Analyst at a lending institution.

---

## Project Overview

LendInsight is a comprehensive **end-to-end data analysis system** built to solve a real business problem in consumer lending:

> **How can a bank grow its loan portfolio without increasing credit losses?**

This project analyses **32,411 loan records** to identify default patterns, build a risk segmentation model, and deliver six evidence-based business recommendations — all presented through SQL analysis, Python EDA, Excel dashboards, and a Power BI executive dashboard.

---

## Key Business Findings

| Finding | Value |
|---------|-------|
| Overall Default Rate | **21.87%** — critically above 3–5% industry benchmark |
| Total Portfolio Exposure | **$310.94M** |
| Defaulted Loan Exposure | **$76.97M** |
| HIGH Risk Segment Default Rate | **69.86%** |
| LOW Risk Segment Default Rate | **5.85%** |
| Segmentation Spread | **64 percentage points** |
| Income Gap (Repaid vs Defaulted) | **$20,239/year** |
| Prior Defaulters Re-default Rate | **38% vs 18%** for clean borrowers |

---

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python 3.13** | ETL pipeline, EDA, chart generation, report generation |
| **pandas / numpy** | Data cleaning and transformation |
| **matplotlib / seaborn** | 10 business visualisations |
| **openpyxl** | Automated Excel workbook generation |
| **SQL Server Express** | Relational database with PK/FK schema |
| **T-SQL (SSMS)** | 6 analytical SQL scripts |
| **Microsoft Excel** | 6-sheet formatted analysis workbook |
| **Power BI Desktop** | 5-page interactive dashboard |
| **python-docx** | Automated Word report generation |

---

## Project Structure

```
LendInsight/
│
├── 00_documentation/          # Business & functional requirements
│   ├── BRD_LendInsight.md     # Business Requirements Document
│   ├── FRD_LendInsight.md     # Functional Requirements Document
│   ├── Data_Dictionary_LendInsight.md
│   └── ER_Diagram_dbml.txt    # Entity-Relationship diagram (DBML)
│
├── 01_data/
│   ├── raw/                   # Original dataset (32,581 rows)
│   └── clean/                 # ETL output (32,411 rows, 15 columns)
│
├── 02_sql/                    # T-SQL analysis scripts (SQL Server)
│   ├── 01_verify_data.sql
│   ├── 02_portfolio_kpis.sql
│   ├── 03_risk_analysis.sql
│   ├── 04_segment_analysis.sql
│   ├── 05_portfolio_summary.sql
│   └── 06_business_insights.sql
│
├── 03_python/                 # Python scripts and Jupyter notebooks
│   ├── etl_pipeline.py        # Full ETL: Extract → Transform → Load
│   ├── run_eda.py             # EDA chart generator (10 charts)
│   ├── generate_excel.py      # Excel workbook generator
│   ├── generate_report.py     # Word report generator
│   ├── 01_data_exploration.ipynb
│   ├── 02_eda_visualizations.ipynb
│   ├── 03_risk_segmentation.ipynb
│   └── charts/                # 10 exported PNG charts
│
├── 04_excel/
│   └── LendInsight_Analysis.xlsx  # 6-sheet formatted workbook
│
├── 05_powerbi/
│   └── LendInsight_Dashboard.pbix # 5-page interactive dashboard
│
└── 06_report/
    └── LendInsight_Final_Report.docx
```

---

## Phase Breakdown

| Phase | Deliverable | Status |
|-------|------------|--------|
| Phase 0 | Business & Functional Requirements (BRD + FRD) | Complete |
| Phase 1 | Data Dictionary + ER Diagram | Complete |
| Phase 2 | ETL Pipeline (Python → SQL Server) | Complete |
| Phase 3 | SQL Analysis — 6 scripts, 30+ queries | Complete |
| Phase 4 | Excel Analysis — 6-sheet workbook | Complete |
| Phase 5 | Python EDA — 3 notebooks, 10 charts | Complete |
| Phase 6 | Power BI Dashboard — 5 pages | Complete |
| Phase 7 | Final Business Intelligence Report | Complete |

---

## ETL Pipeline Summary

The `etl_pipeline.py` script performs a full Extract → Transform → Load cycle:

**Cleaning steps:**
- Removed 165 duplicate records
- Removed 5 age outliers (age > 100)
- Capped income at 99th percentile ($225,000) — 322 records affected
- Median imputation for `emp_length` (887 nulls) and `loan_int_rate` (3,094 nulls)
- Standardised all categorical columns to UPPERCASE

**Derived columns created:**

| Column | Logic |
|--------|-------|
| `risk_category` | HIGH if Grade E/F/G or DTI > 0.40; LOW if Grade A/B and DTI < 0.20; else MEDIUM |
| `income_bracket` | Low / Middle / Upper-Middle / High Income |
| `dti_bracket` | Low / Moderate / High / Very High DTI |

**Output:** `customers` and `loans` tables loaded into SQL Server Express with PK/FK constraints.

---

## SQL Analysis Highlights

Six T-SQL scripts run against `lendsight_db` in SQL Server Express:

- **Portfolio KPIs** — Default rate, total exposure, avg loan amount
- **Risk Analysis** — Default rate by grade, intent, DTI, income, home ownership
- **Segment Analysis** — Risk category deep-dive, top 10 riskiest profiles
- **Portfolio Summary** — Exposure by grade, defaulter vs non-defaulter profiles
- **Business Insights** — Cross-dimensional analysis for report recommendations

---

## Power BI Dashboard — 5 Pages

| Page | Audience | Purpose |
|------|----------|---------|
| Executive Summary | Senior Management | KPI cards, grade chart, risk split |
| Risk Analysis | Credit Risk Manager | Default rate by all dimensions |
| Portfolio Analysis | Portfolio Manager | Exposure, interest rate, loan size |
| Customer Segmentation | Analytics Team | Heatmap, segment comparison |
| High-Risk Deep Dive | Credit Risk Manager | Filtered HIGH segment analysis |

---

## Business Recommendations

1. **Segment-Based Approval Policy** — Restrict HIGH risk approvals or mandate collateral
2. **Risk-Adjusted Pricing** — Price HIGH risk borrowers at a premium
3. **Monitor Riskiest Loan Purposes** — Apply stricter underwriting to highest-default purposes
4. **Prior Bureau Default as Hard Filter** — 38% re-default rate justifies hard screening
5. **Income-Based Loan Caps** — Set loan limits relative to income bracket, not flat amounts
6. **Rebalance Portfolio** — Grow Grade A/B book, reduce Grade E-G concentration

---

## Dataset

- **Source**: [Credit Risk Dataset — Kaggle (Laotse)](https://www.kaggle.com/datasets/laotse/credit-risk-dataset)
- **Raw records**: 32,581
- **Clean records**: 32,411 (after ETL)
- **Features**: 12 original + 3 derived = 15 columns

---

## How to Run

```bash
# 1. Install dependencies
pip install pandas numpy sqlalchemy pyodbc openpyxl matplotlib seaborn python-docx nbformat

# 2. Run the ETL pipeline (requires SQL Server Express)
python 03_python/etl_pipeline.py

# 3. Generate EDA charts
python 03_python/run_eda.py

# 4. Generate Excel workbook
python 03_python/generate_excel.py

# 5. Generate Word report
python 03_python/generate_report.py

# 6. Open notebooks in Jupyter
jupyter notebook 03_python/
```

---

## Author

Built as a capstone project targeting **Associate Business Analyst / Data Analyst** roles.  
Demonstrates: Business Analysis · Data Analysis · ETL · SQL · Python · Excel · Power BI · Reporting

---

*LendInsight — Turning raw loan data into business intelligence*
