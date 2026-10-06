"""
Extract stage: read the raw CSV file into memory.

TODO:
1. Write `read_transactions(path)` — read data/raw/online_retail.csv using
   either Python's built-in `csv.DictReader` or `pandas.read_csv`. Either
   is fine; pandas is easier for this dataset since it handles mixed types
   and missing values more gracefully.
2. Do a basic sanity check: does the file have the columns you expect?
   Raise a clear error if not — don't let a malformed file silently
   proceed to the load stage.
3. Return the data in whatever shape load.py will want it (a DataFrame if
   using pandas, or a list of dicts if using csv.DictReader).

Things to think about:
- The real file is ~540,000 rows. Don't load it into memory more than once
  if you can avoid it — but for a project this size, loading the whole
  thing with pandas is perfectly reasonable (don't over-engineer this).
- What encoding is the file in? Some versions of this dataset aren't
  plain UTF-8 — you may need to specify `encoding="ISO-8859-1"` or similar
  when reading. If you get a UnicodeDecodeError, that's the fix.
"""

import os
import pandas as pd
from pathlib import Path

DATA_PATH = Path(os.environ.get("RAW_CSV_PATH", "data/raw/online_retail.csv"))

EXPECTED_COLUMNS = [
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country",
]

def read_transactions(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Cannot find '{path}'. Make sure you downloaded the CSV and placed it in data/raw/."
        )

    # Use pandas to handle the 540k rows efficiently.
    # ISO-8859-1 encoding prevents UnicodeDecodeErrors common with the UCI dataset.
    # Casting IDs to string ensures pandas doesn't truncate leading zeros or fail on mixed types.
    df = pd.read_csv(
        path, 
        encoding="ISO-8859-1",
        dtype={"InvoiceNo": str, "StockCode": str, "CustomerID": str}
    )

    # Handle potential column name mismatches if you downloaded the Kaggle version 
    # instead of the direct UCI version.
    kaggle_rename_map = {
        "Invoice": "InvoiceNo",
        "Price": "UnitPrice",
        "Customer ID": "CustomerID"
    }
    df = df.rename(columns=kaggle_rename_map)

    # Sanity check: verify all expected columns are present
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Malformed CSV. Missing expected columns: {missing_cols}")

    # Return only the requested columns in the correct order
    return df[EXPECTED_COLUMNS]

if __name__ == "__main__":
    data = read_transactions()
    print(f"Read {len(data)} rows from {DATA_PATH}")
    print(data.head())