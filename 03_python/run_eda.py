"""
Exploratory Data Analysis (EDA) & Visualization Suite for LendInsight

Executes statistical correlation analysis, generates the 10 core business figures,
and exports the segmented dataset for Power BI reporting.

Author: Subhodeep Modak
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings, os
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.dpi": 120, "font.family": "sans-serif"})

CLEAN_PATH = r"C:\data_analyst\LendInsight\01_data\clean\credit_risk_cleaned.csv"
OUT_DIR    = r"C:\data_analyst\LendInsight\03_python\charts"
os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CLEAN_PATH)
total = len(df)
print(f"Loaded {total:,} rows")

def save(name):
    path = os.path.join(OUT_DIR, name)
    plt.savefig(path, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"  Saved: {name}")

# ── Chart 1: Target Distribution ────────────────────────────
counts = df["default_flag"].value_counts()
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].bar(["Repaid","Defaulted"], counts.values, color=["#2ECC71","#E74C3C"], edgecolor="white", width=0.5)
axes[0].set_title("Loan Outcome — Count", fontsize=13, fontweight="bold")
axes[0].set_ylabel("Number of Loans")
for i, v in enumerate(counts.values):
    axes[0].text(i, v+200, f"{v:,}", ha="center", fontweight="bold")
axes[1].pie(counts.values, labels=["Repaid","Defaulted"], colors=["#2ECC71","#E74C3C"],
            autopct="%1.1f%%", startangle=90, wedgeprops=dict(edgecolor="white", linewidth=2))
axes[1].set_title("Loan Outcome — Share", fontsize=13, fontweight="bold")
plt.suptitle("Default vs Repaid Distribution", fontsize=15, fontweight="bold")
plt.tight_layout(); save("01_target_distribution.png")

# ── Chart 2: Default Rate by Loan Grade ─────────────────────
grade_df = df.groupby("loan_grade").agg(total=("default_flag","count"), defaults=("default_flag","sum")).reset_index()
grade_df["dr"] = grade_df["defaults"] / grade_df["total"] * 100
colors = ["#1A5276" if r < 15 else "#E67E22" if r < 30 else "#C0392B" for r in grade_df["dr"]]
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(grade_df["loan_grade"], grade_df["dr"], color=colors, edgecolor="white", width=0.6)
ax.set_title("Default Rate by Loan Grade", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Loan Grade (A = Lowest Risk  to  G = Highest Risk)", fontsize=11)
ax.set_ylabel("Default Rate (%)"); ax.yaxis.set_major_formatter(mtick.PercentFormatter())
avg_dr = grade_df["dr"].mean()
ax.axhline(y=avg_dr, color="red", linestyle="--", alpha=0.6, label=f"Portfolio Avg ({avg_dr:.1f}%)")
ax.legend()
for bar, val in zip(bars, grade_df["dr"]):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f"{val:.1f}%", ha="center", fontweight="bold")
plt.tight_layout(); save("02_default_by_grade.png")

# ── Chart 3: Default Rate by Loan Intent ────────────────────
intent_df = df.groupby("loan_intent").agg(total=("default_flag","count"), defaults=("default_flag","sum")).reset_index()
intent_df["dr"] = intent_df["defaults"] / intent_df["total"] * 100
intent_df = intent_df.sort_values("dr", ascending=True)
colors = ["#C0392B" if r > 25 else "#E67E22" if r > 18 else "#2E86C1" for r in intent_df["dr"]]
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(intent_df["loan_intent"], intent_df["dr"], color=colors, edgecolor="white")
ax.set_title("Default Rate by Loan Intent", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Default Rate (%)"); ax.xaxis.set_major_formatter(mtick.PercentFormatter())
for bar, val in zip(bars, intent_df["dr"]):
    ax.text(val+0.3, bar.get_y()+bar.get_height()/2, f"{val:.1f}%", va="center", fontweight="bold")
plt.tight_layout(); save("03_default_by_intent.png")

# ── Chart 4: Income Distribution ────────────────────────────
repaid    = df[df["default_flag"]==0]["person_income"]
defaulted = df[df["default_flag"]==1]["person_income"]
fig, ax = plt.subplots(figsize=(12, 5))
ax.hist(repaid,    bins=50, alpha=0.6, color="#2ECC71", label=f"Repaid (n={len(repaid):,})",    density=True)
ax.hist(defaulted, bins=50, alpha=0.6, color="#E74C3C", label=f"Defaulted (n={len(defaulted):,})", density=True)
ax.axvline(repaid.mean(),    color="#1E8449", linestyle="--", lw=2, label=f"Repaid Avg: ${repaid.mean():,.0f}")
ax.axvline(defaulted.mean(), color="#922B21", linestyle="--", lw=2, label=f"Defaulted Avg: ${defaulted.mean():,.0f}")
ax.set_title("Income Distribution: Defaulters vs Non-Defaulters", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Annual Income (USD)"); ax.set_ylabel("Density"); ax.set_xlim(0,200000); ax.legend()
plt.tight_layout(); save("04_income_distribution.png")

# ── Chart 5: DTI Bracket vs Default Rate ────────────────────
order = ["Low DTI","Moderate DTI","High DTI","Very High DTI"]
dti_df = df.groupby("dti_bracket").agg(total=("default_flag","count"), defaults=("default_flag","sum")).reindex(order).reset_index()
dti_df["dr"] = dti_df["defaults"] / dti_df["total"] * 100
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(dti_df["dti_bracket"], dti_df["dr"], color=["#1A5276","#2E86C1","#E67E22","#C0392B"], edgecolor="white", width=0.55)
ax.set_title("Default Rate by DTI Bracket", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("DTI Bracket"); ax.set_ylabel("Default Rate (%)"); ax.yaxis.set_major_formatter(mtick.PercentFormatter())
for bar, val in zip(bars, dti_df["dr"]):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f"{val:.1f}%", ha="center", fontweight="bold", fontsize=11)
plt.tight_layout(); save("05_dti_default_rate.png")

# ── Chart 6: Credit History vs Default Rate ─────────────────
df["cred_band"] = pd.cut(df["cb_person_cred_hist_length"], bins=[0,3,7,15,50], labels=["1-3 yrs","4-7 yrs","8-15 yrs","15+ yrs"])
ch_df = df.groupby("cred_band", observed=True).agg(total=("default_flag","count"), defaults=("default_flag","sum")).reset_index()
ch_df["dr"] = ch_df["defaults"] / ch_df["total"] * 100
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ch_df["cred_band"].astype(str), ch_df["dr"], marker="o", markersize=9, lw=2.5, color="#2E86C1")
ax.fill_between(range(len(ch_df)), ch_df["dr"], alpha=0.15, color="#2E86C1")
for i, (x, y) in enumerate(zip(ch_df["cred_band"].astype(str), ch_df["dr"])):
    ax.annotate(f"{y:.1f}%", (i, y), textcoords="offset points", xytext=(0,10), ha="center", fontweight="bold")
ax.set_title("Default Rate by Credit History Length", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Credit History Band"); ax.set_ylabel("Default Rate (%)"); ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.tight_layout(); save("06_credit_history_default.png")

# ── Chart 7: Prior Default Flag ─────────────────────────────
prior_df = df.groupby("cb_person_default_on_file").agg(total=("default_flag","count"), defaults=("default_flag","sum")).reset_index()
prior_df["dr"] = prior_df["defaults"] / prior_df["total"] * 100
prior_df["label"] = prior_df["cb_person_default_on_file"].map({"N":"No Prior Default","Y":"Prior Default on File"})
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(prior_df["label"], prior_df["dr"], color=["#2ECC71","#E74C3C"], edgecolor="white", width=0.4)
ax.set_title("Default Rate: Prior vs No Prior Default (Credit Bureau)", fontsize=14, fontweight="bold", pad=12)
ax.set_ylabel("Default Rate (%)"); ax.yaxis.set_major_formatter(mtick.PercentFormatter())
for bar, val in zip(bars, prior_df["dr"]):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.4, f"{val:.1f}%", ha="center", fontweight="bold", fontsize=13)
plt.tight_layout(); save("07_prior_default_flag.png")

# ── Chart 8: Correlation Heatmap ────────────────────────────
num_cols = ["person_age","person_income","person_emp_length","loan_amnt","loan_int_rate","loan_percent_income","cb_person_cred_hist_length","default_flag"]
corr = df[num_cols].corr()
fig, ax = plt.subplots(figsize=(10, 7))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdYlBu_r", center=0, square=True, ax=ax, linewidths=0.5, cbar_kws={"shrink":0.8})
ax.set_title("Feature Correlation Heatmap\n(Key: correlation with default_flag)", fontsize=13, fontweight="bold", pad=12)
plt.tight_layout(); save("08_correlation_heatmap.png")

# ── Chart 9: Risk Segment Performance ───────────────────────
order3 = ["LOW","MEDIUM","HIGH"]
seg_df = df.groupby("risk_category").agg(total=("default_flag","count"), defaults=("default_flag","sum"), avg_loan=("loan_amnt","mean")).reindex(order3).reset_index()
seg_df["dr"] = seg_df["defaults"] / seg_df["total"] * 100
col3 = {"LOW":"#2ECC71","MEDIUM":"#F39C12","HIGH":"#E74C3C"}
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# Default rate bar
axes[0].bar(order3, seg_df["dr"], color=[col3[c] for c in order3], edgecolor="white", width=0.5)
axes[0].set_title("Default Rate by Risk Segment", fontweight="bold"); axes[0].set_ylabel("Default Rate (%)")
axes[0].yaxis.set_major_formatter(mtick.PercentFormatter())
for i, val in enumerate(seg_df["dr"]): axes[0].text(i, val+0.5, f"{val:.1f}%", ha="center", fontweight="bold")
# Donut
axes[1].pie(seg_df["total"], labels=order3, colors=[col3[c] for c in order3], autopct="%1.1f%%", startangle=90, wedgeprops=dict(edgecolor="white", linewidth=2, width=0.6))
axes[1].set_title("Portfolio Share by Risk Segment", fontweight="bold")
# Avg loan
axes[2].bar(order3, seg_df["avg_loan"], color=[col3[c] for c in order3], edgecolor="white", width=0.5)
axes[2].set_title("Avg Loan Amount by Risk Segment", fontweight="bold"); axes[2].set_ylabel("Avg Loan (USD)")
for i, val in enumerate(seg_df["avg_loan"]): axes[2].text(i, val+50, f"${val:,.0f}", ha="center", fontweight="bold", fontsize=9)
plt.suptitle("Risk Segmentation Validation", fontsize=15, fontweight="bold", y=1.02)
plt.tight_layout(); save("09_risk_segments.png")

# ── Chart 10: Segment x Intent Heatmap ──────────────────────
pivot = df.groupby(["risk_category","loan_intent"])["default_flag"].mean().unstack() * 100
pivot = pivot.reindex(["HIGH","MEDIUM","LOW"])
fig, ax = plt.subplots(figsize=(12, 4))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="RdYlGn_r", linewidths=0.5, ax=ax, cbar_kws={"label":"Default Rate (%)"})
ax.set_title("Default Rate Heatmap: Risk Category x Loan Intent", fontsize=14, fontweight="bold", pad=12)
plt.tight_layout(); save("10_segment_intent_heatmap.png")

# ── Export segmented CSV for Power BI ────────────────────────
seg_out = r"C:\data_analyst\LendInsight\01_data\clean\credit_risk_segmented.csv"
df.to_csv(seg_out, index=False)
print(f"\nSegmented CSV exported: {seg_out}")

print(f"\nAll charts saved to: {OUT_DIR}")
print(f"Total charts: 10")
print("\nKey Findings:")
dr = df["default_flag"].mean()*100
print(f"  Overall Default Rate      : {dr:.2f}%")
print(f"  HIGH segment default rate : {df[df.risk_category=='HIGH']['default_flag'].mean()*100:.2f}%")
print(f"  LOW segment default rate  : {df[df.risk_category=='LOW']['default_flag'].mean()*100:.2f}%")
print(f"  Income gap (repaid vs def): ${repaid.mean()-defaulted.mean():,.0f}")
