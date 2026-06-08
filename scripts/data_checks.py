import duckdb

conn = duckdb.connect("olist.db")

queries = {
    "customers": """
        SELECT COUNT(*) total_rows,
               COUNT(DISTINCT customer_id) unique_customers
        FROM customers
    """,

    "orders": """
        SELECT COUNT(*) total_rows,
               COUNT(DISTINCT order_id) unique_orders
        FROM orders
    """,

    "products": """
        SELECT COUNT(*) total_rows,
               COUNT(DISTINCT product_id) unique_products
        FROM products
    """,

    "sellers": """
        SELECT COUNT(*) total_rows,
               COUNT(DISTINCT seller_id) unique_sellers
        FROM sellers
    """
}

for name, query in queries.items():
    print(f"\n{name.upper()}")
    print(conn.sql(query).df())