-- Databricks notebook source
-- MAGIC %md
-- MAGIC #Ingest raw data from S3 → Bronze

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC from pyspark.sql import functions as F
-- MAGIC
-- MAGIC from pyspark.sql.types import(
-- MAGIC     StructType,
-- MAGIC     StructField,
-- MAGIC     StringType,
-- MAGIC     IntegerType,
-- MAGIC     DoubleType,
-- MAGIC     DataType
-- MAGIC )

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customers_path="s3://retail-analytics-dataa/raw/customers.csv"
-- MAGIC products_path="s3://retail-analytics-dataa/raw/products.csv"
-- MAGIC orders_path="s3://retail-analytics-dataa/raw/orders.csv"
-- MAGIC

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customer_schema=StructType([
-- MAGIC     StructField("customer_id",StringType(),False),
-- MAGIC     StructField("name",StringType(),True),
-- MAGIC     StructField("city",StringType(),True),
-- MAGIC     StructField("state",StringType(),True)
-- MAGIC ])

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customers_df=(
-- MAGIC     spark.read
-- MAGIC     .option("header","true")
-- MAGIC     .schema(customer_schema)
-- MAGIC     .csv(customers_path)
-- MAGIC )

-- COMMAND ----------

-- MAGIC %python
-- MAGIC display(customers_df)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customers_df.printSchema()

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customers_df=customers_df.withColumn("ingestion_timestamp",F.current_timestamp()).withColumn("source_file",F.input_file_name())

-- COMMAND ----------

-- MAGIC %python
-- MAGIC customers_df = (
-- MAGIC     customers_df
-- MAGIC     .withColumn("ingestion_timestamp", F.current_timestamp())
-- MAGIC     .withColumn("source_file", F.col("_metadata.file_path"))
-- MAGIC )

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC customers_df = (
-- MAGIC     spark.read
-- MAGIC     .option("header", "true")
-- MAGIC     .schema(customer_schema)
-- MAGIC     .csv(customers_path)
-- MAGIC     .withColumn("ingestion_timestamp", F.current_timestamp())
-- MAGIC     .withColumn("source_file", F.col("_metadata.file_path"))
-- MAGIC )
-- MAGIC customers_df.write \
-- MAGIC     .format("delta") \
-- MAGIC     .mode("overwrite") \
-- MAGIC     .saveAsTable("retail_analytics.bronze.customers")

-- COMMAND ----------

Select * from retail_analytics.bronze.customers;

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql import functions as F
-- MAGIC products_df=(
-- MAGIC     spark.read
-- MAGIC     .option("header","true")
-- MAGIC     .option("inferSchema","true")
-- MAGIC     .csv(products_path)
-- MAGIC )
-- MAGIC products_df=(
-- MAGIC     products_df
-- MAGIC     .withColumn("ingestion_timestamp", F.current_timestamp())
-- MAGIC     .withColumn("source_file", F.col("_metadata.file_path"))
-- MAGIC
-- MAGIC )
-- MAGIC display(products_df)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC products_df.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.bronze.products")

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql import functions as f
-- MAGIC
-- MAGIC orders_df=spark.read.option("header","true").option("inferSchema","true").csv(orders_path)
-- MAGIC
-- MAGIC orders_df=(
-- MAGIC     orders_df
-- MAGIC     .withColumn("ingestion_timestamp", F.current_timestamp())
-- MAGIC     .withColumn("source_file", F.col("_metadata.file_path"))
-- MAGIC
-- MAGIC )
-- MAGIC display(orders_df)
-- MAGIC

-- COMMAND ----------

-- MAGIC %python
-- MAGIC orders_df.write.format("delta").mode("overwrite").saveAsTable("retail_analytics.bronze.orders")

-- COMMAND ----------

Show tables in retail_analytics.bronze;

-- COMMAND ----------

Select * from retail_analytics.bronze.orders;

-- COMMAND ----------

Select * from retail_analytics.bronze.customers;

-- COMMAND ----------

SELECT * from retail_analytics.bronze.products;