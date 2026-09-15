import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, to_date

load_dotenv()
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("AWS_BUCKET_NAME")

# 1. Initialize Spark Session with AWS S3 credentials configured
# Spark needs explicit Hadoop/AWS configurations to securely talk to S3

spark = SparkSession.builder \
    .appName('NorthwindPySparkS3Processing') \
    .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262') \
    .config('spark.hadoop.fs.s3a.access.key', aws_access_key) \
    .config('spark.hadoop.fs.s3a.secret.key', aws_secret_key) \
    .config('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem') \
    .getOrCreate()

print(f'\n Spark Session initialized successfully')

# 2. Read the raw Parquet directly from S3 using s3a:// protocol

s3_input_path = f"s3a://{bucket_name}/raw/orders/orders_raw.parquet"
print(f"\n Reading data from S3: {s3_input_path}")

df_spark = spark.read.parquet(s3_input_path)

# Show schema and count to prove Spark is processing it
print(f"\n Total rows loaded into Spark: {df_spark.count()}")
df_spark.printSchema()

# 3. Perform a distributed transformation

df_transformed = df_spark \
    .withColumn('order_date_parsed', to_date(col('order_date'))) \
    .withColumn('order_year', year(col('order_date_parsed'))) \
    .filter("order_year >= 1996")

# 4. Write back to s3

s3_output_path = f"s3a://{bucket_name}/processed/orders_transformed/"
print(f"\n Writing transformed data back to s3: {s3_output_path}")

df_transformed.write \
    .mode('overwrite') \
    .parquet(s3_output_path)

print(f"\n PySpark distributed processing pipeline completed successfully!")
spark.stop()
