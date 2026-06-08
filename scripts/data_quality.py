import duckdb

conn = duckdb.connect("olist.db")

checks = {

    "Null customer_id": """
        SELECT COUNT(*)
        FROM fact_sales
        WHERE customer_id IS NULL
    """,

    "Null product_id": """
        SELECT COUNT(*)
        FROM fact_sales
        WHERE product_id IS NULL
    """,

    "Null seller_id": """
        SELECT COUNT(*)
        FROM fact_sales
        WHERE seller_id IS NULL
    """,

    "Negative sales amount": """
        SELECT COUNT(*)
        FROM fact_sales
        WHERE sales_amount < 0
    """
}

for check_name, query in checks.items():
    result = conn.sql(query).fetchone()[0]
    print(f"{check_name}: {result}")