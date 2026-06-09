# Olist E-Commerce Analytics Project

## Overview

This project analyzes the Brazilian E-Commerce Public Dataset by Olist. It transforms raw CSV files into a simple analytics warehouse and uses the warehouse to answer business questions about marketplace growth, product performance, geography, and customer retention.

The main fact table, `fact_sales`, is built at the order-item level. Each row represents one product item within an order.

In this project, gross item sales are defined as:

```text
sales_amount = product price + freight value
```

This means the sales metric includes both product value and freight charged to customers. The project therefore analyzes gross item sales, not pure product revenue.

## Tech Stack

| Component | Technology |
|---|---|
| Data Warehouse | DuckDB |
| Data Transformation | dbt |
| Data Validation | dbt Tests |
| Data Analysis | Python, Pandas |
| Visualization | Matplotlib |
| Documentation | Jupyter Notebook |

## Project Architecture

```text
CSV Files
    ->
DuckDB
    ->
dbt Staging Models
    ->
Star Schema Warehouse
    ->
dbt Tests
    ->
Analytics & Visualizations
```

## Data Model

### Fact Table

* `fact_sales`

### Dimension Tables

* `dim_customer`
* `dim_product`
* `dim_seller`

### Staging Models

* `stg_orders`
* `stg_order_items`

## Data Quality Validation

The following dbt tests were implemented:

* Unique customer IDs
* Unique product IDs
* Unique seller IDs
* Non-null customer IDs
* Non-null product IDs
* Non-null seller IDs
* Non-null order IDs

### Results

```text
PASS = 7
WARN = 0
ERROR = 0
```

## Business Analysis

### 1. Monthly Gross Item Sales Trend

Olist grew from a small sales base in late 2016 into a much larger marketplace through 2017 and 2018. Monthly gross item sales increased strongly during 2017, reaching about R$1.18M in November 2017. In 2018, sales remained around the R$1M monthly level, suggesting the business had moved into a more stable operating rhythm after its earlier growth phase.

### 2. Top Product Categories

Gross item sales are concentrated in a few leading categories. Health & Beauty, Watches & Gifts, and Bed/Bath/Table are the top categories, together contributing roughly a quarter of total sales amount. These categories are the commercial core of the marketplace and should be protected through inventory depth, seller quality, promotions, and customer experience improvements.

Because freight is included in `sales_amount`, product-only revenue should also be checked before making category investment decisions, especially for bulky or high-shipping-cost categories.

### 3. Gross Item Sales by State

Gross item sales are heavily concentrated in Southeast Brazil. Sao Paulo is the largest market by far, generating about R$5.9M in gross item sales, roughly three times Rio de Janeiro. RJ and MG are also major contributors.

This supports a strategy of retaining and deepening the strongest markets while evaluating expansion opportunities in states such as RS and PR. Because the sales amount includes freight, regional analysis should be interpreted as a mix of customer demand and delivery cost, not product demand alone.

### 4. Customer RFM Analysis

RFM analysis evaluates customers using:

* Recency: how recently the customer purchased
* Frequency: how often the customer purchased
* Monetary value: how much gross item sales the customer generated

Only about 3.05% of customers are repeat customers, so a normal frequency percentile score can be misleading. This project scores recency and monetary value with quartiles, then uses a more honest frequency score:

```text
1 order = low frequency
2 orders = repeat buyer
3-5 orders = strong repeat buyer
6+ orders = very frequent buyer
```

#### RFM Segment Results

| Segment | Customers | Share | Gross Sales | Campaign Use |
|---|---:|---:|---:|---|
| Recent New Customers | 23,179 | 24.29% | R$1.46M | Second-purchase coupon |
| Core / Mid-Value Customers | 24,071 | 25.23% | R$2.70M | General nurture / category offers |
| Dormant Low Value | 11,959 | 12.53% | R$523k | Low-cost reactivation only |
| At-Risk High Spenders | 11,274 | 11.82% | R$1.59M | Win-back campaign |
| High-Value New Customers | 11,081 | 11.61% | R$4.34M | Priority second-purchase campaign |
| Big Spenders - One-Time Buyers | 10,943 | 11.47% | R$4.32M | Cross-sell / premium recommendation |
| Recent Repeat Buyers | 1,518 | 1.59% | R$453k | Loyalty campaign |
| At-Risk Repeat Buyers | 1,314 | 1.38% | R$402k | Win-back repeat buyers |
| Champions | 81 | 0.08% | R$50k | VIP treatment |

The strongest campaign opportunity is not broad loyalty yet. Most customers bought only once, so the main opportunity is converting valuable one-time buyers into repeat customers.

The best targets are:

1. High-Value New Customers: recent, one-time buyers with high spending. These are ideal for second-purchase offers.
2. At-Risk High Spenders: customers who spent a lot but have not purchased recently. These are good targets for win-back campaigns.
3. Recent Repeat Buyers: customers who have already purchased more than once recently. These are the strongest candidates for loyalty rewards.
4. Champions: a very small group with recent, frequent, high-value behavior. They should receive VIP treatment, early access, or premium offers.

Strong slide message:

> RFM scoring shows that Olist's biggest customer opportunity is converting high-value one-time buyers into repeat customers, while using win-back campaigns for older high-spend customers and loyalty offers for the small repeat-buyer base.

To rerun the RFM segmentation:

```text
python scripts/customer_rfm_segments.py
```

The script writes the latest segment summary to `slices/customer_rfm_segments.csv`.

## Key Findings

* Gross item sales showed strong growth throughout 2017 and then stabilized around the R$1M monthly level in 2018.
* Health & Beauty, Watches & Gifts, and Bed/Bath/Table are the leading gross item sales categories.
* Sao Paulo is the largest market by gross item sales, followed by Rio de Janeiro and Minas Gerais.
* Customer value is concentrated, but repeat purchasing is limited.
* Olist's largest retention opportunity is converting high-value one-time buyers into second-time customers.

## Repository Structure

```text
ecommerce-project/
|-- data/
|-- notebooks/
|-- scripts/
|-- images/
|-- slices/
|-- dbt_olist/
|-- olist.db
|-- README.md
```

## Conclusion

This project tells the story of a growing Brazilian marketplace with strong sales momentum, clear category leaders, Southeast-driven demand, and a major opportunity to improve customer retention. The key caveat is that the project's sales metric is gross item sales including freight, so business recommendations should distinguish between total sales value, product demand, and shipping effects.
