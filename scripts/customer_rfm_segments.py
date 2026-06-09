from pathlib import Path

import duckdb


DB_PATH = Path("olist.db")
OUTPUT_PATH = Path("slices/customer_rfm_segments.csv")


RFM_QUERY = """
WITH customer_rfm AS (
    SELECT
        c.customer_unique_id,
        MAX(f.purchase_date) AS last_purchase,
        COUNT(DISTINCT f.order_id) AS frequency,
        SUM(f.sales_amount) AS monetary
    FROM fact_sales f
    JOIN dim_customer c
        ON f.customer_id = c.customer_id
    GROUP BY 1
),
scored AS (
    SELECT
        customer_unique_id,
        last_purchase,
        DATE_DIFF(
            'day',
            last_purchase,
            (SELECT MAX(purchase_date) + INTERVAL 1 DAY FROM fact_sales)
        ) AS recency_days,
        frequency,
        monetary,
        NTILE(4) OVER (
            ORDER BY DATE_DIFF(
                'day',
                last_purchase,
                (SELECT MAX(purchase_date) + INTERVAL 1 DAY FROM fact_sales)
            ) DESC, customer_unique_id
        ) AS recency_score,
        CASE
            WHEN frequency = 1 THEN 1
            WHEN frequency = 2 THEN 2
            WHEN frequency BETWEEN 3 AND 5 THEN 3
            ELSE 4
        END AS frequency_score,
        NTILE(4) OVER (ORDER BY monetary, customer_unique_id) AS monetary_score
    FROM customer_rfm
),
segmented AS (
    SELECT
        *,
        CASE
            WHEN recency_score = 4
                AND frequency_score >= 3
                AND monetary_score >= 3
                THEN 'Champions'
            WHEN recency_score >= 3
                AND frequency_score >= 2
                THEN 'Recent Repeat Buyers'
            WHEN recency_score <= 2
                AND frequency_score >= 2
                THEN 'At-Risk Repeat Buyers'
            WHEN recency_score >= 3
                AND frequency_score = 1
                AND monetary_score = 4
                THEN 'High-Value New Customers'
            WHEN recency_score <= 2
                AND frequency_score = 1
                AND monetary_score = 4
                THEN 'Big Spenders - One-Time Buyers'
            WHEN recency_score <= 2
                AND frequency_score = 1
                AND monetary_score = 3
                THEN 'At-Risk High Spenders'
            WHEN recency_score >= 3
                AND frequency_score = 1
                AND monetary_score <= 2
                THEN 'Recent New Customers'
            WHEN recency_score <= 2
                AND frequency_score = 1
                AND monetary_score = 1
                THEN 'Dormant Low Value'
            ELSE 'Core / Mid-Value Customers'
        END AS segment
    FROM scored
),
summary AS (
    SELECT
        segment,
        COUNT(*) AS customers,
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS share,
        SUM(monetary) AS gross_sales
    FROM segmented
    GROUP BY 1
)
SELECT
    segment,
    customers,
    ROUND(share, 2) AS share_pct,
    ROUND(gross_sales, 2) AS gross_sales,
    CASE segment
        WHEN 'Recent New Customers'
            THEN 'Second-purchase coupon'
        WHEN 'Core / Mid-Value Customers'
            THEN 'General nurture / category offers'
        WHEN 'Dormant Low Value'
            THEN 'Low-cost reactivation only'
        WHEN 'At-Risk High Spenders'
            THEN 'Win-back campaign'
        WHEN 'High-Value New Customers'
            THEN 'Priority second-purchase campaign'
        WHEN 'Big Spenders - One-Time Buyers'
            THEN 'Cross-sell / premium recommendation'
        WHEN 'Recent Repeat Buyers'
            THEN 'Loyalty campaign'
        WHEN 'At-Risk Repeat Buyers'
            THEN 'Win-back repeat buyers'
        WHEN 'Champions'
            THEN 'VIP treatment'
    END AS campaign_use
FROM summary
ORDER BY
    CASE segment
        WHEN 'Recent New Customers' THEN 1
        WHEN 'Core / Mid-Value Customers' THEN 2
        WHEN 'Dormant Low Value' THEN 3
        WHEN 'At-Risk High Spenders' THEN 4
        WHEN 'High-Value New Customers' THEN 5
        WHEN 'Big Spenders - One-Time Buyers' THEN 6
        WHEN 'Recent Repeat Buyers' THEN 7
        WHEN 'At-Risk Repeat Buyers' THEN 8
        WHEN 'Champions' THEN 9
    END
"""


REPEAT_QUERY = """
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT f.order_id) AS frequency
    FROM fact_sales f
    JOIN dim_customer c
        ON f.customer_id = c.customer_id
    GROUP BY 1
)
SELECT
    COUNT(*) AS customers,
    SUM(CASE WHEN frequency > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    SUM(CASE WHEN frequency > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*)
        AS repeat_customer_share
FROM customer_orders
"""


def format_currency(value):
    if value >= 1_000_000:
        return f"R${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"R${value / 1_000:.0f}k"
    return f"R${value:.0f}"


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError("olist.db was not found. Run this script from the project root.")

    conn = duckdb.connect(str(DB_PATH))
    rows = conn.sql(RFM_QUERY).fetchall()
    repeat_stats = conn.sql(REPEAT_QUERY).fetchone()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn.sql(RFM_QUERY).write_csv(str(OUTPUT_PATH))

    print("RFM Segment Results")
    print()
    print("| Segment | Customers | Share | Gross Sales | Campaign Use |")
    print("|---|---:|---:|---:|---|")
    for segment, customers, share, gross_sales, campaign_use in rows:
        print(
            f"| {segment} | {customers:,} | {share:.2f}% | "
            f"{format_currency(gross_sales)} | {campaign_use} |"
        )

    total_customers, repeat_customers, repeat_share = repeat_stats
    print()
    print(
        f"Repeat customers: {repeat_customers:,} of {total_customers:,} "
        f"({repeat_share:.2f}%)."
    )
    print()
    print(
        "Method note: frequency is bucketed as 1 order, 2 orders, "
        "3-5 orders, and 6+ orders because repeat purchasing is rare."
    )
    print(f"Saved segment summary to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
