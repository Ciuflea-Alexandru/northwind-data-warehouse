import os
import boto3
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

print(' Retrieving data... ')

query = """
SELECT
c.customer_id,
c.company_name,
SUM(f.line_total) AS total_spend,
COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.company_name
"""

df_metrics = pd.read_sql(query, engine)
print(df_metrics.head(5))

print('\n Sorting customers into respective categories... ')

conditions = [
    df_metrics['total_spend'] < 1000,
    (df_metrics['total_spend'] >= 1000) & (df_metrics['total_spend'] < 5000),
    df_metrics['total_spend'] >= 5000
]

choices = ['Standard', 'Regular', 'VIP']

df_metrics['tier'] = np.select(conditions, choices, default='Standard')
print(df_metrics.head(5))

print('\n Saving the data frame on cloud as a CSV extension... ')
path = 'target_loyalty_campaign.csv'
df_metrics.to_csv(path, index=False)

s3 = boto3.client('s3')
bucket = os.getenv('AWS_BUCKET_NAME')
s3_path = f"processed/reports/target_loyalty_campaign.csv"

s3.upload_file(path, bucket, s3_path)

if os.path.isfile('target_loyalty_campaign.csv'):
    os.remove('target_loyalty_campaign.csv')

print('\n Retrieving data from the s3... ')
read_s3 = f"s3://{bucket}/{s3_path}"
df_s3 = pd.read_csv(read_s3)
print(df_s3.head(5))

