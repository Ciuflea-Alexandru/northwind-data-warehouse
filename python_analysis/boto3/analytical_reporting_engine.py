import os
import boto3
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
bucket_name = os.getenv('AWS_BUCKET_NAME')

olap_engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

print('\n Running Analytical Queries against the Northwind Star Schema')

# 1. Top 5 customers by total revenue
top_customers = """
SELECT
c.company_name,
c.country,
SUM(f.line_total) AS total_revenue,
SUM(f.quantity) AS total_items_bought
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.company_name, c.country
ORDER BY total_revenue DESC
LIMIT 5;
"""

df_top_customers = pd.read_sql(text(top_customers), olap_engine)

print(' Top 5 Customers by Revenue:')
print(df_top_customers.to_string(index=False))
print("-" * 50)

# 2. Monthly Sales Trends using dim_time

monthly_sales = """
SELECT
t.year,
t.month,
SUM(f.line_total) AS monthly_revenue,
COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_sales f
JOIN dim_time t ON f.date_key = t.date_key
GROUP BY t.year, t.month
ORDER BY t.year, t.month;
"""

df_monthly_sales = pd.read_sql(text(monthly_sales), olap_engine)

print(' Monthly Revenue Trends:')
print(df_monthly_sales.to_string(index=False))
print("-" * 50)

# 3. Save both reports locally as temporary parquet files, then upload to s3
s3_client = boto3.client('s3')

reports = {
    'processed/reports/top_customers.parquet': df_top_customers,
    'processed/reports/monthly_sales.parquet': df_monthly_sales,
}

for s3_path_key, df in reports.items():
    temp_filename = 'temp_report.parquet'
    df.to_parquet(temp_filename, index=False)

    print(f" Uploading report to s3://{bucket_name}/{temp_filename}")
    s3_client.upload_file(temp_filename, bucket_name, s3_path_key)

    if os.path.exists(temp_filename):
        os.remove(temp_filename)

print('\n All analytical report successfully generated and uploaded to S3!')
