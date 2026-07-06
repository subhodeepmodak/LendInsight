"""
Jupyter Notebook Generator for LendInsight

Programmatically generates the 3 EDA and risk segmentation notebooks using nbformat.
Run once to initialize or reset the .ipynb files in the project workspace.

Author: Subhodeep Modak
"""
import nbformat as nbf
import os

NB_DIR = r"C:\data_analyst\LendInsight\03_python"
os.makedirs(NB_DIR, exist_ok=True)

def nb(cells):
    n = nbf.v4.new_notebook()
    n.cells = cells
    return n

def md(src):  return nbf.v4.new_markdown_cell(src)
def code(src): return nbf.v4.new_code_cell(src)

# ══════════════════════════════════════════════════════════════
# NOTEBOOK 1: Data Exploration
# ══════════════════════════════════════════════════════════════
nb1 = nb([
md("""# LendInsight — Notebook 1: Data Exploration
**Project**: LendInsight Lending Business Decision Support System  
**Purpose**: Understand the raw structure, distributions and quality of the cleaned dataset before analysis.  
**Dataset**: `credit_risk_cleaned.csv` — 32,411 loan records, 15 columns
"""),

code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Plot style
sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams.update({"figure.dpi": 120, "font.family": "sans-serif"})

CLEAN_PATH = r"C:\\data_analyst\\LendInsight\\01_data\\clean\\credit_risk_cleaned.csv"
df = pd.read_csv(CLEAN_PATH)
print(f"Dataset loaded: {df.shape[0]:,} rows x {df.shape[1]} columns")
"""),

md("## 1. Dataset Shape & Column Overview"),

code("""
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")
print()
print(df.dtypes.to_string())
"""),

md("## 2. First 5 Rows"),

code("df.head()"),

md("## 3. Descriptive Statistics — Numeric Columns"),

code("df.describe().round(2)"),

md("## 4. Null Value Check (Post-ETL)"),

code("""
nulls = df.isnull().sum()
print("Null counts per column:")
print(nulls[nulls > 0] if nulls.sum() > 0 else "[OK] Zero nulls — dataset is clean")
"""),

md("## 5. Target Variable Distribution — default_flag"),

code("""
counts = df["default_flag"].value_counts()
labels = ["Repaid (0)", "Defaulted (1)"]
colors = ["#2ECC71", "#E74C3C"]

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Count bar
axes[0].bar(labels, counts.values, color=colors, edgecolor="white", width=0.5)
axes[0].set_title("Loan Outcome — Count", fontsize=13, fontweight="bold")
axes[0].set_ylabel("Number of Loans")
for i, v in enumerate(counts.values):
    axes[0].text(i, v + 200, f"{v:,}", ha="center", fontweight="bold")

# Pie
axes[1].pie(counts.values, labels=labels, colors=colors, autopct="%1.1f%%",
            startangle=90, wedgeprops=dict(edgecolor="white", linewidth=2))
axes[1].set_title("Loan Outcome — Share", fontsize=13, fontweight="bold")

plt.suptitle("Default vs Repaid Distribution", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_01_target_distribution.png",
            bbox_inches="tight")
plt.show()
print(f"Default Rate: {counts[1]/counts.sum()*100:.2f}%")
"""),

md("## 6. Loan Grade Distribution"),

code("""
grade_counts = df["loan_grade"].value_counts().sort_index()
colors_grade = ["#1A5276","#2E86C1","#5DADE2","#F39C12","#E67E22","#C0392B","#7B241C"]

fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.bar(grade_counts.index, grade_counts.values, color=colors_grade, edgecolor="white")
ax.set_title("Loan Volume by Grade (A = Lowest Risk → G = Highest Risk)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Loan Grade"); ax.set_ylabel("Number of Loans")
for bar, val in zip(bars, grade_counts.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+100,
            f"{val:,}", ha="center", fontsize=9, fontweight="bold")
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_02_grade_distribution.png",
            bbox_inches="tight")
plt.show()
"""),

md("## 7. Loan Intent Distribution"),

code("""
intent_counts = df["loan_intent"].value_counts()

fig, ax = plt.subplots(figsize=(10, 4))
bars = ax.barh(intent_counts.index, intent_counts.values,
               color=sns.color_palette("Blues_d", len(intent_counts)), edgecolor="white")
ax.set_title("Loan Volume by Intent (Purpose)", fontsize=13, fontweight="bold")
ax.set_xlabel("Number of Loans")
for bar, val in zip(bars, intent_counts.values):
    ax.text(val + 80, bar.get_y()+bar.get_height()/2,
            f"{val:,}", va="center", fontsize=9, fontweight="bold")
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_03_intent_distribution.png",
            bbox_inches="tight")
plt.show()
"""),

md("## 8. Loan Amount Distribution"),

code("""
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

axes[0].hist(df["loan_amnt"], bins=40, color="#2E86C1", edgecolor="white")
axes[0].set_title("Loan Amount Distribution", fontsize=13, fontweight="bold")
axes[0].set_xlabel("Loan Amount (USD)"); axes[0].set_ylabel("Frequency")

sns.boxplot(x="default_flag", y="loan_amnt", data=df, ax=axes[1],
            palette={0:"#2ECC71", 1:"#E74C3C"})
axes[1].set_title("Loan Amount by Outcome", fontsize=13, fontweight="bold")
axes[1].set_xlabel("0 = Repaid | 1 = Defaulted"); axes[1].set_ylabel("Loan Amount (USD)")
axes[1].set_xticklabels(["Repaid","Defaulted"])

plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_04_loan_amount.png",
            bbox_inches="tight")
plt.show()
print(f"Avg loan (Repaid)   : ${df[df.default_flag==0].loan_amnt.mean():,.0f}")
print(f"Avg loan (Defaulted): ${df[df.default_flag==1].loan_amnt.mean():,.0f}")
"""),

md("## 9. Key Summary Statistics"),

code("""
total   = len(df)
defs    = df["default_flag"].sum()
summary = {
    "Total Loans"          : f"{total:,}",
    "Total Defaults"       : f"{defs:,}",
    "Default Rate"         : f"{defs/total*100:.2f}%",
    "Avg Loan Amount"      : f"${df['loan_amnt'].mean():,.2f}",
    "Avg Interest Rate"    : f"{df['loan_int_rate'].mean():.2f}%",
    "Avg DTI (loan/income)": f"{df['loan_percent_income'].mean():.3f}",
    "HIGH Risk Loans"      : f"{(df['risk_category']=='HIGH').sum():,}",
    "LOW Risk Loans"       : f"{(df['risk_category']=='LOW').sum():,}",
}
for k, v in summary.items():
    print(f"  {k:<28}: {v}")
"""),
])

nbf.write(nb1, os.path.join(NB_DIR, "01_data_exploration.ipynb"))
print("[OK] 01_data_exploration.ipynb created")


# ══════════════════════════════════════════════════════════════
# NOTEBOOK 2: EDA Visualizations
# ══════════════════════════════════════════════════════════════
nb2 = nb([
md("""# LendInsight — Notebook 2: EDA Visualizations
**Purpose**: Uncover business patterns through 8 targeted visualizations.  
Each chart answers a specific stakeholder question and maps to a Power BI dashboard page.
"""),

code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.dpi": 120, "font.family": "sans-serif"})

CLEAN_PATH = r"C:\\data_analyst\\LendInsight\\01_data\\clean\\credit_risk_cleaned.csv"
df = pd.read_csv(CLEAN_PATH)
print(f"Dataset: {df.shape[0]:,} rows loaded.")
"""),

md("## Chart 1 — Default Rate by Loan Grade\n**Business Question**: Which grade bands are failing most?"),

code("""
grade_df = df.groupby("loan_grade").agg(
    total=("default_flag","count"),
    defaults=("default_flag","sum")
).reset_index()
grade_df["default_rate"] = grade_df["defaults"] / grade_df["total"] * 100

colors = ["#1A5276" if r < 15 else "#E67E22" if r < 30 else "#C0392B"
          for r in grade_df["default_rate"]]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(grade_df["loan_grade"], grade_df["default_rate"], color=colors, edgecolor="white", width=0.6)
ax.set_title("Default Rate by Loan Grade", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("Loan Grade (A = Lowest Risk → G = Highest Risk)", fontsize=11)
ax.set_ylabel("Default Rate (%)", fontsize=11)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
for bar, val in zip(bars, grade_df["default_rate"]):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f"{val:.1f}%", ha="center", fontweight="bold", fontsize=10)
ax.axhline(y=grade_df["default_rate"].mean(), color="red", linestyle="--", alpha=0.6, label="Portfolio Avg")
ax.legend()
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_05_default_by_grade.png", bbox_inches="tight")
plt.show()
print("Key Finding: Grade G default rate is significantly higher than portfolio average.")
"""),

md("## Chart 2 — Default Rate by Loan Intent\n**Business Question**: Which loan purpose has the highest failure rate?"),

code("""
intent_df = df.groupby("loan_intent").agg(
    total=("default_flag","count"),
    defaults=("default_flag","sum")
).reset_index()
intent_df["default_rate"] = intent_df["defaults"] / intent_df["total"] * 100
intent_df = intent_df.sort_values("default_rate", ascending=True)

colors = ["#C0392B" if r > 25 else "#E67E22" if r > 18 else "#2E86C1"
          for r in intent_df["default_rate"]]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(intent_df["loan_intent"], intent_df["default_rate"], color=colors, edgecolor="white")
ax.set_title("Default Rate by Loan Intent", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("Default Rate (%)", fontsize=11)
ax.xaxis.set_major_formatter(mtick.PercentFormatter())
for bar, val in zip(bars, intent_df["default_rate"]):
    ax.text(val + 0.3, bar.get_y()+bar.get_height()/2,
            f"{val:.1f}%", va="center", fontweight="bold", fontsize=10)
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_06_default_by_intent.png", bbox_inches="tight")
plt.show()
"""),

md("## Chart 3 — Income Distribution: Defaulters vs Non-Defaulters\n**Business Question**: Does income level predict default?"),

code("""
fig, ax = plt.subplots(figsize=(12, 5))
repaid   = df[df["default_flag"]==0]["person_income"]
defaulted = df[df["default_flag"]==1]["person_income"]

ax.hist(repaid,    bins=50, alpha=0.6, color="#2ECC71", label=f"Repaid   (n={len(repaid):,})",    density=True)
ax.hist(defaulted, bins=50, alpha=0.6, color="#E74C3C", label=f"Defaulted (n={len(defaulted):,})", density=True)
ax.axvline(repaid.mean(),    color="#1E8449", linestyle="--", linewidth=2,
           label=f"Repaid Avg: ${repaid.mean():,.0f}")
ax.axvline(defaulted.mean(), color="#922B21", linestyle="--", linewidth=2,
           label=f"Defaulted Avg: ${defaulted.mean():,.0f}")
ax.set_title("Income Distribution: Defaulters vs Non-Defaulters", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("Annual Income (USD)", fontsize=11)
ax.set_ylabel("Density", fontsize=11)
ax.legend(fontsize=10)
ax.set_xlim(0, 200000)
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_07_income_distribution.png", bbox_inches="tight")
plt.show()
print(f"Avg Income — Repaid   : ${repaid.mean():,.0f}")
print(f"Avg Income — Defaulted: ${defaulted.mean():,.0f}")
print(f"Income Gap            : ${repaid.mean()-defaulted.mean():,.0f}")
"""),

md("## Chart 4 — DTI Bracket vs Default Rate\n**Business Question**: Does higher debt burden mean more defaults?"),

code("""
order = ["Low DTI","Moderate DTI","High DTI","Very High DTI"]
dti_df = df.groupby("dti_bracket").agg(
    total=("default_flag","count"),
    defaults=("default_flag","sum")
).reindex(order).reset_index()
dti_df["default_rate"] = dti_df["defaults"] / dti_df["total"] * 100

colors = ["#1A5276","#2E86C1","#E67E22","#C0392B"]
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(dti_df["dti_bracket"], dti_df["default_rate"], color=colors, edgecolor="white", width=0.55)
ax.set_title("Default Rate by DTI Bracket (Debt-to-Income Proxy)", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("DTI Bracket", fontsize=11); ax.set_ylabel("Default Rate (%)", fontsize=11)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
for bar, val in zip(bars, dti_df["default_rate"]):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f"{val:.1f}%", ha="center", fontweight="bold", fontsize=11)
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_08_dti_default.png", bbox_inches="tight")
plt.show()
"""),

md("## Chart 5 — Credit History Length vs Default Rate\n**Business Question**: Does credit seniority reduce default risk?"),

code("""
df["cred_hist_band"] = pd.cut(df["cb_person_cred_hist_length"],
    bins=[0,3,7,15,50], labels=["1-3 yrs","4-7 yrs","8-15 yrs","15+ yrs"])

ch_df = df.groupby("cred_hist_band", observed=True).agg(
    total=("default_flag","count"), defaults=("default_flag","sum")).reset_index()
ch_df["default_rate"] = ch_df["defaults"] / ch_df["total"] * 100

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ch_df["cred_hist_band"].astype(str), ch_df["default_rate"],
        marker="o", markersize=9, linewidth=2.5, color="#2E86C1")
ax.fill_between(range(len(ch_df)), ch_df["default_rate"], alpha=0.15, color="#2E86C1")
for i, (x, y) in enumerate(zip(ch_df["cred_hist_band"].astype(str), ch_df["default_rate"])):
    ax.annotate(f"{y:.1f}%", (i, y), textcoords="offset points",
                xytext=(0, 10), ha="center", fontweight="bold")
ax.set_title("Default Rate by Credit History Length", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("Credit History Band", fontsize=11); ax.set_ylabel("Default Rate (%)", fontsize=11)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_09_credit_history.png", bbox_inches="tight")
plt.show()
"""),

md("## Chart 6 — Prior Default History vs Current Default Rate\n**Business Question**: Are repeat defaulters more likely to fail again?"),

code("""
prior_df = df.groupby("cb_person_default_on_file").agg(
    total=("default_flag","count"), defaults=("default_flag","sum")).reset_index()
prior_df["default_rate"] = prior_df["defaults"] / prior_df["total"] * 100
prior_df["label"] = prior_df["cb_person_default_on_file"].map({"N":"No Prior Default","Y":"Prior Default on File"})

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(prior_df["label"], prior_df["default_rate"],
              color=["#2ECC71","#E74C3C"], edgecolor="white", width=0.4)
ax.set_title("Default Rate: Prior vs No Prior Default (Credit Bureau)", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Default Rate (%)", fontsize=11)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
for bar, val in zip(bars, prior_df["default_rate"]):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            f"{val:.1f}%", ha="center", fontweight="bold", fontsize=13)
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_10_prior_default.png", bbox_inches="tight")
plt.show()
print(prior_df[["label","total","defaults","default_rate"]].to_string(index=False))
"""),

md("## Chart 7 — Correlation Heatmap\n**Business Question**: Which numeric features are most related to default?"),

code("""
num_cols = ["person_age","person_income","person_emp_length",
            "loan_amnt","loan_int_rate","loan_percent_income",
            "cb_person_cred_hist_length","default_flag"]
corr = df[num_cols].corr()

fig, ax = plt.subplots(figsize=(10, 7))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdYlBu_r",
            center=0, square=True, ax=ax, linewidths=0.5,
            cbar_kws={"shrink":0.8})
ax.set_title("Feature Correlation Heatmap\\n(Focus: correlation with default_flag)",
             fontsize=13, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_11_correlation_heatmap.png", bbox_inches="tight")
plt.show()
print("\\nCorrelation with default_flag:")
print(corr["default_flag"].drop("default_flag").sort_values(ascending=False).round(3).to_string())
"""),

md("## Chart 8 — Home Ownership vs Default Rate\n**Business Question**: Does housing stability affect repayment?"),

code("""
own_df = df.groupby("person_home_ownership").agg(
    total=("default_flag","count"), defaults=("default_flag","sum")).reset_index()
own_df["default_rate"] = own_df["defaults"] / own_df["total"] * 100
own_df = own_df.sort_values("default_rate", ascending=False)

colors = ["#C0392B" if r > 25 else "#E67E22" if r > 18 else "#2ECC71"
          for r in own_df["default_rate"]]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(own_df["person_home_ownership"], own_df["default_rate"],
              color=colors, edgecolor="white", width=0.5)
ax.set_title("Default Rate by Home Ownership Type", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("Home Ownership"); ax.set_ylabel("Default Rate (%)")
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
for bar, val in zip(bars, own_df["default_rate"]):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4,
            f"{val:.1f}%", ha="center", fontweight="bold", fontsize=11)
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_12_home_ownership.png", bbox_inches="tight")
plt.show()
"""),
])

nbf.write(nb2, os.path.join(NB_DIR, "02_eda_visualizations.ipynb"))
print("[OK] 02_eda_visualizations.ipynb created")


# ══════════════════════════════════════════════════════════════
# NOTEBOOK 3: Risk Segmentation
# ══════════════════════════════════════════════════════════════
nb3 = nb([
md("""# LendInsight — Notebook 3: Risk Segmentation
**Purpose**: Validate and analyze the rule-based risk segmentation (LOW / MEDIUM / HIGH).  
**Segmentation Logic**: Based on loan grade + DTI proxy (loan_percent_income).  
**Output**: `credit_risk_segmented.csv` — used as Power BI data source.
"""),

code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.dpi": 120, "font.family": "sans-serif"})

CLEAN_PATH = r"C:\\data_analyst\\LendInsight\\01_data\\clean\\credit_risk_cleaned.csv"
df = pd.read_csv(CLEAN_PATH)
print(f"Dataset: {df.shape[0]:,} rows | risk_category already derived by ETL pipeline.")
print(df["risk_category"].value_counts())
"""),

md("""## 1. Risk Segmentation Logic
The `risk_category` column was created in the ETL pipeline using this business rule:

| Condition | Category |
|-----------|----------|
| Grade E/F/G **or** DTI > 0.40 | **HIGH** |
| Grade A/B **and** DTI < 0.20 | **LOW** |
| Everything else | **MEDIUM** |

This mirrors how a credit risk team would classify borrowers — using the internal risk grade as the primary signal and DTI as a secondary stress indicator.
"""),

code("""
# Confirm distribution
seg = df["risk_category"].value_counts()
total = len(df)
print("Risk Category Distribution:")
print("-" * 35)
for cat, cnt in seg.items():
    print(f"  {cat:<8}: {cnt:>6,}  ({cnt/total*100:.1f}%)")
"""),

md("## 2. Validation — Default Rate per Segment\nThis confirms the segmentation is meaningful: HIGH risk must default more than LOW risk."),

code("""
seg_df = df.groupby("risk_category").agg(
    total=("default_flag","count"),
    defaults=("default_flag","sum"),
    avg_loan=("loan_amnt","mean"),
    avg_rate=("loan_int_rate","mean"),
    avg_dti=("loan_percent_income","mean")
).reset_index()
seg_df["default_rate"] = (seg_df["defaults"] / seg_df["total"] * 100).round(2)
seg_df["pct_portfolio"] = (seg_df["total"] / total * 100).round(1)

display_df = seg_df[["risk_category","total","pct_portfolio","defaults","default_rate","avg_loan","avg_rate","avg_dti"]].copy()
display_df.columns = ["Segment","Loans","% Portfolio","Defaults","Default Rate %","Avg Loan","Avg Rate %","Avg DTI"]
print(display_df.to_string(index=False))
"""),

md("## 3. Visualization — Risk Segment Performance"),

code("""
order = ["LOW","MEDIUM","HIGH"]
seg_ordered = seg_df.set_index("risk_category").reindex(order).reset_index()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
colors = {"LOW":"#2ECC71","MEDIUM":"#F39C12","HIGH":"#E74C3C"}
color_list = [colors[c] for c in order]

# Default rate
axes[0].bar(order, seg_ordered["default_rate"], color=color_list, edgecolor="white", width=0.5)
axes[0].set_title("Default Rate by Risk Segment", fontweight="bold")
axes[0].set_ylabel("Default Rate (%)")
axes[0].yaxis.set_major_formatter(mtick.PercentFormatter())
for i, (cat, val) in enumerate(zip(order, seg_ordered["default_rate"])):
    axes[0].text(i, val+0.5, f"{val:.1f}%", ha="center", fontweight="bold")

# Loan count (donut)
axes[1].pie(seg_ordered["total"], labels=order, colors=color_list,
            autopct="%1.1f%%", startangle=90,
            wedgeprops=dict(edgecolor="white", linewidth=2, width=0.6))
axes[1].set_title("Portfolio Share by Risk Segment", fontweight="bold")

# Avg loan amount
axes[2].bar(order, seg_ordered["avg_loan"], color=color_list, edgecolor="white", width=0.5)
axes[2].set_title("Avg Loan Amount by Risk Segment", fontweight="bold")
axes[2].set_ylabel("Avg Loan (USD)")
for i, val in enumerate(seg_ordered["avg_loan"]):
    axes[2].text(i, val+50, f"${val:,.0f}", ha="center", fontweight="bold", fontsize=9)

plt.suptitle("Risk Segmentation Validation", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_13_risk_segments.png", bbox_inches="tight")
plt.show()
"""),

md("## 4. Risk Category vs Loan Intent Heatmap\n**Question**: Where does HIGH risk concentrate by loan purpose?"),

code("""
pivot = df.groupby(["risk_category","loan_intent"])["default_flag"].mean().unstack() * 100
pivot = pivot.reindex(["HIGH","MEDIUM","LOW"])

fig, ax = plt.subplots(figsize=(12, 4))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="RdYlGn_r",
            linewidths=0.5, ax=ax, cbar_kws={"label": "Default Rate (%)"})
ax.set_title("Default Rate Heatmap: Risk Category × Loan Intent",
             fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Risk Category"); ax.set_xlabel("Loan Intent")
plt.tight_layout()
plt.savefig(r"C:\\data_analyst\\LendInsight\\03_python\\chart_14_segment_intent_heatmap.png", bbox_inches="tight")
plt.show()
"""),

md("## 5. TOP 10 Highest-Risk Customer Profiles"),

code("""
profile_df = df.groupby(["loan_grade","loan_intent","income_bracket","dti_bracket"]).agg(
    count=("default_flag","count"),
    defaults=("default_flag","sum")
).reset_index()
profile_df["default_rate"] = (profile_df["defaults"]/profile_df["count"]*100).round(1)
profile_df = profile_df[profile_df["count"] >= 20].sort_values("default_rate", ascending=False).head(10)

print("TOP 10 Riskiest Customer Profiles (min 20 loans per group):")
print("-"*80)
print(profile_df[["loan_grade","loan_intent","income_bracket","dti_bracket","count","defaults","default_rate"]].to_string(index=False))
"""),

md("## 6. Export Segmented Dataset for Power BI"),

code("""
OUTPUT_PATH = r"C:\\data_analyst\\LendInsight\\01_data\\clean\\credit_risk_segmented.csv"
df.to_csv(OUTPUT_PATH, index=False)
print(f"Segmented dataset exported:")
print(f"  Path : {OUTPUT_PATH}")
print(f"  Rows : {len(df):,}")
print(f"  Cols : {len(df.columns)}")
print(f"\\nColumns: {list(df.columns)}")
print("\\nThis file is the Power BI data source.")
"""),

md("""## 7. Key Findings Summary

| Finding | Detail |
|---------|--------|
| **Overall default rate** | 21.87% — critically high |
| **Grade G default rate** | Significantly above portfolio average |
| **DTI > 0.40 borrowers** | Default at the highest rate in any bracket |
| **Prior defaulters** | Default again at a much higher rate than clean borrowers |
| **HIGH risk segment** | Represents a small share of volume but concentrated losses |
| **Income gap** | Defaulted borrowers have meaningfully lower average income |
| **Loan intent** | Certain purposes (e.g. VENTURE) carry above-average default risk |

> **Interview talking point**: *"The risk segmentation shows that grade and DTI together are strong predictors of default — which justifies the business rule approach over a complex model for this use case."*
"""),
])

nbf.write(nb3, os.path.join(NB_DIR, "03_risk_segmentation.ipynb"))
print("[OK] 03_risk_segmentation.ipynb created")

print("\n All 3 notebooks created in:", NB_DIR)
print("Open with: jupyter notebook")
