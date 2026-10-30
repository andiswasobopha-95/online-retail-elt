# Online Retail ELT Pipeline

![Python](https://img.shields.io/badge/python-3.10+-blue)
![SQLite](https://img.shields.io/badge/database-SQLite-lightgrey)

An end-to-end ELT pipeline that ingests real e-commerce transaction data,
loads it unmodified into a raw layer, cleans it in SQL, and exposes
analytics-ready views that answer real business questions about sales.

## Project Overview

Online retailers generate large volumes of messy transactional data:
cancelled invoices, product returns, guest checkouts with no customer ID,
postage and adjustment lines mixed in with real products. Before anyone can
answer "which countries drive revenue?" or "what sells best?", that data has
to be landed safely, cleaned with clear rules, and modelled into trustworthy
tables.

This project does exactly that, using **real historical invoices** (no
synthetic or generated data) and a deliberately lightweight stack, Python,
SQLite and SQL, so every step of the pipeline is transparent and
explainable.

**What this project demonstrates**

- Building a layered ELT pipeline: raw, staging, marts
- Loading raw data as-is and doing transformations inside the database
- Making and documenting data cleaning decisions on genuinely messy data
- Writing analytical SQL views that answer business questions
- Testing pipeline code with pytest

## Dataset

**UCI Online Retail II dataset**, real transaction records from a UK-based
online retailer, about 1.07 million line items (1,067,371 rows) covering
December 2009 to December 2011. All monetary values are in pounds sterling
(£). The final month (December 2011) is partial because the data ends
part-way through it. Source: UCI Machine Learning Repository (see the dataset
page for licence and citation details).

| Column      | Description                                          |
|-------------|------------------------------------------------------|
| InvoiceNo   | Invoice number (prefix `C` indicates a cancellation) |
| StockCode   | Product code                                         |
| Description | Product name                                         |
| Quantity    | Units sold (negative for returns)                    |
| InvoiceDate | Date and time of the transaction                     |
| UnitPrice   | Price per unit                                       |
| CustomerID  | Customer identifier (frequently missing)             |
| Country     | Customer's country                                   |

Some copies of the dataset (for example on Kaggle) name three columns
differently (`Invoice`, `Price`, `Customer ID`). The extract step renames them
automatically.

## Architecture

```
 data/raw/online_retail.csv
            |
            v
   Extract   src/extract.py     read the CSV and validate its columns
            |
            v
   Load      src/load.py        write rows unmodified into SQLite
            |                   raw_transactions
            v
   Staging   src/transform.py   runs staging.sql, then marts.sql
            |                   staging_transactions (view)
            v
   Marts     sql/marts.sql      business-level views
            |                   revenue_by_country, top_products,
            |                   monthly_revenue
            v
   Report    src/report.py      prints a sales summary
```

**Why ELT and not ETL?** Raw data is loaded first and untouched, then
transformed inside the database with SQL. The original data is always
available to fall back on, and every cleaning rule lives in one visible,
reviewable place.

## Tech Stack

| Layer          | Tool           |
|----------------|----------------|
| Language       | Python 3.10+   |
| Data handling  | pandas         |
| Storage        | SQLite         |
| Transformation | SQL views      |
| Testing        | pytest         |

SQLite and plain SQL were chosen on purpose: the dataset is about a million
rows, so heavier infrastructure (Spark, Airflow, a warehouse server) would add
complexity without adding value.

## Project Structure

```
online-retail-elt/
├── data/raw/              # Place online_retail.csv here (gitignored)
├── sql/
│   ├── schema.sql         # Raw table definition
│   ├── staging.sql        # Cleaning view
│   └── marts.sql          # Analytics views
├── src/
│   ├── extract.py         # Read and validate the CSV
│   ├── load.py            # Load raw data into SQLite
│   ├── transform.py       # Run staging.sql and marts.sql to build the views
│   └── report.py          # Print a summary from the mart views
├── tests/                 # pytest unit tests
│   ├── test_extract.py
│   ├── test_load.py
│   ├── test_transform.py
│   └── test_report.py
├── requirements.txt
└── README.md
```

## Getting Started

**Prerequisites:** Python 3.10 or newer.

### 1. Clone the repository

```bash
git clone https://github.com/andiswasobopha-95/online-retail-elt.git
cd online-retail-elt
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate        # Linux and Mac
.\venv\Scripts\Activate.ps1     # Windows (PowerShell):
pip install -r requirements.txt
```

### 3. Download the dataset

Download the Online Retail II dataset from the UCI Machine Learning
Repository (search "Online Retail II"), and save it as:

```
data/raw/online_retail.csv
```

The file is gitignored and is not redistributed with this repository.

### 4. (Optional) Check the CSV reads correctly

```bash
python -m src.extract
```

This prints the row count and the first few rows. You should see
`Read 1067371 rows`.

### 5. Run the pipeline, in this order

```bash
python -m src.load        # 1. load the raw CSV into SQLite (online_retail.db)
python -m src.transform   # 2. build the staging view and the analytics views
python -m src.report      # 3. print the sales summary
```

Each step depends on the one before it, so run them in this order. Running
`load` again replaces the raw table and reloads it from the CSV, so you never
get duplicate rows. To start completely fresh, delete the database file first:

```bash
rm online_retail.db
```

### 6. Run the tests

```bash
pytest tests/ -v
```

The tests build their own small datasets and use temporary files and
in-memory databases, so they do not need the real CSV.

## Configuration

Defaults work out of the box. Set these environment variables only if your
files live somewhere else.

| Variable          | Default                       | Purpose               |
|-------------------|-------------------------------|-----------------------|
| `RAW_CSV_PATH`    | `data/raw/online_retail.csv`  | Location of the CSV   |
| `SQLITE_DB_PATH`  | `online_retail.db`            | Location of the database file |

Example:

```bash
RAW_CSV_PATH=/path/to/file.csv python -m src.load
```

## Exploring the data (optional)

If you have the `sqlite3` command-line tool installed, you can query the
views directly:

```bash
sqlite3 online_retail.db "DROP VIEW IF EXISTS revenue_by_country;"
sqlite3 online_retail.db ".tables"
sqlite3 online_retail.db "DROP VIEW IF EXISTS top_products;"
sqlite3 online_retail.db "SELECT * FROM monthly_revenue LIMIT 5;"
```

## Data Quality and Cleaning Decisions

Real data is messy, and the staging layer handles it explicitly rather than
silently. Issues found in the raw data and how they are treated:

| Issue                                         | Treatment |
|-----------------------------------------------|-----------|
| Cancelled invoices (`C` prefix)               | Kept and flagged with an `is_cancelled` column (21,755 of 1,061,862 staging rows), not deleted |
| Negative quantities (returns)                 | Kept and flagged with the same `is_cancelled` column, not deleted |
| Missing `CustomerID`                          | Kept in staging, not dropped |
| Missing or inconsistent descriptions          | Kept as loaded, no description cleaning |
| Non-product stock codes                       | Excluded (5,509 rows): `POST`, `D`, `DOT`, `M`, `BANK CHARGES`, `ADJUST`, `S`, `B`, `AMAZONFEE`, `CRUK` |
| Derived `line_total`                          | `Quantity * UnitPrice`, rounded to 2 decimals, computed once in staging |

Postage, discounts, manual adjustments, bad debt and marketplace fees are
excluded because they are not product sales. This means the revenue figures
below describe product revenue rather than the retailer's full accounting
revenue.

## Analytics Views

| View                 | Business question                              |
|----------------------|------------------------------------------------|
| `revenue_by_country` | Which markets generate the most revenue?       |
| `top_products`       | Which products sell best by units and revenue? |
| `monthly_revenue`    | How does revenue trend month to month?         |

## Sample Results

Output of `python -m src.report`:

| Metric                 | Result                                 |
|------------------------|----------------------------------------|
| Total net revenue      | £19,399,632.17                         |
| Total orders           | 52,214                                 |
| Top country by revenue | United Kingdom (£16,597,424.74)        |
| Best month             | 2011-11 (£1,433,884.99)                |
| Best-selling product   | REGENCY CAKESTAND 3 TIER (£327,813.65) |

**Key findings**

- The United Kingdom generates roughly 86% of net revenue. The next largest
  markets are EIRE, the Netherlands, Germany and France.
- Revenue is strongly seasonal: November is the peak month in both years
  (£1.40M in 2010, £1.43M in 2011), consistent with pre-Christmas demand.
- December 2011 looks like a sharp drop only because the data ends part-way
  through that month.

## Testing

Unit tests cover the extract, load, transform and report steps, using
in-memory SQLite databases and temporary files so tests are fast and never
touch the real data.

## Possible Extensions

- Incremental loading instead of a full reload on each run
- Add a customer segmentation view (repeat vs one-time buyers)
- Orchestrate runs with a scheduler such as Airflow
- Migrate the storage layer to PostgreSQL
- Add data quality assertions as a separate validation step

## Author

**Andiswa** · [GitHub](https://github.com/andiswasobopha-95)

## Acknowledgements

Dataset: UCI Machine Learning Repository, Online Retail II dataset.

VERIFICATION CODE: WTC-4SF75D3P
