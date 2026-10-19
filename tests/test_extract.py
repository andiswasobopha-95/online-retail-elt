import pandas as pd
import pytest
from pathlib import Path
from src.extract import read_transactions


def test_read_transactions_success(tmp_path):
    """Test that valid CSV files with mixed or missing CustomerIDs are read correctly."""
    # Create a temporary CSV file
    file_path = tmp_path / "online_retail_sample.csv"
    
    csv_content = (
        "InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country\n"
        "489434,85048,REGENCY CAKESTAND 3 TIER,12,2009-12-01 07:45:00,6.95,13085.0,United Kingdom\n"
        "489435,79323P,PINK CHRYSANTHEMUM ARTIFICIAL FLOWER,6,2009-12-01 07:46:00,4.25,,United Kingdom\n"
    )
    file_path.write_text(csv_content, encoding="utf-8")
    
    # Run extraction on the temporary file
    df = read_transactions(file_path)
    
    # Assertions
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == [
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country",
    ]
    # Verify the row with missing CustomerID is handled gracefully as NaN/null
    assert pd.isna(df.loc[1, "CustomerID"])


def test_read_transactions_wrong_columns(tmp_path):
    """Test that a clear ValueError is raised if the CSV lacks expected columns."""
    file_path = tmp_path / "bad_schema.csv"
    
    csv_content = (
        "BadColumn1,BadColumn2\n"
        "value1,value2\n"
    )
    file_path.write_text(csv_content, encoding="utf-8")
    
    # Assert that a ValueError is raised due to missing schema columns
    with pytest.raises(ValueError, match="Malformed CSV"):
        read_transactions(file_path)
