import duckdb

conn = duckdb.connect("olist.db")

query = """
SELECT
    customer_id,

    MAX(purchase_date) AS last_purchase,

    COUNT(DISTINCT order_id) AS frequency,

    SUM(sales_amount) AS monetary

FROM fact_sales

GROUP BY customer_id

ORDER BY monetary DESC

LIMIT 20
"""

df = conn.sql(query).df()

print(df)