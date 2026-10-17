
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. Set project paths
# -----------------------------
ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    ROOT / "data" / "raw" / "Superstore_Sales_Analysis  (1).xlsx"
)
REPORT_DIR = ROOT / "reports"
CHART_DIR = REPORT_DIR / "charts"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Cleaned dataset not found: {INPUT_FILE}\n"
        "Run scripts/clean_data.py first."
    )


df = pd.read_excel(INPUT_FILE)

# Standardize column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

print("Dataset shape:", df.shape)
print("Available columns:", df.columns.tolist())


# -----------------------------
# 2. Detect dataset columns
# -----------------------------
def find_column(candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None

sales_col = find_column(["sales", "total_sales", "revenue"])
profit_col = find_column(["profit", "net_profit"])
date_col = find_column(["order_date", "date", "orderdate"])
category_col = find_column(["category", "product_category"])
product_col = find_column(["product_name", "product", "item_name"])
region_col = find_column(["region", "market_region"])
quantity_col = find_column(["quantity", "qty"])
order_id_col = find_column(["order_id", "orderid", "transaction_id"])

print("Dataset shape:", df.shape)
print("Available columns:", df.columns.tolist())

if sales_col is None:
    raise ValueError(
        "Sales column not found. Check the printed column names "
        "and update the sales_col candidates."
    )

df[sales_col] = pd.to_numeric(df[sales_col], errors="coerce")

if profit_col:
    df[profit_col] = pd.to_numeric(df[profit_col], errors="coerce")

if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

if quantity_col:
    df[quantity_col] = pd.to_numeric(
        df[quantity_col], errors="coerce"
    )

# -----------------------------
# 3. Calculate overall KPIs
# -----------------------------
total_sales = df[sales_col].sum()
total_orders = (
    df[order_id_col].nunique()
    if order_id_col else len(df)
)
average_order_value = (
    total_sales / total_orders if total_orders else 0
)

print("\n========== SALES KPIs ==========")
print(f"Total sales: {total_sales:,.2f}")
print(f"Order count: {total_orders:,}")
print(f"Average sales per order: {average_order_value:,.2f}")

if profit_col:
    total_profit = df[profit_col].sum()
    profit_margin = (
        total_profit / total_sales * 100
        if total_sales else 0
    )
    print(f"Total profit: {total_profit:,.2f}")
    print(f"Profit margin: {profit_margin:.2f}%")

# Save KPI summary
kpis = {
    "metric": [
        "Total Sales",
        "Order Count",
        "Average Sales per Order"
    ],
    "value": [
        total_sales,
        total_orders,
        average_order_value
    ]
}

if profit_col:
    kpis["metric"].extend(["Total Profit", "Profit Margin (%)"])
    kpis["value"].extend([total_profit, profit_margin])

pd.DataFrame(kpis).to_csv(
    REPORT_DIR / "kpi_summary.csv", index=False
)

# -----------------------------
# 4. Monthly sales trend
# -----------------------------
if date_col:
    dated_df = df.dropna(subset=[date_col]).copy()
    dated_df["month"] = (
        dated_df[date_col].dt.to_period("M").astype(str)
    )

    monthly_sales = (
        dated_df.groupby("month")[sales_col]
        .sum()
        .sort_index()
    )

    monthly_sales.to_csv(
        REPORT_DIR / "monthly_sales.csv",
        header=["sales"]
    )

    plt.figure(figsize=(12, 5))
    monthly_sales.plot(marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "monthly_sales.png", dpi=150)
    plt.close()

    print("\nMonthly sales:")
    print(monthly_sales)

# -----------------------------
# 5. Category analysis
# -----------------------------
if category_col:
    aggregations = {sales_col: "sum"}

    if profit_col:
        aggregations[profit_col] = "sum"

    category_summary = (
        df.groupby(category_col)
        .agg(aggregations)
        .sort_values(sales_col, ascending=False)
    )

    category_summary.to_csv(
        REPORT_DIR / "category_summary.csv"
    )

    print("\nCategory performance:")
    print(category_summary)

    category_summary[sales_col].plot(
        kind="bar", figsize=(9, 5)
    )
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "sales_by_category.png", dpi=150)
    plt.close()

# -----------------------------
# 6. Regional analysis
# -----------------------------
if region_col:
    aggregations = {sales_col: "sum"}

    if profit_col:
        aggregations[profit_col] = "sum"

    region_summary = (
        df.groupby(region_col)
        .agg(aggregations)
        .sort_values(sales_col, ascending=False)
    )

    region_summary.to_csv(
        REPORT_DIR / "region_summary.csv"
    )

    print("\nRegional performance:")
    print(region_summary)

# -----------------------------
# 7. Top 10 products
# -----------------------------
if product_col:
    top_products = (
        df.groupby(product_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    top_products.to_csv(
        REPORT_DIR / "top_10_products.csv",
        header=["sales"]
    )

    print("\nTop 10 products by sales:")
    print(top_products)

# -----------------------------
# 8. Quantity analysis
# -----------------------------
if quantity_col:
    print(
        "\nTotal quantity sold:",
        f"{df[quantity_col].sum():,.0f}"
    )

print("\nEDA completed successfully.")
print("Reports saved in:", REPORT_DIR)
print("Charts saved in:", CHART_DIR)
