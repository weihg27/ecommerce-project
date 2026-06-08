import duckdb

conn = duckdb.connect("olist.db")

print(
    conn.sql("""
    SELECT COUNT(*)
    FROM fact_sales
    """).df()
)