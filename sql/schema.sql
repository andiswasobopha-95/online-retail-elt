-- TODO: Design the raw landing table.
--
-- This should mirror the CSV columns closely — don't clean anything here,
-- that's staging's job. The raw layer's purpose is to capture the data
-- exactly as it arrived, so you always have an unmodified copy to fall
-- back on.
--
-- Columns from the CSV: InvoiceNo, StockCode, Description, Quantity,
-- InvoiceDate, UnitPrice, CustomerID, Country
--
-- Questions to think through:
--   - Should this table have a primary key? (Hint: no single column is
--     unique on its own — InvoiceNo + StockCode together might be, but
--     even that's not guaranteed. Consider a surrogate auto-increment id.)
--   - What type should Quantity be? It can be negative (returns).
--   - What type should InvoiceDate be? SQLite doesn't have a strict DATE
--     type — look up how SQLite handles dates (often stored as TEXT in
--     ISO format, or as a Unix timestamp).
--   - Should CustomerID be NOT NULL? (Hint: no — it's genuinely missing
--     on many real rows, and losing those rows at the raw layer would
--     defeat the point of a raw layer.)
--   - Should you add a `loaded_at` timestamp column, same pattern as
--     before?

CREATE TABLE IF NOT EXISTS raw_transactions (
    -- TODO: define columns
);
