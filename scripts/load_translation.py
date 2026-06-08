import duckdb

conn = duckdb.connect("olist.db")

conn.execute("""
CREATE OR REPLACE TABLE category_translation AS
SELECT *
FROM read_csv_auto(
'data/product_category_name_translation.csv'
)
""")

print("Translation table loaded")