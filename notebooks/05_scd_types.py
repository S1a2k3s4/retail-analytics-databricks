-- Databricks notebook source
-- MAGIC %md
-- MAGIC #SCD Type 1 / Type 2

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC source_data = [
-- MAGIC     ("C001", "Rahul", "Mumbai", "Maharashtra"),
-- MAGIC     ("C002", "Priya", "Mumbai", "Maharashtra"),
-- MAGIC     ("C006", "Sneha", "Pune", "Maharashtra")
-- MAGIC ]
-- MAGIC
-- MAGIC columns = ["customer_id", "name", "city", "state"]
-- MAGIC
-- MAGIC source_customers = spark.createDataFrame(
-- MAGIC     source_data,
-- MAGIC     columns
-- MAGIC )
-- MAGIC
-- MAGIC display(source_customers)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC source_customers.createOrReplaceTempView("source_customers")

-- COMMAND ----------

SELECT *
FROM source_customers;

-- COMMAND ----------

MERGE INTO retail_analytics.silver.customers AS target

USING source_customers AS source

ON target.customer_id = source.customer_id

WHEN MATCHED THEN
    UPDATE SET
        target.name = source.name,
        target.city = source.city,
        target.state = source.state

WHEN NOT MATCHED THEN
    INSERT (customer_id, name, city, state, ingestion_timestamp) VALUES (source.customer_id, source.name, source.city, source.state, CURRENT_TIMESTAMP)

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS retail_analytics.silver.customer_history (
    customer_id STRING,
    name STRING,
    city STRING,
    state STRING,
    effective_date DATE,
    end_date DATE,
    is_current BOOLEAN
)
USING DELTA;

-- COMMAND ----------

DESCRIBE HISTORY retail_analytics.silver.orders;

-- COMMAND ----------

Select *
From retail_analytics.silver.orders 
version as of 1;

-- COMMAND ----------

Select * 
from retail_analytics.silver.orders 
version as of 2;