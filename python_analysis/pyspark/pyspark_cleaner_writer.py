import os
import shutil
from pyspark.sql import SparkSession, functions as f

spark = SparkSession.builder \
    .appName('Transformation_Pipeline') \
    .config('spark.jars.packages', 'org.postgresql:postgresql:42.6.0') \
    .getOrCreate()

db_url = 'jdbc:postgresql://localhost:5432/northwind_olap'
db_properties = {
    'user': 'postgres',
    'password': '12345',
    'driver': 'org.postgresql.Driver'
}

print('\n Retrieving Data... ')
df_sales = spark.read.jdbc(url=db_url, table='fact_sales', properties=db_properties)
df_sales.show(5, truncate=False)

print('\n Cleaning and transforming data... ')
df_cleaned = df_sales \
    .filter(f.col('unit_price') > 0) \
    .filter(f.col('quantity') > 0) \
    .withColumn('total_discount_amount', f.col('unit_price') * f.col('quantity') * f.col('discount')) \
    .withColumn('is_high_value_order', f.when(f.col('line_total') > 500, 'Yes').otherwise('No'))
df_cleaned.show(5, truncate=False)

print('\n Aggregating customers spend summary... ')
df_customer_summary = df_cleaned.groupBy('customer_id') \
    .agg(
    f.sum('line_total').alias('lifetime_spend'),
    f.count('order_id').alias('total_orders')
) \
    .orderBy(f.desc('lifetime_spend'))

print('\n Top 5 Customers by lifetime spend')
df_customer_summary.show(5, truncate=False)

print('\n Writing transformed dataset locally to parquet format')
output_path = 'processed_sales_parquet'
df_cleaned.write \
    .mode('overwrite') \
    .parquet(output_path)

spark.stop()

if os.path.exists(output_path):
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
    else:
        os.remove(output_path)