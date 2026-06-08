import duckdb
import pandas as pd
import matplotlib.pyplot as plt

conn = duckdb.connect("olist.db")

query = """
SELECT
    DATE_TRUNC('month', purchase_date) AS sales_month,
    SUM(sales_amount) AS revenue
FROM fact_sales
GROUP BY 1
ORDER BY 1
"""

df = conn.sql(query).df()

print(df)

plt.figure(figsize=(10,5))
plt.plot(df["sales_month"], df["revenue"])
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()

plt.show()