from pyspark.sql import SparkSession, functions as f

spark = SparkSession.builder \
    .appName('NorthwindOLAP_PySpark_Analysis') \
    .config('spark.jars.packages', 'org.postgresql:postgresql:42.6.0') \
    .getOrCreate()

print(f'\n Spark Session initialized successfully! ')

db_engine = 'jdbc:postgresql://localhost:5432/northwind_olap'
db_properties = {
    'user': 'postgres',
    'password': '12345',
    'driver': 'org.postgresql.Driver'
}

print(f'\n Reading star schema tables into Spark DataFrames... ')

df_fact_sales = spark.read.jdbc(url=db_engine, table='fact_sales', properties=db_properties)
df_dim_customers = spark.read.jdbc(url=db_engine, table='dim_customers', properties=db_properties)
df_dim_products = spark.read.jdbc(url=db_engine, table='dim_products', properties=db_properties)

print('\n Joining Fact_Sales with Dimensions using PySpark API... ')
df_enriched_sales = df_fact_sales \
    .join(df_dim_customers, 'customer_id') \
    .join(df_dim_products, 'product_id')

df_summary = df_enriched_sales.groupBy('country', 'category_name') \
    .agg(
    f.sum('line_total').alias('total_revenue'),
    f.sum('quantity').alias('total_units_sold'),
    f.countDistinct('order_id').alias('total_orders')
) \
    .orderBy(f.desc('total_revenue'))

print(f'\n Top 10 Category & Country Revenue Performance... ')
df_summary.show(10, truncate=False)

spark.stop()
