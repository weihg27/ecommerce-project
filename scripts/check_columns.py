import duckdb

conn = duckdb.connect("olist.db")

print(
    conn.sql("""
    DESCRIBE category_translation
    """).df()
)