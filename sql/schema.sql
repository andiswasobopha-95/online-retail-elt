-- Raw landing table: mirrors the CSV columns, loaded as-is with no cleaning.

CREATE TABLE IF NOT EXISTS raw_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    InvoiceNo TEXT,
    StockCode TEXT,
    Description TEXT,
    Quantity INTEGER,
    InvoiceDate TEXT,
    UnitPrice REAL,
    CustomerID TEXT,
    Country TEXT,
    loaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
);