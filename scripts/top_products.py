import duckdb

conn = duckdb.connect("olist.db")

query = """
SELECT
    ct.product_category_name_english,
    SUM(f.sales_amount) AS revenue

FROM fact_sales f

JOIN dim_product p
    ON f.product_id = p.product_id

LEFT JOIN category_translation ct
    ON p.product_category_name =
       ct.product_category_name

GROUP BY 1
ORDER BY revenue DESC
LIMIT 10
"""

df = conn.sql(query).df()

print(df)