-- Databricks notebook source
-- MAGIC %md
-- MAGIC #Optimize tables and Final table/data validation

-- COMMAND ----------

OPTIMIZE retail_analytics.silver.orders;

-- COMMAND ----------

DESCRIBE DETAIL retail_analytics.silver.orders;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC orders=spark.table("retail_analytics.silver.orders")
-- MAGIC products=spark.table("retail_analytics.silver.products")
-- MAGIC sales=orders.join(products,orders.product_id==products.product_id,"left")
-- MAGIC
-- MAGIC sales.explain(True)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql.functions import broadcast
-- MAGIC
-- MAGIC sales=orders.join(broadcast(products),orders.product_id==products.product_id,"left")