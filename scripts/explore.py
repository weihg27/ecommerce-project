import duckdb

conn = duckdb.connect("olist.db")

tables = [
    "customers",
    "orders",
    "order_items",
    "products",
    "sellers"
]

for table in tables:
    print(f"\n===== {table.upper()} =====")
    print(conn.sql(f"DESCRIBE {table}").df())