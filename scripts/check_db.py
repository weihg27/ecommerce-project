import duckdb

conn = duckdb.connect("olist.db")

print(conn.sql("SHOW TABLES").df())