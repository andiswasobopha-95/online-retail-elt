import sqlite3
from pathlib import Path

DB_PATH = Path("online_retail.db")
STAGING_SQL_PATH = Path("sql/staging.sql")
MARTS_SQL_PATH = Path("sql/marts.sql")

def run_transformations(db_path: Path = DB_PATH):
    """Executes staging and marts SQL scripts and prints analytical insights."""
    if not STAGING_SQL_PATH.exists() or not MARTS_SQL_PATH.exists():
        raise FileNotFoundError("Transformation SQL files are missing.")
        
    print(f"Connecting to database at {db_path}...")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # 1. Run Staging Transformation
        print("Executing staging transformation script...")
        with open(STAGING_SQL_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
            
        cursor.execute("SELECT COUNT(*) FROM staging_transactions;")
        staging_count = cursor.fetchone()[0]
        print(f" -> Staging view ready ({staging_count:,} rows).")
        
        # 2. Run Marts Transformation
        print("Executing analytical marts script...")
        with open(MARTS_SQL_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print(" -> Analytical marts views created successfully!\n")
        
        # 3. Query & Print Insights: Top 5 Products
        print("--- TOP 5 PRODUCTS BY NET REVENUE ---")
        cursor.execute("""
            SELECT StockCode, Description, total_units_sold, total_net_revenue 
            FROM top_products 
            LIMIT 5;
        """)
        for row in cursor.fetchall():
            print(f"Code: {row[0]} | Desc: {row[1]} | Units: {row[2]:,} | Revenue: ${row[3]:,.2f}")
            
        # 4. Query & Print Insights: Monthly Revenue Trends
        print("\n--- MONTHLY REVENUE TRENDS (Sample) ---")
        cursor.execute("""
            SELECT order_month, total_orders, net_revenue 
            FROM monthly_revenue 
            LIMIT 5;
        """)
        for row in cursor.fetchall():
            print(f"Month: {row[0]} | Orders: {row[1]:,} | Net Revenue: ${row[2]:,.2f}")

        conn.commit()

if __name__ == "__main__":
    run_transformations()
