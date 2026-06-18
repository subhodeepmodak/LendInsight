"""
=============================================================
LendInsight -- ETL Pipeline
=============================================================
Project      : LendInsight Lending Business Decision Support System
Author       : [Your Name]
Description  : Extracts raw loan data, transforms and cleans it,
               creates derived business columns, and loads the
               result into SQL Server Express and a cleaned CSV.
Database     : SQL Server Express (Windows Authentication)
=============================================================
"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import warnings
import os

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIG
# No password needed -- uses Windows Authentication
# ─────────────────────────────────────────────
SERVER     = r".\SQLEXPRESS"      # SQL Server Express instance
DB_NAME    = "lendsight_db"
DRIVER     = "ODBC+Driver+17+for+SQL+Server"

RAW_PATH   = r"C:\data_analyst\LendInsight\01_data\raw\credit_risk_dataset.csv"
CLEAN_PATH = r"C:\data_analyst\LendInsight\01_data\clean\credit_risk_cleaned.csv"

# SQLAlchemy connection string (Windows Auth = no username/password)
CONN_STR = (
    f"mssql+pyodbc://@{SERVER}/{DB_NAME}"
    f"?driver={DRIVER}&trusted_connection=yes"
)
CONN_STR_MASTER = (
    f"mssql+pyodbc://@{SERVER}/master"
    f"?driver={DRIVER}&trusted_connection=yes"
)


# ─────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────
def section(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


# ─────────────────────────────────────────────
# STEP 1: EXTRACT
# ─────────────────────────────────────────────
section("STEP 1: EXTRACT -- Loading Raw Data")

df = pd.read_csv(RAW_PATH)

raw_rows = len(df)
print(f"  Raw rows loaded   : {raw_rows:,}")
print(f"  Columns           : {len(df.columns)}")
print(f"  Column names      : {list(df.columns)}")

print("\n  Null counts per column (raw):")
for col, cnt in df.isnull().sum().items():
    if cnt > 0:
        print(f"    {col:35s} -> {cnt:,} nulls ({cnt/raw_rows*100:.1f}%)")


# ─────────────────────────────────────────────
# STEP 2: TRANSFORM
# ─────────────────────────────────────────────
section("STEP 2: TRANSFORM -- Cleaning & Enriching")

# 2a. Remove duplicates
before = len(df)
df = df.drop_duplicates()
print(f"  Duplicates removed          : {before - len(df):,}")

# 2b. Remove age outliers
before = len(df)
df = df[df["person_age"] <= 100]
print(f"  Rows removed (age > 100)    : {before - len(df):,}")

# 2c. Cap income at 99th percentile
income_cap = df["person_income"].quantile(0.99)
capped_income = (df["person_income"] > income_cap).sum()
df["person_income"] = df["person_income"].clip(upper=income_cap)
print(f"  Income values capped (99th) : {capped_income:,}  (cap = ${income_cap:,.0f})")

# 2d. Impute emp_length with median
emp_median = df["person_emp_length"].median()
imputed_emp = df["person_emp_length"].isnull().sum()
df["person_emp_length"] = df["person_emp_length"].fillna(emp_median)
print(f"  emp_length nulls imputed    : {imputed_emp:,}  (median = {emp_median})")

# 2e. Impute loan_int_rate with median
rate_median = df["loan_int_rate"].median()
imputed_rate = df["loan_int_rate"].isnull().sum()
df["loan_int_rate"] = df["loan_int_rate"].fillna(rate_median)
print(f"  loan_int_rate nulls imputed : {imputed_rate:,}  (median = {rate_median:.2f}%)")

# 2f. Standardize text to UPPERCASE
text_cols = ["person_home_ownership", "loan_intent", "loan_grade", "cb_person_default_on_file"]
for col in text_cols:
    df[col] = df[col].str.strip().str.upper()
print(f"  Text columns standardized to uppercase")

# 2g. Rename loan_status -> default_flag
df = df.rename(columns={"loan_status": "default_flag"})
print(f"  Renamed: loan_status -> default_flag")

# 2h. Derive: risk_category (business rule-based segmentation)
def assign_risk(row):
    grade = row["loan_grade"]
    dti   = row["loan_percent_income"]
    if grade in ["E", "F", "G"] or dti > 0.40:
        return "HIGH"
    elif grade in ["A", "B"] and dti < 0.20:
        return "LOW"
    else:
        return "MEDIUM"

df["risk_category"] = df.apply(assign_risk, axis=1)
print(f"\n  Derived column: risk_category")
print(df["risk_category"].value_counts().to_string(header=False))

# 2i. Derive: income_bracket
def assign_income_bracket(income):
    if income < 30000:
        return "Low Income"
    elif income < 60000:
        return "Middle Income"
    elif income < 100000:
        return "Upper-Middle Income"
    else:
        return "High Income"

df["income_bracket"] = df["person_income"].apply(assign_income_bracket)
print(f"\n  Derived column: income_bracket")
print(df["income_bracket"].value_counts().to_string(header=False))

# 2j. Derive: dti_bracket
def assign_dti_bracket(dti):
    if dti < 0.15:
        return "Low DTI"
    elif dti < 0.30:
        return "Moderate DTI"
    elif dti <= 0.50:
        return "High DTI"
    else:
        return "Very High DTI"

df["dti_bracket"] = df["loan_percent_income"].apply(assign_dti_bracket)
print(f"\n  Derived column: dti_bracket")
print(df["dti_bracket"].value_counts().to_string(header=False))

# 2k. Final validation
final_nulls = df.isnull().sum().sum()
clean_rows  = len(df)
print(f"\n  Total nulls after cleaning  : {final_nulls}")
print(f"\n  TRANSFORM SUMMARY")
print(f"  {'Raw rows':<25}: {raw_rows:,}")
print(f"  {'Rows removed':<25}: {raw_rows - clean_rows:,}")
print(f"  {'Final clean rows':<25}: {clean_rows:,}")


# ─────────────────────────────────────────────
# STEP 3a: LOAD -- Save Clean CSV
# ─────────────────────────────────────────────
section("STEP 3a: LOAD -- Saving Cleaned CSV")

os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
df.to_csv(CLEAN_PATH, index=False)
print(f"  Saved  -> {CLEAN_PATH}")
print(f"  Rows   : {clean_rows:,} | Cols: {len(df.columns)}")


# ─────────────────────────────────────────────
# STEP 3b: LOAD -- Push to SQL Server Express
# ─────────────────────────────────────────────
section("STEP 3b: LOAD -- Pushing to SQL Server Express")

# Create the database if it doesn't exist
# SQL Server requires CREATE DATABASE to run with autocommit (outside any transaction)
engine_master = create_engine(CONN_STR_MASTER, echo=False,
                               execution_options={"isolation_level": "AUTOCOMMIT"})
with engine_master.connect() as conn:
    result = conn.execute(
        text(f"SELECT name FROM sys.databases WHERE name = '{DB_NAME}'")
    ).fetchone()
    if not result:
        conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
        print(f"  Database '{DB_NAME}' created.")
    else:
        print(f"  Database '{DB_NAME}' already exists.")

engine = create_engine(CONN_STR, echo=False)

# Enable fast_executemany for bulk insert speed (pyodbc SQL Server optimization)
from sqlalchemy import event as sa_event
@sa_event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if executemany:
        cursor.fast_executemany = True

# Build customers dataframe
customers_cols = [
    "person_age", "person_income", "person_home_ownership",
    "person_emp_length", "cb_person_default_on_file",
    "cb_person_cred_hist_length", "income_bracket"
]
df_customers = df[customers_cols].copy()
df_customers.insert(0, "customer_id", range(1, len(df_customers) + 1))
df_customers = df_customers.rename(columns={
    "cb_person_default_on_file"  : "cb_default_on_file",
    "cb_person_cred_hist_length" : "cred_hist_length"
})

# Build loans dataframe
loans_cols = [
    "loan_intent", "loan_grade", "loan_amnt", "loan_int_rate",
    "loan_percent_income", "default_flag", "risk_category", "dti_bracket"
]
df_loans = df[loans_cols].copy()
df_loans.insert(0, "loan_id", range(1, len(df_loans) + 1))
df_loans.insert(1, "customer_id", range(1, len(df_loans) + 1))

# Drop old tables then reload
with engine.begin() as conn:
    conn.execute(text("IF OBJECT_ID('loans', 'U') IS NOT NULL DROP TABLE loans"))
    conn.execute(text("IF OBJECT_ID('customers', 'U') IS NOT NULL DROP TABLE customers"))

# chunksize=1000 batches the inserts for better performance
df_customers.to_sql("customers", con=engine, if_exists="replace", index=False, chunksize=1000)
df_loans.to_sql("loans",     con=engine, if_exists="replace", index=False, chunksize=1000)

# Add primary and foreign keys
# SQL Server requires columns to be NOT NULL before they can be a PRIMARY KEY
with engine.begin() as conn:
    # Step 1: Make ID columns NOT NULL
    conn.execute(text("ALTER TABLE customers ALTER COLUMN customer_id INT NOT NULL"))
    conn.execute(text("ALTER TABLE loans ALTER COLUMN loan_id INT NOT NULL"))
    conn.execute(text("ALTER TABLE loans ALTER COLUMN customer_id INT NOT NULL"))
    # Step 2: Add primary keys
    conn.execute(text("ALTER TABLE customers ADD CONSTRAINT PK_customers PRIMARY KEY (customer_id)"))
    conn.execute(text("ALTER TABLE loans ADD CONSTRAINT PK_loans PRIMARY KEY (loan_id)"))
    # Step 3: Add foreign key
    conn.execute(text("""
        ALTER TABLE loans
        ADD CONSTRAINT FK_loans_customers
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    """))

print(f"  Table 'customers' loaded : {len(df_customers):,} rows")
print(f"  Table 'loans' loaded     : {len(df_loans):,} rows")
print(f"  Primary keys set on both tables")
print(f"  Foreign key: loans.customer_id -> customers.customer_id")


# ─────────────────────────────────────────────
# DONE
# ─────────────────────────────────────────────
section("ETL COMPLETE")
print(f"""
  Raw rows      : {raw_rows:,}
  Clean rows    : {clean_rows:,}
  Rows dropped  : {raw_rows - clean_rows:,}
  Nulls left    : {final_nulls}
  Derived cols  : risk_category, income_bracket, dti_bracket

  Output
  CSV    -> {CLEAN_PATH}
  DB     -> SQL Server Express: {DB_NAME}
             Tables: customers ({len(df_customers):,} rows)
                     loans     ({len(df_loans):,} rows)

  Verify in SSMS:
    USE lendsight_db;
    SELECT COUNT(*) FROM loans;
    SELECT COUNT(*) FROM customers;
""")
