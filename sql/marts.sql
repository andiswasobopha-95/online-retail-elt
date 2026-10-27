-- Mart views: business-level summaries built on staging_transactions.
-- Drop existing views to allow clean re-creation
DROP VIEW IF EXISTS revenue_by_country;
DROP VIEW IF EXISTS top_products;
DROP VIEW IF EXISTS monthly_revenue;

-- =========================================================================
-- 1. Revenue by Country
-- Calculates total gross revenue, net revenue (accounting for returns), 
-- and total order count per country.
-- =========================================================================
CREATE VIEW revenue_by_country AS
SELECT 
    Country,
    COUNT(DISTINCT InvoiceNo) AS total_orders,
    ROUND(SUM(CASE WHEN is_cancelled = 0 THEN line_total ELSE 0 END), 2) AS gross_revenue,
    ROUND(SUM(CASE WHEN is_cancelled = 1 THEN ABS(line_total) ELSE 0 END), 2) AS total_refunds,
    ROUND(SUM(line_total), 2) AS net_revenue
FROM staging_transactions
GROUP BY Country
ORDER BY net_revenue DESC;


-- =========================================================================
-- 2. Top Products
-- Ranks products by total units sold and total net revenue generated.
-- =========================================================================
CREATE VIEW top_products AS
SELECT 
    StockCode,
    Description,
    SUM(CASE WHEN is_cancelled = 0 THEN Quantity ELSE 0 END) AS total_units_sold,
    ROUND(SUM(line_total), 2) AS total_net_revenue,
    COUNT(DISTINCT InvoiceNo) AS times_ordered
FROM staging_transactions
GROUP BY StockCode, Description
ORDER BY total_net_revenue DESC;


-- =========================================================================
-- 3. Monthly Revenue
-- Tracks financial performance and order volumes broken down by year and month.
-- =========================================================================
CREATE VIEW monthly_revenue AS
SELECT 
    -- Extracts 'YYYY-MM' from the invoice date string
    SUBSTR(InvoiceDate, 1, 7) AS order_month,
    COUNT(DISTINCT InvoiceNo) AS total_orders,
    ROUND(SUM(CASE WHEN is_cancelled = 0 THEN line_total ELSE 0 END), 2) AS gross_revenue,
    ROUND(SUM(line_total), 2) AS net_revenue
FROM staging_transactions
WHERE InvoiceDate IS NOT NULL AND LENGTH(InvoiceDate) >= 7
GROUP BY order_month
ORDER BY order_month ASC;