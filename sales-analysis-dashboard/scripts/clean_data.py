
from pathlib import Path
import pandas as pd

# Find the project folder
ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    ROOT / "data" / "raw" / "Superstore_Sales_Analysis  (1).xlsx"
)
OUTPUT_DIR = ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "superstore_clean.csv"

# Load the dataset
if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"CSV file not found: {INPUT_FILE}\n"
        "Place superstore.csv inside data/raw/"
    )

df = pd.read_excel(INPUT_FILE)

# Standardize column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

# Display data quality information
print("\n--- DATASET OVERVIEW ---")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATES ---")
print("Duplicate rows:", df.duplicated().sum())

# Clean whitespace in text columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].map(
        lambda x: x.strip() if isinstance(x, str) else x
    )

# Convert dates where present
for col in ["order_date", "ship_date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(
            df[col], errors="coerce", dayfirst=True
        )

# Convert numeric fields where present
for col in ["sales", "profit", "discount", "quantity"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Save cleaned data
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("\n--- CLEANING COMPLETE ---")
print("Saved to:", OUTPUT_FILE)
print("Final shape:", df.shape)
