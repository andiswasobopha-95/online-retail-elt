import os
import sqlite3
from pathlib import Path
import pandas as pd

from src.extract import read_transactions

DB_PATH = Path(os.environ.get("SQLITE_DB_PATH", "online_retail.db"))
SCHEMA_PATH = Path("sql/schema.sql")


def get_connection(db_path: Path = DB_PATH):
    """Create and return a SQLite database connection."""
    return sqlite3.connect(db_path)


def init_schema(conn, schema_path: Path = SCHEMA_PATH):
    """Run sql/schema.sql against the connection to create the raw table."""
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found at {schema_path}")
    
    with open(schema_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
        
    conn.executescript(sql_script)
    conn.commit()


def load_raw(conn, transactions):
    """
    Insert rows into raw_transactions using executemany and parameterized queries
    to avoid SQL injection and handle special characters securely.
    """
    cursor = conn.cursor()
    
    # Wipe the table on each run to prevent duplicate accumulation during development
    cursor.execute("DELETE FROM raw_transactions;")
    
    # If transactions is a pandas DataFrame, convert it to a clean list of tuples
    if isinstance(transactions, pd.DataFrame):
        cols = [
            "InvoiceNo", "StockCode", "Description", "Quantity",
            "InvoiceDate", "UnitPrice", "CustomerID", "Country"
        ]
        # Replace pandas NaN with Python None so SQLite stores them as proper NULLs
        rows = [
            tuple(None if pd.isna(val) else val for val in row)
            for row in transactions[cols].itertuples(index=False, name=None)
        ]
    else:
        rows = transactions

    insert_sql = """
        INSERT INTO raw_transactions (
            InvoiceNo, StockCode, Description, Quantity,
            InvoiceDate, UnitPrice, CustomerID, Country
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    print(f"Executing bulk insert for {len(rows)} rows...")
    cursor.executemany(insert_sql, rows)
    conn.commit()


def run():
    """Tie it together: read CSV, connect to DB, init schema, load rows, commit."""
    print("Step 1: Reading raw CSV data...")
    df = read_transactions()
    
    print(f"Step 2: Opening connection to {DB_PATH}...")
    conn = get_connection(DB_PATH)
    
    try:
        print("Step 3: Initializing database schema...")
        init_schema(conn, SCHEMA_PATH)
        
        print("Step 4: Loading raw rows into SQLite...")
        load_raw(conn, df)
        print("Load stage completed successfully!")
    finally:
        conn.close()


if __name__ == "__main__":
    run()
