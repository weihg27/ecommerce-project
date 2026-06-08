import duckdb

conn = duckdb.connect("olist.db")

conn.sql("DROP TABLE IF EXISTS my_first_dbt_model")
conn.sql("DROP VIEW IF EXISTS my_second_dbt_model")

print("Removed old example models")