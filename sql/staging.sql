-- TODO: Build a staging view that cleans the raw data.
--
-- This is where real business judgment comes in. Think through each
-- decision rather than copying a pattern blindly:
--
-- 1. Cancelled orders: InvoiceNo starting with "C" means a cancellation.
--    Should these be excluded from staging entirely, or kept but flagged
--    with a column like `is_cancelled`? Either is defensible — pick one
--    and be ready to explain why.
--
-- 2. Missing CustomerID: many rows have no customer attached (likely
--    guest checkouts or data quality issues in the original export).
--    Should you exclude these, or keep them for revenue totals but
--    exclude them from customer-level analysis? Think about which mart
--    views will need CustomerID and which won't.
--
-- 3. Negative quantities: these are returns, not necessarily bad data.
--    Should staging keep them (so marts can calculate net sales = sales
--    minus returns) or exclude them? Keeping them and calculating "net"
--    in the marts layer is usually the more honest approach.
--
-- 4. Computed columns: consider adding `line_total` (Quantity * UnitPrice)
--    here, so you don't repeat that calculation in every downstream mart.
--
-- CREATE VIEW staging_transactions AS
-- SELECT
--     ...
-- FROM raw_transactions
-- WHERE ...
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
    
    -- 1. Flag cancellations (either 'C' prefix or negative quantity)
    CASE 
        WHEN InvoiceNo LIKE 'C%' OR Quantity < 0 THEN 1 
        ELSE 0 
    END AS is_cancelled,
    
    -- 4. Precompute line total for downstream marts
    (CAST(Quantity AS REAL) * CAST(UnitPrice AS REAL)) AS line_total

FROM raw_transactions
WHERE InvoiceNo IS NOT NULL 
  AND StockCode IS NOT NULL;