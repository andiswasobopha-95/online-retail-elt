-- Staging layer: cleans raw_transactions into analysis-ready rows.
--
-- Decisions:
--   * Cancellations (invoice prefix 'C' or negative quantity) are kept and
--     flagged with is_cancelled, so marts can calculate net revenue.
--   * Non-product rows (postage, manual adjustments, bank charges, etc.) are
--     excluded using an explicit list of fee and adjustment codes
--     (POST, D, DOT, M, BANK CHARGES, ADJUST, S, B, AMAZONFEE, CRUK).
--   * line_total is computed once here and rounded to 2 decimals.

DROP VIEW IF EXISTS staging_transactions;

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

    CASE
        WHEN InvoiceNo LIKE 'C%' OR Quantity < 0 THEN 1
        ELSE 0
    END AS is_cancelled,

    ROUND(CAST(Quantity AS REAL) * CAST(UnitPrice AS REAL), 2) AS line_total

FROM raw_transactions
WHERE InvoiceNo IS NOT NULL
  AND StockCode IS NOT NULL
  AND StockCode NOT IN ('POST', 'D', 'DOT', 'M', 'm', 'BANK CHARGES', 'ADJUST', 'S', 'B', 'AMAZONFEE', 'CRUK');
