import sqlite3
from pathlib import Path
import pytest
from src.transform import run_staging_transform


@pytest.fixture
def temp_staging_db(tmp_path):
    """Creates a temporary SQLite database with a mock raw_transactions table."""
    db_path = tmp_path / "test_retail.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Create raw table schema
    cursor.execute("""
        CREATE TABLE raw_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            InvoiceNo TEXT,
            StockCode TEXT,
            Description TEXT,
            Quantity INTEGER,
            InvoiceDate TEXT,
            UnitPrice REAL,
            CustomerID TEXT,
            Country TEXT,
            loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Insert sample test data (two valid normal sales)
    sample_data = [
        ("536365", "85123A", "WHITE HANGING HEART T-LIGHT HOLDER", 6, "2010-12-01 08:26:00", 2.55, "17850", "United Kingdom"),
        ("536366", "22633", "HAND WARMER UNION JACK", 6, "2010-12-01 08:28:00", 1.85, "17850", "United Kingdom"),
    ]
    cursor.executemany("""
        INSERT INTO raw_transactions (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, sample_data)

    conn.commit()
    conn.close()
    return db_path


def test_run_staging_transform(temp_staging_db):
    """Tests that run_staging_transform builds the staging view and handles data correctly."""
    sql_path = Path("sql/staging.sql")
    assert sql_path.exists(), "sql/staging.sql file must exist for testing."

    # Run the staging transform function on our temporary test database
    run_staging_transform(db_path=temp_staging_db, sql_path=sql_path)

    # Verify the view contents
    with sqlite3.connect(temp_staging_db) as conn:
        cursor = conn.cursor()

        # Check total rows in view
        cursor.execute("SELECT COUNT(*) FROM staging_transactions;")
        total_rows = cursor.fetchone()[0]
        assert total_rows == 2, f"Expected 2 rows in staging view, got {total_rows}"

        # Check line total calculation
        cursor.execute("""
            SELECT InvoiceNo, line_total 
            FROM staging_transactions 
            ORDER BY InvoiceNo;
        """)
        rows = cursor.fetchall()

        # Row 1: Invoice 536365 (6 * 2.55 = 15.30)
        assert rows[0][0] == "536365"
        assert pytest.approx(rows[0][1], 0.01) == 15.30

        # Row 2: Invoice 536366 (6 * 1.85 = 11.10)
        assert rows[1][0] == "536366"
        assert pytest.approx(rows[1][1], 0.01) == 11.10
