import duckdb

conn = duckdb.connect("olist.db")

tables = {
    "customers": "data/olist_customers_dataset.csv",
    "orders": "data/olist_orders_dataset.csv",
    "order_items": "data/olist_order_items_dataset.csv",
    "products": "data/olist_products_dataset.csv",
    "sellers": "data/olist_sellers_dataset.csv",
    "payments": "data/olist_order_payments_dataset.csv",
    "reviews": "data/olist_order_reviews_dataset.csv",
    "geolocation": "data/olist_geolocation_dataset.csv"
}

for table_name, csv_file in tables.items():
    conn.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT *
        FROM read_csv_auto('{csv_file}')
    """)
    print(f"Loaded {table_name}")

print("\nAll tables loaded successfully!")