
from pathlib import Path
from getpass import getpass

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "data" / "processed" / "superstore_clean.csv"

if not CSV_FILE.exists():
    raise FileNotFoundError(f"CSV not found: {CSV_FILE}")

# Load and validate the CSV before touching MySQL
df = pd.read_csv(CSV_FILE)
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

expected_columns = [
    "row_id", "order_id", "order_date", "ship_date",
    "ship_mode", "customer_id", "customer_name", "segment",
    "country", "city", "state", "postal_code", "region",
    "product_id", "category", "sub_category", "product_name",
    "sales", "quantity", "discount", "profit"
]

if list(df.columns) != expected_columns:
    raise ValueError(f"Unexpected columns: {df.columns.tolist()}")

if len(df) != 9994:
    raise ValueError(f"Expected 9994 rows; found {len(df)}")

for col in ["order_date", "ship_date"]:
    df[col] = pd.to_datetime(df[col], errors="raise").dt.date

for col in ["sales", "quantity", "discount", "profit", "row_id"]:
    df[col] = pd.to_numeric(df[col], errors="raise")

# Enter your MySQL root password locally; it won't be displayed.
password = getpass("MySQL root password: ")

url = URL.create(
    "mysql+pymysql",
    username="root",
    password=password,
    host="127.0.0.1",
    port=3306,
    database="sales_analysis",
)

engine = create_engine(url)

try:
    with engine.connect() as conn:
        # Confirm that the destination table exists.
        conn.execute(text("SELECT 1 FROM superstore LIMIT 1"))

    # Replace the partial import only after validating the CSV
    # and confirming the destination table.
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE superstore"))

    df.to_sql(
        "superstore",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=500,
        method="multi",
    )

    with engine.connect() as conn:
        count = conn.execute(
            text("SELECT COUNT(*) FROM superstore")
        ).scalar_one()

        totals = conn.execute(text("""
            SELECT
                ROUND(SUM(sales), 2),
                ROUND(SUM(profit), 2),
                COUNT(DISTINCT order_id)
            FROM superstore
        """)).one()

    print("\nImport complete!")
    print("Rows imported:", count)
    print("Total sales:", totals[0])
    print("Total profit:", totals[1])
    print("Unique orders:", totals[2])

finally:
    engine.dispose()
