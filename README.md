# E-Commerce Data Engineering & Analytics Project

## Overview

This project analyzes the **Brazilian E-Commerce Public Dataset by Olist** using a modern analytics engineering workflow.

The project demonstrates:

* Data ingestion with DuckDB
* Data transformation with dbt
* Data quality testing with dbt tests
* Business analytics with Python and Pandas
* Data visualization with Matplotlib

---

## Tech Stack

| Component           | Technology       |
| ------------------- | ---------------- |
| Data Warehouse      | DuckDB           |
| Data Transformation | dbt              |
| Data Validation     | dbt Tests        |
| Data Analysis       | Python, Pandas   |
| Visualization       | Matplotlib       |
| Documentation       | Jupyter Notebook |

---

## Project Architecture

```text
CSV Files
    ↓
DuckDB
    ↓
dbt Staging Models
    ↓
Star Schema Warehouse
    ↓
dbt Tests
    ↓
Analytics & Visualizations
```

---

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

---

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

---

## Business Analysis

### 1. Monthly Sales Trend

Analyzed revenue trends over time to identify growth patterns and seasonality.

### 2. Top Product Categories

Identified the highest revenue-generating product categories.

### 3. Revenue by State

Compared revenue performance across Brazilian states.

### 4. Customer RFM Analysis

Evaluated customer behavior using:

* Recency
* Frequency
* Monetary Value

---

## Key Findings

* Revenue showed strong growth throughout 2017–2018.
* Beauty & Health was the highest revenue-generating product category.
* São Paulo (SP) generated the highest overall revenue.
* A small group of customers contributed multiple repeat purchases.

---

## Repository Structure

```text
ecommerce-project/
│
├── data/
├── notebooks/
├── scripts/
├── images/
├── dbt_olist/
├── olist.db
└── README.md
```

---

## Conclusion

This project demonstrates an end-to-end analytics engineering workflow, from raw data ingestion and warehouse modeling to data quality validation and business intelligence reporting using DuckDB, dbt, and Python.




### Using the starter project

Try running the following commands:
- dbt run
- dbt test

Get dbt docs
- dbt docs generate
- dbt docs serve


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
