-- Databricks notebook source
-- MAGIC %md
-- MAGIC #Incremental/CDC-style loading

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC from pyspark.sql import functions as F
-- MAGIC new_orders=spark.read.option("header","true").option("inferSchema","true").csv("s3://retail-analytics-dataa/raw/orders_2026_10_02.csv") 
-- MAGIC
-- MAGIC new_orders=(
-- MAGIC     new_orders
-- MAGIC     .withColumn("ingestion_timestamp", F.current_timestamp())
-- MAGIC     .withColumn("source_file", F.col("_metadata.file_path"))
-- MAGIC
-- MAGIC )
-- MAGIC

-- COMMAND ----------

-- MAGIC %python
-- MAGIC display(new_orders)

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC new_orders.createOrReplaceTempView("new_orders")

-- COMMAND ----------

Select * from new_orders;

-- COMMAND ----------

MERGE INTO retail_analytics.silver.orders AS target

USING new_orders AS source

ON target.order_id = source.order_id

WHEN MATCHED THEN
    UPDATE SET *

WHEN NOT MATCHED THEN
    INSERT *;

-- COMMAND ----------

Select * 
from retail_analytics.silver.orders 
order by order_date;

-- COMMAND ----------

