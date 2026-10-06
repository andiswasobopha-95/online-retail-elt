"""
TODO: Write unit tests for src/load.py.

Ideas:
- Use an in-memory SQLite DB for tests: sqlite3.connect(":memory:") —
  no file needed, fast, and isolated per test.
- Test init_schema() creates the raw_transactions table.
- Test load_raw() inserts the expected number of rows, and that a row's
  values round-trip correctly (read back what you inserted).

Run with: pytest tests/ -v
"""
