"""
TODO: Write unit tests for src/extract.py.

Ideas:
- Write a small sample CSV to a temp file (pytest's tmp_path fixture) with
  a handful of rows, including one with a missing CustomerID, then assert
  read_transactions() reads it correctly.
- Test that read_transactions() raises a clear error on a file with the
  wrong columns.

Run with: pytest tests/ -v
"""
