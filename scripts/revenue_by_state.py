import duckdb

conn = duckdb.connect("olist.db")

query = """
SELECT
    c.customer_state,
    SUM(f.sales_amount) revenue

FROM fact_sales f

JOIN dim_customer c
    ON f.customer_id = c.customer_id

GROUP BY 1
ORDER BY revenue DESC
"""

df = conn.sql(query).df()

print(df)