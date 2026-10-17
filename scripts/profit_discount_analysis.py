"""Profit and discount charts: profit by sub-category, discount vs profit,
and top / bottom 10 products by profit.

Reads data/processed/superstore_clean.csv and writes PNGs to reports/charts/.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "data" / "processed" / "superstore_clean.csv"
CHART_DIR = ROOT / "reports" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

GAIN, LOSS, INK, GRID = "#2a6fdb", "#d9531e", "#222222", "#dddddd"

plt.rcParams.update({
    "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "axes.spines.top": False,
    "axes.spines.right": False,
})

df = pd.read_csv(CSV_FILE)


def colours(values):
    return [GAIN if v >= 0 else LOSS for v in values]


# 1. Profit by sub-category -------------------------------------------------
sub = df.groupby("sub_category")["profit"].sum().sort_values()
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(sub.index, sub.values, color=colours(sub.values))
ax.axvline(0, color=INK, linewidth=0.8)
ax.set_title("Profit by sub-category (orange = loss-making)", loc="left")
ax.set_xlabel("Total profit")
ax.xaxis.grid(True, color=GRID)
ax.set_axisbelow(True)
for y, v in enumerate(sub.values):
    ax.text(v + (2500 if v >= 0 else -2500), y, f"{v:,.0f}", va="center",
            ha="left" if v >= 0 else "right", fontsize=8)
ax.margins(x=0.12)
fig.tight_layout()
fig.savefig(CHART_DIR / "profit_by_subcategory.png", dpi=150)
plt.close(fig)

# 2. Discount vs profit ---------------------------------------------------
bins = [-0.001, 0, 0.10, 0.20, 0.30, 0.50, 1.0]
labels = ["0%", "1-10%", "11-20%", "21-30%", "31-50%", "50%+"]
df["discount_band"] = pd.cut(df["discount"], bins=bins, labels=labels)
band = (df.groupby("discount_band", observed=True)
        .agg(profit=("profit", "sum"), sales=("sales", "sum"),
             rows=("profit", "size")))
band["margin"] = band["profit"] / band["sales"] * 100
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(band.index.astype(str), band["profit"], color=colours(band["profit"]))
ax.axhline(0, color=INK, linewidth=0.8)
ax.set_title("Total profit by discount band", loc="left")
ax.set_xlabel("Discount applied")
ax.set_ylabel("Total profit")
ax.yaxis.grid(True, color=GRID)
ax.set_axisbelow(True)
for x, (p, m, n) in enumerate(zip(band["profit"], band["margin"], band["rows"])):
    ax.text(x, p + (6000 if p >= 0 else -6000), f"{p:,.0f}\n{m:.1f}% margin\n{n:,} rows",
            ha="center", va="bottom" if p >= 0 else "top", fontsize=8)
ax.margins(y=0.25)
fig.tight_layout()
fig.savefig(CHART_DIR / "profit_by_discount_band.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(df["discount"] * 100, df["profit"], s=8, alpha=0.35,
           color=colours(df["profit"]))
ax.axhline(0, color=INK, linewidth=0.8)
ax.set_title("Discount vs profit, every order line", loc="left")
ax.set_xlabel("Discount (%)")
ax.set_ylabel("Profit")
ax.grid(True, color=GRID)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(CHART_DIR / "discount_vs_profit.png", dpi=150)
plt.close(fig)

# 3. Top and bottom 10 products by profit ---------------------------------
prod = df.groupby("product_name")["profit"].sum().sort_values()
extremes = pd.concat([prod.head(10), prod.tail(10)])
names = [n if len(n) <= 42 else n[:41] + "…" for n in extremes.index]
fig, ax = plt.subplots(figsize=(10, 7))
ax.barh(names, extremes.values, color=colours(extremes.values))
ax.axvline(0, color=INK, linewidth=0.8)
ax.set_title("Bottom 10 and top 10 products by profit", loc="left")
ax.set_xlabel("Total profit")
ax.xaxis.grid(True, color=GRID)
ax.set_axisbelow(True)
for y, v in enumerate(extremes.values):
    ax.text(v + (150 if v >= 0 else -150), y, f"{v:,.0f}", va="center",
            ha="left" if v >= 0 else "right", fontsize=8)
ax.margins(x=0.12)
fig.tight_layout()
fig.savefig(CHART_DIR / "top_bottom_products.png", dpi=150)
plt.close(fig)

print("Charts saved in:", CHART_DIR)
