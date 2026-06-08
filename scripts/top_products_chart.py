import duckdb
import pandas as pd
import matplotlib.pyplot as plt

# Connect to DuckDB
conn = duckdb.connect("olist.db")

# Query top product categories by revenue
query = """
SELECT
    p.product_category_name,
    SUM(f.sales_amount) AS revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_id = p.product_id
GROUP BY 1
ORDER BY revenue DESC
LIMIT 10
"""

df = conn.sql(query).df()

# Print results to terminal
print("\nTop 10 Product Categories by Revenue")
print(df)

# Create chart
plt.figure(figsize=(12, 6))

plt.barh(
    df["product_category_name"][::-1],
    df["revenue"][::-1]
)

plt.title("Top 10 Product Categories by Revenue")
plt.xlabel("Revenue (BRL)")
plt.ylabel("Product Category")

plt.tight_layout()

# Save chart for portfolio / README
plt.savefig("top_products_chart.png", dpi=300)

# Display chart
plt.show()

print("\nChart saved as: top_products_chart.png")