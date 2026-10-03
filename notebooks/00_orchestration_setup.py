# Databricks notebook source
# DBTITLE 1,Pipeline Overview
# MAGIC %md
# MAGIC # Pipeline Orchestration Setup
# MAGIC
# MAGIC This notebook initializes the catalog and schemas for the **Retail Analytics Daily Pipeline**.
# MAGIC
# MAGIC **Pipeline Flow:**
# MAGIC 1. `bronze_ingestion` — Ingest raw CSV data from S3 into bronze layer
# MAGIC 2. `silver_transformation` — Clean and transform bronze data into silver layer
# MAGIC 3. `data_quality` — Validate silver layer tables (nulls, duplicates, referential integrity)
# MAGIC 4. `incremental_loading` — MERGE new orders into silver layer
# MAGIC 5. `scd_types` — Apply SCD Type 1 & Type 2 on customer dimensions
# MAGIC 6. `gold_reporting` — Build gold aggregation tables from final silver state
# MAGIC 7. `optimization` — Optimize Delta tables and analyze query performance

# COMMAND ----------

# DBTITLE 1,Initialize Catalog and Schemas
# Create the catalog and schemas if they don't exist
print("=== Retail Analytics Pipeline — Setup ===")
print("Initializing catalog and schemas...")

# Create catalog
spark.sql("CREATE CATALOG IF NOT EXISTS retail_analytics")
print("✓ Catalog 'retail_analytics' ready")

# Create schemas
for schema in ["bronze", "silver", "gold"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS retail_analytics.{schema}")
    print(f"✓ Schema 'retail_analytics.{schema}' ready")

print("\n=== Setup complete. Pipeline ready to run. ===")

# COMMAND ----------

