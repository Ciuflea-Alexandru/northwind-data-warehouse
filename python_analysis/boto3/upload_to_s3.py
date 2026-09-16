import os
import boto3
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

oltp_engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_oltp')

print(' Extracting raw data to upload to S3... ')
df_orders = pd.read_sql('SELECT * FROM orders', oltp_engine)

local_file = "orders_raw.parquet"
df_orders.to_parquet(local_file, index=False)

s3_client = boto3.client('s3')
bucket_name = os.getenv('AWS_BUCKET_NAME')
s3_file_key = 'raw/orders/orders_raw.parquet'

print(f" Uploading {local_file} to S3 bucket '{bucket_name}'... ")
s3_client.upload_file(local_file, bucket_name, s3_file_key)

print(f" Successfully uploaded to s3://{bucket_name}/{s3_file_key}")
if os.path.exists(local_file):
    os.remove(local_file)

s3_path = f"s3://{bucket_name}/{s3_file_key}"
df_from_cloud = pd.read_parquet(s3_path)

print(f"\n Data successfully pulled from S3: ")
print(f"\n {df_from_cloud.head()}")
