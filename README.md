# Online Retail ELT Pipeline

An end-to-end ELT pipeline that ingests real e-commerce transaction data,
loads it unmodified into a raw layer, cleans it in SQL, and exposes
analytics-ready views that answer real business questions about sales.

## Project Overview

Online retailers generate large volumes of messy transactional data:
cancelled invoices, product returns, guest checkouts with no customer ID,
inconsistent product names. Before anyone can answer "which countries drive
revenue?" or "what sells best?", that data has to be landed safely, cleaned
with clear rules, and modelled into trustworthy tables.

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

**UCI Online Retail dataset**, real transaction records from a UK-based
online retailer, roughly 540,000 line items covering December 2010 to
December 2011. Source: UCI Machine Learning Repository (see the dataset page
for licence and citation details).

| Column      | Description                                    |
|-------------|------------------------------------------------|
| InvoiceNo   | Invoice number (prefix `C` indicates a cancellation) |
| StockCode   | Product code                                   |
| Description | Product name                                   |
| Quantity    | Units sold (negative for returns)              |
| InvoiceDate | Date and time of the transaction               |
| UnitPrice   | Price per unit                                 |
| CustomerID  | Customer identifier (frequently missing)       |
| Country     | Customer's country                             |

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
   Staging   sql/staging.sql    cleaned, typed, analysis-ready rows
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

| Layer          | Tool                |
|----------------|---------------------|
| Language       | Python 3.10+        |
| Data handling  | pandas              |
| Storage        | SQLite              |
| Transformation | SQL views           |
| Testing        | pytest              |

SQLite and plain SQL were chosen on purpose: the dataset is a few hundred
thousand rows, so heavier infrastructure (Spark, Airflow, a warehouse server)
would add complexity without adding value.

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
│   └── report.py          # Print a summary from the mart views
├── tests/                 # pytest unit tests
├── requirements.txt
└── README.md
```

## Data Quality and Cleaning Decisions

Real data is messy, and the staging layer handles it explicitly rather than
silently. Issues found in the raw data and how they are treated:

| Issue                               | Treatment                              |
|-------------------------------------|----------------------------------------|
| Cancelled invoices (`C` prefix)     | [describe: excluded / flagged]         |
| Negative quantities (returns)       | [describe: kept for net sales / excluded] |
| Missing `CustomerID`                | [describe: kept for revenue, excluded from customer analysis] |
| Missing or inconsistent descriptions| [describe]                             |
| Derived `line_total`                | `Quantity * UnitPrice`, computed once in staging |

## Analytics Views

| View                 | Business question                              |
|----------------------|-------------------------------------------------|
| `revenue_by_country` | Which markets generate the most revenue?        |
| `top_products`       | Which products sell best by units and revenue?  |
| `monthly_revenue`    | How does revenue trend month to month?          |

## Sample Results

> output from `python -m src.report`.

======================================================
          ONLINE RETAIL EXECUTIVE SUMMARY          
======================================================
Total Net Revenue   : £19,399,632.17
Total Store Orders  : 52,214
Top Country         : United Kingdom (£16,597,424.74)
Best Month          : 2011-11 (£1,433,884.99)
Best-Selling Product: REGENCY CAKESTAND 3 TIER (£327,813.65)
======================================================

## Getting Started

**Prerequisites:** Python 3.10 or newer.

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. **Download the dataset** from the UCI Machine Learning Repository
   (search "Online Retail"), and save it as:
   ```
   data/raw/online_retail.csv
   ```
   The file is gitignored and is not redistributed with this repository.

4. **Run the pipeline**
   ```bash
   python -m src.load      # extract the CSV and load it into SQLite
   python -m src.report    # print the sales summary
   ```

5. **Run the tests**
   ```bash
   pytest tests/ -v
   ```

## Testing

Unit tests cover the extract and load logic, using in-memory SQLite
databases and temporary files so tests are fast and never touch real data.

## Possible Extensions

- Incremental loading instead of a full reload on each run
- Add a customer segmentation view (repeat vs one-time buyers)
- Orchestrate runs with a scheduler such as Airflow
- Migrate the storage layer to PostgreSQL
- Add data quality assertions as a separate validation step

## Acknowledgements

Dataset: UCI Machine Learning Repository, Online Retail dataset._

VERIFICATION CODE: WTC-4SF75D3P
