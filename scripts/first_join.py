import duckdb

conn = duckdb.connect("olist.db")

query = """
SELECT
    o.order_id,
    o.customer_id,
    o.order_purchase_timestamp,
    oi.product_id,
    oi.seller_id,
    oi.price,
    oi.freight_value
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
LIMIT 10
"""

print(conn.sql(query).df())