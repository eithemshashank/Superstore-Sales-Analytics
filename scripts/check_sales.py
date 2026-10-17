
from pathlib import Path
import pandas as pd
import csv

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "processed" / "superstore_clean.csv"

# Inspect the CSV using Python's CSV parser
with open(FILE, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)

    print("Number of CSV columns:", len(header))
    print("CSV header:", header)

    for row_number, row in enumerate(reader, start=2):
        if row_number in [1365, 1366, 1367]:
            print(f"\nCSV line {row_number}:")
            print("Number of fields:", len(row))
            print(row)

# Check the actual sales values using Pandas
df = pd.read_csv(FILE)
print("\nPandas column count:", len(df.columns))
print("Sales data types:", df["sales"].dtype)
print("\nRows around index 1365:")
print(df.iloc[1363:1367].to_string(index=False))

