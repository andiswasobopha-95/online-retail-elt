from src.load import get_connection, DB_PATH


def run():
    """Queries mart views and prints a formatted executive summary report."""
    print(f"Connecting to database at {DB_PATH}...")
    with get_connection(DB_PATH) as conn:
        cursor = conn.cursor()

        # 1. Headline Numbers
        # Total Net Revenue & Total Orders
        cursor.execute("SELECT SUM(net_revenue), SUM(total_orders) FROM monthly_revenue;")
        row = cursor.fetchone()
        total_net_rev = row[0] if row and row[0] else 0.0
        total_orders = row[1] if row and row[1] else 0

        # Top Country by Net Revenue
        cursor.execute("SELECT Country, net_revenue FROM revenue_by_country ORDER BY net_revenue DESC LIMIT 1;")
        top_country_row = cursor.fetchone()
        top_country = top_country_row[0] if top_country_row else "N/A"
        top_country_rev = top_country_row[1] if top_country_row else 0.0

        # Best Month by Net Revenue
        cursor.execute("SELECT order_month, net_revenue FROM monthly_revenue ORDER BY net_revenue DESC LIMIT 1;")
        best_month_row = cursor.fetchone()
        best_month = best_month_row[0] if best_month_row else "N/A"
        best_month_rev = best_month_row[1] if best_month_row else 0.0

        # Best-Selling Product by Net Revenue
        cursor.execute("SELECT StockCode, Description, total_net_revenue FROM top_products ORDER BY total_net_revenue DESC LIMIT 1;")
        top_prod_row = cursor.fetchone()
        top_prod_desc = top_prod_row[1] if top_prod_row else "N/A"
        top_prod_rev = top_prod_row[2] if top_prod_row else 0.0

        # Print Executive Summary Headline Block
        print("\n" + "=" * 54)
        print("          ONLINE RETAIL EXECUTIVE SUMMARY          ")
        print("=" * 54)
        print(f"💰 Total Net Revenue   : £{total_net_rev:,.2f}")
        print(f"📦 Total Store Orders  : {total_orders:,}")
        print(f"🌍 Top Country         : {top_country} (£{top_country_rev:,.2f})")
        print(f"📈 Best Month          : {best_month} (£{best_month_rev:,.2f})")
        print(f"🏆 Best-Selling Product: {top_prod_desc} (£{top_prod_rev:,.2f})")
        print("=" * 54 + "\n")

        # 2. Detailed Mart Summaries
        print("--- TOP 5 COUNTRIES BY NET REVENUE ---")
        cursor.execute("SELECT Country, total_orders, net_revenue FROM revenue_by_country LIMIT 5;")
        for country, orders, rev in cursor.fetchall():
            print(f"  * {country:<15} | Orders: {orders:<6,} | Net Revenue: £{rev:,.2f}")

        print("\n--- TOP 5 PRODUCTS BY NET REVENUE ---")
        cursor.execute("SELECT StockCode, Description, total_units_sold, total_net_revenue FROM top_products LIMIT 5;")
        for code, desc, units, rev in cursor.fetchall():
            short_desc = (desc[:28] + "..") if len(desc) > 30 else desc
            print(f"  * [{code}] {short_desc:<30} | Units: {units:<6,} | Revenue: £{rev:,.2f}")

        print("\n--- MONTHLY REVENUE TRENDS ---")
        cursor.execute("SELECT order_month, total_orders, net_revenue FROM monthly_revenue;")
        for month, orders, rev in cursor.fetchall():
            print(f"  * Month: {month}   | Orders: {orders:<5,} | Net Revenue: £{rev:,.2f}")
        print("-" * 54)


if __name__ == "__main__":
    run()
