import sqlite3
import pandas as pd
import pytest
from pathlib import Path
from src.load import init_schema, load_raw


def test_init_schema():
    """Test that init_schema successfully creates the raw_transactions table."""
    conn = sqlite3.connect(":memory:")
    schema_path = Path("sql/schema.sql")
    
    # Run schema initialization
    init_schema(conn, schema_path)
    
    # Verify table exists in sqlite_master
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='raw_transactions';"
    )
    table = cursor.fetchone()
    conn.close()
    
    assert table is not None
    assert table[0] == "raw_transactions"


def test_load_raw_roundtrip():
    """Test that load_raw correctly inserts rows and they round-trip properly."""
    conn = sqlite3.connect(":memory:")
    schema_path = Path("sql/schema.sql")
    init_schema(conn, schema_path)
    
    # Mock transaction data as a pandas DataFrame matching the schema contract
    sample_data = pd.DataFrame([
        {
            "InvoiceNo": "489434",
            "StockCode": "85048",
            "Description": "REGENCY CAKESTAND 3 TIER",
            "Quantity": 12,
            "InvoiceDate": "2009-12-01 07:45:00",
            "UnitPrice": 6.95,
            "CustomerID": "13085.0",
            "Country": "United Kingdom"
        },
        {
            "InvoiceNo": "489435",
            "StockCode": "79323P",
            "Description": "PINK FLOWER",
            "Quantity": 6,
            "InvoiceDate": "2009-12-01 07:46:00",
            "UnitPrice": 4.25,
            "CustomerID": None,
            "Country": "United Kingdom"
        }
    ])
    
    # Load the raw data
    load_raw(conn, sample_data)
    
    # Verify row count and values round-trip
    cursor = conn.cursor()
    cursor.execute(
        "SELECT InvoiceNo, StockCode, Quantity, UnitPrice, CustomerID FROM raw_transactions ORDER BY InvoiceNo;"
    )
    rows = cursor.fetchall()
    conn.close()
    
    assert len(rows) == 2
    
    # Check first row values
    assert rows[0][0] == "489434"
    assert rows[0][1] == "85048"
    assert rows[0][2] == 12
    assert rows[0][3] == 6.95
    assert rows[0][4] == "13085.0"
    
    # Check second row (verifying pandas NaN converted to SQL NULL)
    assert rows[1][0] == "489435"
    assert rows[1][4] is None
