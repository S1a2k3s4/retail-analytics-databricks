-- Databricks notebook source
-- MAGIC %md
-- MAGIC #Business transformations → Gold

-- COMMAND ----------

-- MAGIC %python
-- MAGIC sales=spark.table("retail_analytics.silver.sales")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Gold - Daily Sales

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql import functions as F
-- MAGIC daily_sales=sales.groupBy("order_date").agg(
-- MAGIC     F.sum("revenue").alias("total_revenue"),
-- MAGIC     F.countDistinct("order_id").alias("total_orders"),
-- MAGIC     F.sum("quantity").alias("total_quantity")
-- MAGIC )

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC daily_sales.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.gold.daily_sales")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Gold - Monthly Sales

-- COMMAND ----------

-- MAGIC %python
-- MAGIC monthly_sales=sales.withColumn("month",F.date_format("order_date","yyyy-MM")).groupBy("month").agg(
-- MAGIC     F.sum("revenue").alias("total_revenue"),
-- MAGIC
-- MAGIC     F.countDistinct("order_id").alias("total_orders"),
-- MAGIC     F.sum("quantity").alias("total_quantity")
-- MAGIC )

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC monthly_sales.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.gold.monthly_sales")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Gold - Product Sales

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC product_sales=sales.groupBy("product_id","product_name","category").agg(
-- MAGIC     F.sum("quantity").alias("units_sold"),
-- MAGIC     F.sum("revenue").alias("total_revenue"),
-- MAGIC     F.countDistinct("order_id").alias("total_orders")
-- MAGIC )

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC product_sales.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.gold.product_sales")
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Gold - Customer Sales

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customer_sales=sales.groupBy("customer_id","name","city").agg(
-- MAGIC     F.countDistinct("order_id").alias("total_orders"),
-- MAGIC     F.sum('quantity').alias("total_quantity"),
-- MAGIC     F.sum("revenue").alias("total_revenue")
-- MAGIC )

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC customer_sales.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.gold.customer_sales")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC Gold - City Sales

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC city_sales=sales.groupBy("city","state").agg(
-- MAGIC     F.sum("revenue").alias("total_revenue"),
-- MAGIC     F.countDistinct("order_id").alias("total_orders")
-- MAGIC )

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC city_sales.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.gold.city_sales")

-- COMMAND ----------

SHOW TABLES IN retail_analytics.gold;

-- COMMAND ----------

Select * from retail_analytics.gold.daily_sales
order by order_date;

-- COMMAND ----------

