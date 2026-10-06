# Online Retail ELT Pipeline (Starter)

A moderate-complexity data engineering portfolio project built on **real**
transaction data — no synthetic or fake data anywhere.

Nothing here works yet. You're building it, piece by piece.

## The data

This project uses the **UCI Online Retail dataset** — real invoice records
from a UK-based online retailer, covering transactions from 2009–2011.
Each row is a real line item on a real invoice.

Columns:
| Column       | Meaning                                      |
|--------------|-----------------------------------------------|
| InvoiceNo    | Invoice number. Starts with "C" if cancelled  |
| StockCode    | Product code                                   |
| Description  | Product name                                   |
| Quantity     | Units sold (can be negative for returns)       |
| InvoiceDate  | Date/time of the transaction                   |
| UnitPrice    | Price per unit                                 |
| CustomerID   | Customer identifier (often missing)            |
| Country      | Customer's country                             |

**Get the data:** download it yourself from the UCI Machine Learning
Repository (search "Online Retail Data Set UCI") or Kaggle, and save it as
`data/raw/online_retail.csv`. This file is gitignored — you keep a local
copy, it never gets committed (it's a few MB, too large and not yours to
redistribute).

This is genuinely messy real-world data. You'll find:
- Cancelled orders (InvoiceNo starting with "C")
- Negative quantities (returns)
- Missing CustomerID on many rows
- Inconsistent product descriptions

Cleaning this for real is the actual data engineering work here — there's
no shortcut, and that's the point.

## Architecture

```
data/raw/online_retail.csv
        |
        v
  extract (read + basic validation)
        |
        v
  raw.transactions   (SQLite, loaded as-is, warts included)
        |
        v
  staging views       (cleaned: valid rows only, typed, deduplicated)
        |
        v
  mart views           (revenue by country, top products, monthly trends)
        |
        v
  report script         (prints a summary to the terminal)
```

No Docker, no Airflow, no dbt. Just Python and SQL — the two things worth
mastering first. SQLite means zero setup: it's a single file, no server,
no network dependency once the CSV is downloaded.

## Build order

1. **`sql/schema.sql`** — design the `raw.transactions` table. Think about
   types: should Quantity allow negatives? Should InvoiceDate be stored as
   text or a proper datetime? Should CustomerID be nullable?
2. **`src/extract.py`** — read the CSV with Python's `csv` module or
   pandas, do basic sanity checks (right number of columns, etc.)
3. **`src/load.py`** — load the raw rows into SQLite, as-is. Don't clean
   anything here — that's staging's job. This is the "L" in ELT: load
   first, transform after, inside the database.
4. **`sql/staging.sql`** — write a `CREATE VIEW staging_transactions AS...`
   that filters out cancelled orders, casts types properly, and excludes
   rows with missing critical data. Decide what "critical" means and be
   ready to explain your choice.
5. **`sql/marts.sql`** — build a few `CREATE VIEW` statements for actual
   business questions: revenue by country, top-selling products, monthly
   revenue trend, repeat customers (same CustomerID across multiple
   invoices).
6. **`src/report.py`** — query the mart views and print a readable summary.
7. **`tests/`** — pytest tests for your extract/load/transform logic.
8. **`.github/workflows/ci.yml`** — lint + test on every push.

## Stack
Python · SQLite · SQL · pytest · GitHub Actions

## Why this project
- **Real data, not synthetic** — every row is a genuine historical sale
- **Honest about scale** — no orchestration tooling pretending this is a
  big-data problem when it isn't; SQLite and plain SQL are the right-sized
  tools here
- **The ELT pattern, properly separated** — raw landing, staging
  (cleaning), marts (business logic) — same thinking as a "real" pipeline,
  just without infrastructure obscuring the logic
- **Fully explainable** — every file is something you wrote and can walk
  through line by line in an interview

## Notes to self
_(Design decisions, things you got stuck on, things you'd do differently —
good material for interview discussions later.)_
