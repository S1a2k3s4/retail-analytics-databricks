-- Databricks notebook source
-- MAGIC %md
-- MAGIC #Null checks, duplicate checks, validation

-- COMMAND ----------

Select * 
from retail_analytics.silver.orders 
where order_id is NULL;

-- COMMAND ----------

Select order_id,count(*) as count 
from retail_analytics.silver.orders 
group by order_id 
having count(*)>1;

-- COMMAND ----------

Select * 
from retail_analytics.silver.orders 
where quantity<=0;

-- COMMAND ----------

Select * 
from retail_analytics.silver.products 
where price<=0;

-- COMMAND ----------

Select o.*
From retail_analytics.silver.orders o 
Left Join retail_analytics.silver.customers c 
on o.customer_id=c.customer_id 
where c.customer_id is null;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql import functions as F
-- MAGIC orders=spark.table("retail_analytics.silver.orders")
-- MAGIC
-- MAGIC total_orders=orders.count()
-- MAGIC null_order_ids=orders.filter(
-- MAGIC     F.col("order_id").isNull()
-- MAGIC ).count()
-- MAGIC
-- MAGIC invalid_quantity=orders.filter(
-- MAGIC     F.col("quantity")<=0
-- MAGIC ).count()
-- MAGIC
-- MAGIC print("Total records:",total_orders)
-- MAGIC print("Null order IDs:",null_order_ids)
-- MAGIC print("Invalid quantity:",invalid_quantity)