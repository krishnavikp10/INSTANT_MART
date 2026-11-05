
"""SQL analytics module for InstaMart Copilot."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "instamart.db"


def run_query(connection, title, query):
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)

    cursor = connection.execute(query)
    columns = [description[0] for description in cursor.description]

    print(" | ".join(columns))
    print("-" * 65)

    rows = cursor.fetchall()

    if not rows:
        print("No records found.")
        return

    for row in rows:
        print(" | ".join(str(value) for value in row))


def run_analysis_queries():
    if not DB_PATH.exists():
        print("Database not found:", DB_PATH)
        print("Run the database setup module first.")
        return

    connection = sqlite3.connect(DB_PATH)

    try:
        print("INSTANTMART SQL ANALYTICS")
        print("Database:", DB_PATH)

        # 1. Revenue by city with normalized city names
        run_query(
            connection,
            "1. REVENUE BY CITY",
            """
            SELECT
                UPPER(TRIM(c.city)) AS city,
                ROUND(SUM(o.order_amount), 2) AS total_revenue
            FROM orders o
            JOIN customers c
                ON o.customer_id = c.customer_id
            WHERE LOWER(TRIM(o.status)) = 'completed'
            GROUP BY UPPER(TRIM(c.city))
            ORDER BY total_revenue DESC
            """
        )

        # 2. Top 5 products
        run_query(
            connection,
            "2. TOP 5 PRODUCTS",
            """
            SELECT
                p.product_name,
                SUM(o.quantity) AS total_quantity_sold,
                ROUND(SUM(o.order_amount), 2) AS total_revenue
            FROM orders o
            JOIN products p
                ON o.product_id = p.product_id
            WHERE LOWER(TRIM(o.status)) = 'completed'
            GROUP BY p.product_id, p.product_name
            ORDER BY total_quantity_sold DESC
            LIMIT 5
            """
        )

        # 3. Orders by normalized status
        run_query(
            connection,
            "3. ORDERS BY STATUS",
            """
            SELECT
                COALESCE(
                    NULLIF(LOWER(TRIM(status)), ''),
                    'missing'
                ) AS order_status,
                COUNT(*) AS total_orders
            FROM orders
            GROUP BY order_status
            ORDER BY total_orders DESC
            """
        )

        # 4. Average delivery time
        run_query(
            connection,
            "4. AVERAGE DELIVERY TIME",
            """
            SELECT
                ROUND(AVG(delivery_minutes), 2)
                    AS average_delivery_minutes
            FROM orders
            WHERE LOWER(TRIM(status)) = 'completed'
              AND delivery_minutes IS NOT NULL
            """
        )

        # 5. Ticket category distribution
        run_query(
            connection,
            "5. TICKET CATEGORY ANALYSIS",
            """
            SELECT
                LOWER(TRIM(true_category)) AS category,
                COUNT(*) AS total_tickets
            FROM tickets
            GROUP BY LOWER(TRIM(true_category))
            ORDER BY total_tickets DESC
            """
        )

        # 6. Database record summary
        run_query(
            connection,
            "6. DATABASE RECORD SUMMARY",
            """
            SELECT 'Customers' AS table_name, COUNT(*) AS total_records
            FROM customers
            UNION ALL
            SELECT 'Products', COUNT(*) FROM products
            UNION ALL
            SELECT 'Orders', COUNT(*) FROM orders
            UNION ALL
            SELECT 'Tickets', COUNT(*) FROM tickets
            """
        )

        # 7. Missing order status check
        run_query(
            connection,
            "7. ORDER STATUS DATA QUALITY CHECK",
            """
            SELECT
                COUNT(*) AS orders_with_missing_status
            FROM orders
            WHERE status IS NULL
               OR TRIM(status) = ''
            """
        )

        print("\nSQL ANALYSIS COMPLETED SUCCESSFULLY.")

    except sqlite3.Error as error:
        print("Database query error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    run_analysis_queries()
