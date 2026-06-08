import duckdb

conn = duckdb.connect("olist.db")

query = """
SELECT
    c.customer_unique_id,

    MAX(f.purchase_date) AS last_purchase,

    COUNT(DISTINCT f.order_id) AS frequency,

    SUM(f.sales_amount) AS monetary

FROM fact_sales f

JOIN dim_customer c
    ON f.customer_id = c.customer_id

GROUP BY c.customer_unique_id

ORDER BY frequency DESC

LIMIT 20
"""

df = conn.sql(query).df()

print(df)