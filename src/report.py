"""
Report stage: query the mart views and print a readable summary.

TODO:
1. Connect to the SQLite DB (reuse get_connection from load.py).
2. Query each mart view (revenue_by_country, top_products,
   monthly_revenue) and print a formatted summary — doesn't need to be
   fancy, clear console output is enough. Look up Python's f-strings for
   formatting, or the `tabulate` library if you want nicer tables
   (optional, not required).
3. Highlight a few headline numbers: total revenue, top country, best
   month, best-selling product.
"""
from src.load import get_connection


def run():
    # TODO: implement this
    raise NotImplementedError


if __name__ == "__main__":
    run()
