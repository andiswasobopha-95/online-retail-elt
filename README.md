# Online Retail ELT Data Pipeline

A robust, production-grade ELT (Extract, Load, Transform) data pipeline built on real-world transaction data.

## Project Overview
Processes over 1 million rows from the UCI Online Retail dataset (2009–2011) using a modern ELT pattern:
1. **Extract**: Safely reads CSVs with encoding handling and schema validation.
2. **Load**: Performs idempotent bulk inserts into SQLite into an untouched raw landing table.
3. **Transform**: Builds clean SQL views for staging and analytical business marts.

## Tech Stack
Python · Pandas · SQLite · SQL · Pytest

