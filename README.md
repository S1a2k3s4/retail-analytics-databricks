# Retail Analytics Data Engineering Project

## Overview

An end-to-end retail analytics data engineering project built using AWS S3, Databricks, PySpark, SQL, Delta Lake, Unity Catalog, and Databricks Workflows.

The project demonstrates a production-style Bronze-Silver-Gold data pipeline with incremental loading, SCD Type 1 and Type 2, data quality validation, business reporting, and query optimization.

---

Technologies
AWS S3
Databricks
PySpark
Python
SQL
Delta Lake
Unity Catalog
Databricks Workflows

---

Pipeline Flow
1. Bronze Ingestion

Raw customer, product, and order data is ingested from AWS S3 into Bronze Delta tables.

2. Incremental Loading

New data is processed incrementally using Delta Lake and MERGE operations.

3. Silver Transformation

Data is cleaned, validated, deduplicated, joined, and transformed into business-ready datasets.

4. SCD Type 1

Customer records are updated to maintain the latest/current state.

5. SCD Type 2

Historical customer changes are tracked using:

effective_date
end_date
is_current
6. Data Quality

Data quality checks include:

Null checks
Duplicate checks
Invalid quantities
Invalid dates
Invalid prices
Invalid customer IDs
Invalid product IDs
7. Gold Reporting

Business-ready reporting tables are created for:

Daily sales
Monthly sales
Product sales
Customer sales
City sales
8. Optimization

The project demonstrates:

Broadcast joins
Query plan analysis using EXPLAIN
Photon execution
Delta OPTIMIZE
Delta Time Travel

---

Databricks Workflow-


orchestration_setup
        |
        v
bronze_ingestion
        |
        v
incremental_loading
        |
        v
silver_transformation
        |
        v
scd_types
        |
        v
data_quality
        |
        v
gold_reporting

optimization