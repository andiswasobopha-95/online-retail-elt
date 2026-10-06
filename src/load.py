"""
Load stage: write the raw transactions into SQLite, unmodified.

TODO:
1. Write `get_connection(db_path)` — use Python's built-in `sqlite3` module
   (no install needed, it's in the standard library). Look up
   `sqlite3.connect(path)`.
2. Write `init_schema(conn)` — run sql/schema.sql against the connection to
   create the raw table if it doesn't exist. Look up reading a .sql file
   and running it with `conn.executescript(...)`.
3. Write `load_raw(conn, transactions)` — insert the rows into your raw
   table. Use parameterized queries (`?` placeholders), never string
   formatting, to avoid SQL injection and handle special characters in
   product descriptions correctly.
4. Write `run()` tying it together: read the CSV (via extract.py), connect
   to the DB, init the schema, load the rows, commit.

Things to think about:
- Should re-running this duplicate every row? For a project this size, it's
  reasonable to just wipe and reload the raw table each run (`DELETE FROM
  raw_transactions` before inserting) rather than building full upsert
  logic — but think about whether that's the right call and be ready to
  explain your reasoning.
- With ~540,000 rows, inserting one row at a time in a loop will be slow.
  Look up `cursor.executemany()` for bulk inserts — much faster.
"""
import os
import sqlite3
from pathlib import Path

from src.extract import read_transactions

DB_PATH = Path(os.environ.get("SQLITE_DB_PATH", "online_retail.db"))
SCHEMA_PATH = Path("sql/schema.sql")


def get_connection(db_path: Path = DB_PATH):
    # TODO: implement this
    raise NotImplementedError


def init_schema(conn, schema_path: Path = SCHEMA_PATH):
    # TODO: implement this
    raise NotImplementedError


def load_raw(conn, transactions):
    # TODO: implement this
    raise NotImplementedError


def run():
    # TODO: tie it together
    raise NotImplementedError


if __name__ == "__main__":
    run()
