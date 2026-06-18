# Business Requirements Document (BRD)
## LendInsight: Lending Business Decision Support System

---

| Field | Detail |
|-------|--------|
| **Document Title** | Business Requirements Document |
| **Project Name** | LendInsight — Lending Business Decision Support System |
| **Prepared By** | [Your Name] |
| **Role** | Business / Data Analyst |
| **Version** | 1.0 |
| **Date** | June 2025 |
| **Status** | Final |

---

## 1. Executive Summary

LendInsight is a business decision support system designed for a mid-sized lending institution. The system transforms raw loan application and repayment data into structured business intelligence that enables management to make faster, more informed decisions about credit risk, portfolio composition, and operational efficiency.

The system addresses four linked business problems: rising loan defaults, slow approval processes, lack of portfolio visibility, and manual reporting overhead. By combining data engineering, SQL-based analysis, Python-driven insights, and interactive dashboards, LendInsight provides each stakeholder group with the specific information they need — at the right level of detail — to act decisively and consistently.

---

## 2. Business Context

### 2.1 Company Profile

**Organization Type**: Mid-sized lending institution / retail bank

**Core Business**: Consumer lending — personal loans, education loans, medical loans, home improvement loans, debt consolidation, and venture lending.

**Revenue Model**:
- Interest income from active loans
- Origination fees
- Cross-sell and upsell to existing borrowers

**Primary Risk**:
- Loan defaults leading to write-offs
- Weak underwriting leading to poor-quality loan books
- Operational inefficiency causing customer attrition

### 2.2 Industry Context

Consumer lending is a margin-sensitive business. A 1–2% increase in default rate can significantly erode net interest income. Lenders who cannot identify risky segments early — or who make decisions based on outdated reports — face compounding losses.

The competitive environment requires:
- Faster credit decisions (customers compare across lenders)
- More precise risk targeting (not all borrowers carry the same risk)
- Consistent decisioning (manual processes introduce variability)

---

## 3. Business Problem Statement

The lending institution currently faces four interconnected business problems:

### Problem A — Rising Loan Defaults
Defaults are increasing across certain loan grades and customer segments. The business lacks a structured, real-time view of which segments are defaulting, at what rate, and why. This limits the ability to take preemptive action.

**Business Impact**: Principal loss, interest income shortfall, increased recovery costs, capital allocation inefficiency.

### Problem B — Slow Loan Approval Process
Loan evaluations involve manual document review and ad hoc risk assessment. There is no standardized scoring mechanism or decision support tool. This slows approval time and creates inconsistent decisions across loan officers.

**Business Impact**: Customer attrition (going to competitors), loan officer inefficiency, revenue opportunity loss.

### Problem C — Lack of Portfolio Visibility
Loan data exists in raw CSV and system-level files. Management cannot easily answer questions like: which loan grade is failing most, which loan purpose carries the highest default rate, or whether risk is trending upward. There is no consolidated view.

**Business Impact**: Decision blindness, late detection of portfolio deterioration, reactive rather than proactive management.

### Problem D — Manual Reporting
Monthly performance reports are prepared manually by analysts. This is time-consuming, error-prone, and results in delayed business decisions.

**Business Impact**: Analyst time wasted on low-value data preparation, quality risks from manual errors, delayed decision cycles.

---

## 4. Business Objectives

| # | Objective | Measurement |
|---|-----------|-------------|
| 1 | Enable identification of high-risk customer segments | Risk segmentation model in place; segments validated against default rates |
| 2 | Reduce information lag for management | Dashboard showing portfolio KPIs accessible without manual data preparation |
| 3 | Standardize risk assessment inputs | Defined KPIs with consistent calculation logic documented and applied |
| 4 | Support faster credit decision-making | Approval time analysis available; bottlenecks identified |
| 5 | Reduce manual reporting effort | Automated data pipeline from raw CSV to dashboard — no manual monthly refresh |
| 6 | Produce a reusable, documented analytics system | ETL, SQL, notebooks, and dashboard are documented and reproducible |

---

## 5. Stakeholders

### 5.1 Primary Stakeholders

| Stakeholder | Role | Key Information Need |
|-------------|------|---------------------|
| Credit Risk Manager | Decision-maker for credit policy | Default rate by segment, risk concentration, policy thresholds |
| Loan Officer | Operational assessor | Risk score per applicant, approval criteria, segment classification |
| Portfolio Manager | Performance owner | Portfolio volume, default exposure, approval efficiency |
| Senior Management | Executive oversight | High-level KPIs: profit risk, growth, portfolio health |

### 5.2 Secondary Stakeholders

| Stakeholder | Role | Key Information Need |
|-------------|------|---------------------|
| Compliance Team | Rule adherence monitoring | Lending policy consistency, data completeness |
| Data / Analytics Team | System maintainers | Data pipeline reliability, schema structure |

---

## 6. Scope

### 6.1 In Scope
- Analysis of consumer loan data including credit risk, repayment behavior, and borrower demographics
- ETL pipeline for data cleaning and transformation
- Relational data model design and ER diagram
- SQL-based KPI computation (MySQL)
- Excel-based portfolio summary and pivot analysis
- Python EDA and risk segmentation
- Logistic regression-based default risk scoring
- Power BI dashboard (5 pages)
- Final business report with recommendations

### 6.2 Out of Scope
- Real-time data ingestion or live database connections
- Integration with core banking or loan origination systems
- Regulatory capital calculation (Basel III / IFRS 9)
- Production-grade machine learning deployment
- Approval workflow automation

---

## 7. Business Requirements

### 7.1 Functional Requirements

| ID | Requirement |
|----|------------|
| FR-01 | The system must calculate the overall loan default rate |
| FR-02 | The system must segment customers by risk category (Low / Medium / High) |
| FR-03 | The system must display default rate by loan grade (A–G) |
| FR-04 | The system must display default rate by loan purpose (intent) |
| FR-05 | The system must display default rate by income bracket |
| FR-06 | The system must display portfolio exposure by loan grade |
| FR-07 | The system must compute a risk score (0–100) per customer |
| FR-08 | The system must identify the top high-risk customer profiles |
| FR-09 | The system must display portfolio-level KPIs on an interactive dashboard |
| FR-10 | The system must allow filtering by loan grade, loan intent, and home ownership |
| FR-11 | The system must produce a data dictionary documenting all fields |
| FR-12 | The system must provide a cleaned, validated dataset for all downstream analysis |

### 7.2 Non-Functional Requirements

| ID | Requirement |
|----|------------|
| NFR-01 | The dashboard must be readable by a non-technical business user |
| NFR-02 | All analysis must be reproducible — scripts must run end-to-end |
| NFR-03 | All KPI definitions must be clearly documented |
| NFR-04 | Data cleaning must be traceable — before/after row counts documented |
| NFR-05 | The report must be readable as a standalone document without needing to open code |
| NFR-06 | The GitHub repository must be structured so a reviewer can navigate it in under 2 minutes |

---

## 8. Key Performance Indicators (KPIs)

| KPI | Definition | Calculation | Why It Matters |
|-----|-----------|-------------|----------------|
| Default Rate | % of loans that resulted in a default | (Defaulted loans / Total loans) × 100 | Core portfolio health metric |
| Total Loan Volume | Total number of loans in portfolio | COUNT(loan_id) | Scale indicator |
| Total Exposure | Sum of all outstanding loan amounts | SUM(loan_amnt) | Risk capital at stake |
| Average Loan Amount | Mean loan size across portfolio | AVG(loan_amnt) | Customer segment indicator |
| Default Rate by Grade | Default rate within each loan grade (A–G) | Segmented default rate | Risk grading effectiveness |
| Default Rate by Intent | Default rate by loan purpose | Segmented default rate | Portfolio composition risk |
| High-Risk Customer % | % of customers in High risk segment | (High-risk count / Total) × 100 | Portfolio risk concentration |
| Prior Default Rate | % with prior default on credit bureau file | COUNT(cb_default=Y) / Total | Behavioral risk signal |

---

## 9. AS-IS Process (Current State)

**Current Loan Evaluation Process:**

```
Customer applies
      ↓
Loan officer manually reviews documents
      ↓
Ad hoc risk assessment (no standard scoring)
      ↓
Manual approval / rejection decision
      ↓
Data stored in disconnected CSV files
      ↓
Monthly analyst manually compiles reports
      ↓
Report sent to management (often delayed)
      ↓
Management makes decisions based on stale data
```

**Pain Points:**
- No standardized risk scoring → inconsistent decisions
- Manual report compilation → time cost + error risk
- No real-time portfolio view → reactive management
- No segment-level risk tracking → defaults discovered late
- Data scattered across files → fragmented visibility

---

## 10. TO-BE Process (Future State)

**Improved Process with LendInsight:**

```
Customer applies
      ↓
Automated data intake → ETL pipeline cleans and loads data
      ↓
Risk score auto-calculated (logistic model)
      ↓
Loan officer reviews risk score + segment classification on dashboard
      ↓
Consistent, criteria-based approval decision
      ↓
Data auto-refreshed in Power BI dashboard
      ↓
Management views portfolio KPIs in real time
      ↓
Proactive action on rising risk segments
```

**Improvements:**
- Standardized risk scoring → consistent decisions
- Automated pipeline → no manual monthly prep
- Live dashboard → real-time portfolio visibility
- Segment-level monitoring → early default detection
- Centralized data model → single source of truth

---

## 11. Assumptions

1. The Credit Risk Dataset (Kaggle) is treated as representative of a real lending institution's loan book.
2. The `loan_status` column (1 = default, 0 = repaid) is the ground truth for default classification.
3. Loan grades (A–G) reflect the institution's internal risk grading system.
4. `loan_percent_income` is used as a proxy for the Debt-to-Income (DTI) ratio.
5. Branch-level and approval-time data are not present in the dataset; noted as limitations.

---

## 12. Constraints

| Constraint | Detail |
|-----------|--------|
| Dataset scope | Single CSV — no time-series, no branch-level data |
| No real-time pipeline | Analysis is batch-mode on static dataset |
| Model simplicity | Logistic regression only — not a production model |
| Tool availability | Desktop tools: Python, MySQL, Excel, Power BI |

---

## 13. Success Criteria

- [ ] BRD and FRD are finalized and documented
- [ ] ER diagram and data dictionary are complete
- [ ] ETL pipeline runs end-to-end without errors
- [ ] All SQL queries produce validated business outputs
- [ ] Excel workbook contains pivot analysis and summary KPIs
- [ ] Python notebooks are clean, commented, and reproducible
- [ ] Risk segmentation and scoring are validated
- [ ] Power BI dashboard has all 5 pages with working filters
- [ ] Final report is complete with recommendations
- [ ] GitHub repository is structured with README and screenshots

---

*Document Version 1.0 — LendInsight Capstone Project*
