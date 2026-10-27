import sqlite3
import pytest
from src import report


@pytest.fixture
def mock_mart_db(tmp_path, monkeypatch):
    """Creates a temporary SQLite database with mock analytical mart views/tables for reporting."""
    db_path = tmp_path / "test_report_retail.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create mock analytical tables / views matching what src.report queries
    cursor.execute("""
        CREATE TABLE monthly_revenue (
            order_month TEXT,
            total_orders INTEGER,
            net_revenue REAL
        );
    """)
    cursor.execute("""
        CREATE TABLE revenue_by_country (
            Country TEXT,
            total_orders INTEGER,
            net_revenue REAL
        );
    """)
    cursor.execute("""
        CREATE TABLE top_products (
            StockCode TEXT,
            Description TEXT,
            total_units_sold INTEGER,
            total_net_revenue REAL
        );
    """)

    # Insert mock summary data
    cursor.execute("INSERT INTO monthly_revenue VALUES ('2011-11', 100, 5000.00);")
    cursor.execute("INSERT INTO revenue_by_country VALUES ('United Kingdom', 90, 4500.00);")
    cursor.execute("INSERT INTO top_products VALUES ('85123A', 'WHITE HEART', 50, 1200.00);")
    
    conn.commit()
    conn.close()

    # Monkeypatch DB_PATH in src.report so it points to our temporary test database
    monkeypatch.setattr(report, "DB_PATH", db_path)
    return db_path


def test_report_run(mock_mart_db, capsys):
    """Tests that the report run() function executes successfully and prints summary blocks."""
    # Run the report generator
    report.run()

    # Capture standard output
    captured = capsys.readouterr()

    # Verify that key report headings and values appear in the console output
    assert "ONLINE RETAIL EXECUTIVE SUMMARY" in captured.out
    assert "Total Net Revenue" in captured.out
    assert "TOP 5 COUNTRIES BY NET REVENUE" in captured.out
    assert "United Kingdom" in captured.out
    assert "TOP 5 PRODUCTS BY NET REVENUE" in captured.out
    assert "MONTHLY REVENUE TRENDS" in captured.out
    assert "2011-11" in captured.out
