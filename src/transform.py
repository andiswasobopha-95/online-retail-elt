import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("SQLITE_DB_PATH", "online_retail.db"))
STAGING_SQL_PATH = Path("sql/staging.sql")
MARTS_SQL_PATH = Path("sql/marts.sql")

def run_staging_transform(
    db_path: Path = DB_PATH,
    sql_path: Path = STAGING_SQL_PATH,
    marts_path: Path = MARTS_SQL_PATH,
):
    """Executes the staging SQL script to create the staging view and verifies it works."""
    if not sql_path.exists():
        raise FileNotFoundError(f"Staging SQL file not found at {sql_path}")
        
    print(f"Connecting to database at {db_path}...")
    with sqlite3.connect(db_path) as conn:
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_script = f.read()
            
        print("Executing staging transformation script...")
        conn.executescript(sql_script)
        conn.commit()

        if not marts_path.exists():
            raise FileNotFoundError(f"Marts SQL file not found at {marts_path}")
        print("Executing mart views script...")
        conn.executescript(marts_path.read_text(encoding="utf-8"))
        conn.commit()
        
        # Verification queries
        cursor = conn.cursor()
        
        # 1. Total rows in the staging view
        cursor.execute("SELECT COUNT(*) FROM staging_transactions;")
        total_rows = cursor.fetchone()[0]
        
        # 2. Count cancellations vs normal transactions
        cursor.execute("SELECT is_cancelled, COUNT(*) FROM staging_transactions GROUP BY is_cancelled;")
        breakdown = cursor.fetchall()
        
        # 3. Sample rows
        cursor.execute("""
            SELECT InvoiceNo, StockCode, Quantity, UnitPrice, line_total, is_cancelled 
            FROM staging_transactions 
            LIMIT 5;
        """)
        sample_rows = cursor.fetchall()
        
    print(f"\n Staging view created successfully!")
    print(f"Total rows in staging view: {total_rows:,}")
    print("\nCancellation breakdown (0 = normal, 1 = cancelled/return):")
    for status, count in breakdown:
        print(f"  - Status {status}: {count:,} rows")
        
    print("\nSample transformed rows:")
    for row in sample_rows:
        print(row)

if __name__ == "__main__":
    run_staging_transform()