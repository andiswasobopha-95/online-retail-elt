"""Extract stage: read the raw Online Retail CSV into a pandas DataFrame and
check that the expected columns are present."""

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

    # Use pandas to handle the about 1 million rows efficiently.
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