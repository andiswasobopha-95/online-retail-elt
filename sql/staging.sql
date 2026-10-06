-- Drop the view if it already exists to allow clean re-creation
DROP VIEW IF EXISTS staging_transactions;

-- Create the staging view with business logic applied
CREATE VIEW staging_transactions AS
SELECT 
    InvoiceNo,
    StockCode,
    Description,
    CAST(Quantity AS INTEGER) AS Quantity,
    InvoiceDate,
    CAST(UnitPrice AS REAL) AS UnitPrice,
    CustomerID,
    Country,
    
    -- Flag cancellations (either 'C' prefix or negative quantity)
    CASE 
        WHEN InvoiceNo LIKE 'C%' OR Quantity < 0 THEN 1 
        ELSE 0 
    END AS is_cancelled,
    
    -- Precompute line total for downstream marts
    (CAST(Quantity AS REAL) * CAST(UnitPrice AS REAL)) AS line_total,
    
    loaded_at

FROM raw_transactions
WHERE InvoiceNo IS NOT NULL 
  AND StockCode IS NOT NULL;
