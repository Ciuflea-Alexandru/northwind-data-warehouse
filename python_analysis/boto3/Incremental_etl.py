import os
import boto3
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DB_NAME = os.getenv('AWS_BUCKET_NAME')

oltp_engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_oltp')
olap_engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

# 1. Check what order_ids already exist in OLAP fact_sales table

print(' Checking for new orders to incrementally load into Star Schema ')
existing_orders = "SELECT DISTINCT order_id FROM fact_sales;"
df_existing = pd.read_sql(text(existing_orders), olap_engine)
existing_orders_ids = set(df_existing['order_id'].tolist()) if not df_existing.empty else set()

print(f" Currently loaded orders in Data Warehouse: {len(existing_orders_ids)}")

# 2. Extract fresh orders from source OLTP database
df_orders_raw = pd.read_sql('SELECT order_id, customer_id, order_date FROM orders', oltp_engine)
df_details_raw = pd.read_sql('SELECT order_id, product_id, unit_price, quantity FROM order_details', oltp_engine)

# Calculate line totals
df_details_raw['line_total'] = (
    df_details_raw['unit_price'] *
    df_details_raw['quantity'] *
    (1 - df_details_raw['unit_price'])
)

# Merge orders and details
df_sales_all = df_orders_raw.merge(df_details_raw, on='order_id')

# 3. Filter to keep only orders that are not already in our star schema

df_new_sales = df_sales_all[~df_sales_all['order_id'].isin(existing_orders_ids)]

if df_new_sales.empty:
    print(' No new data found. We are up to date! ')
else:
    print(f" Found {len(df_new_sales)} new order line items to load ")

    df_new_sales['order_date'] = pd.to_datetime(df_new_sales['order_date'])
    df_new_sales['date_key'] = df_new_sales['order_date'].dt.strftime('%y%m%d').astype(int)

    # Drop raw date timestamp to match strict star schema rules

    df_new_sales = df_new_sales.drop(columns=['order_date'])

    # Append only the new rows to fact_sales
    df_new_sales.to_sql('fact_sales', olap_engine, if_exists='append', index=False)
    print("Successfully appended new sales data into fact_sales star schema")
