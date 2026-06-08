import duckdb

conn = duckdb.connect("olist.db")

# -------------------------
# DIM CUSTOMER
# -------------------------

conn.execute("""
CREATE OR REPLACE TABLE dim_customer AS
SELECT
    customer_id,
    customer_unique_id,
    customer_city,
    customer_state
FROM customers
""")

# -------------------------
# DIM PRODUCT
# -------------------------

conn.execute("""
CREATE OR REPLACE TABLE dim_product AS
SELECT
    product_id,
    product_category_name,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
FROM products
""")

# -------------------------
# DIM SELLER
# -------------------------

conn.execute("""
CREATE OR REPLACE TABLE dim_seller AS
SELECT
    seller_id,
    seller_city,
    seller_state
FROM sellers
""")

# -------------------------
# FACT SALES
# -------------------------

conn.execute("""
CREATE OR REPLACE TABLE fact_sales AS
SELECT
    o.order_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,

    CAST(o.order_purchase_timestamp AS DATE)
        AS purchase_date,

    oi.price,
    oi.freight_value,

    oi.price + oi.freight_value
        AS sales_amount

FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
""")

print("Warehouse tables created successfully!")