-- Databricks notebook source
-- MAGIC %md
-- MAGIC #Clean, validate, transform Bronze → Silver

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customers=spark.table("retail_analytics.bronze.customers")
-- MAGIC products=spark.table("retail_analytics.bronze.products")
-- MAGIC orders=spark.table("retail_analytics.bronze.orders")

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql import functions as F
-- MAGIC customers_clean=(
-- MAGIC     customers.withColumn("name",F.trim(F.col("name")))
-- MAGIC     .withColumn("city",F.trim(F.col("city")))
-- MAGIC     .withColumn("state",F.trim(F.col("state")))
-- MAGIC )

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customers_clean=customers_clean.fillna({"city":"unknown","state":"unknown"})

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customers_clean=customers_clean.dropDuplicates(["customer_id"])

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #clean products

-- COMMAND ----------

-- MAGIC %python
-- MAGIC products_clean=products.withColumn("product_name",F.trim("product_name")).withColumn("category",F.trim("category"))

-- COMMAND ----------

-- MAGIC %python
-- MAGIC display(products_clean)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC products_clean=products_clean.dropDuplicates(["product_id"])

-- COMMAND ----------

-- MAGIC %python
-- MAGIC display(products_clean.filter(F.col("price")>=7000))

-- COMMAND ----------

-- MAGIC %python
-- MAGIC display(products_clean.select("category").distinct())

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC products_clean=products_clean.withColumn("revenue",F.col("price")*10)
-- MAGIC display(products_clean)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC display(products_clean.withColumn("name_length", F.length(F.col("product_name"))))

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC products_clean=(products_clean.withColumn("category",F.upper(F.trim(F.col("category")))))
-- MAGIC display(products_clean)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC display(products_clean.filter(F.length(F.col("product_name"))<3))

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #clean orders

-- COMMAND ----------

-- MAGIC %python
-- MAGIC orders_clean=orders.dropDuplicates(["order_id"])

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql import functions as F
-- MAGIC display(orders_clean.filter(F.col("quantity")<=0))

-- COMMAND ----------

-- MAGIC %python
-- MAGIC display(orders_clean.filter(F.col("order_date").isNull()))

-- COMMAND ----------

-- MAGIC %python
-- MAGIC invalid_quantity=orders_clean.filter(F.col("quantity")<=0)
-- MAGIC print("Invalid Quantity",invalid_quantity.count())

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC invalid_orders=orders_clean.filter((F.col("order_id").isNull())|(F.col("quantity")<=0))

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC invalid_orders.write.format("delta").mode("append").saveAsTable("retail_analytics.bronze.invaild_orders")

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC valid_orders=orders_clean.filter((F.col("order_id").isNotNull())&(F.col("quantity")>0))

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #Write Silver Table

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customers_clean.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.silver.customers")
-- MAGIC
-- MAGIC products_clean.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.silver.products")
-- MAGIC
-- MAGIC valid_orders.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.silver.orders")
-- MAGIC
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC create silver sales table

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC sales = (orders.join(customers, "customer_id", "inner")
-- MAGIC     .join(products, "product_id", "inner")
-- MAGIC     .withColumn("revenue", F.col("quantity") * F.col("price"))
-- MAGIC     .select("order_id", "customer_id", "name", "city", "state", "product_id", "product_name", "category", "quantity", "price", "revenue", "order_date"))
-- MAGIC
-- MAGIC sales.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.silver.sales")