import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

# 1. Query existing order IDs to avoid duplicate insertions
print(' Retrieving Data... ')
orders_query = 'SELECT DISTINCT order_id FROM fact_sales'
df = pd.read_sql_query(orders_query, engine)
order_ids = set(df['order_id'])

# 2. Ok lets pretend there is new data for today
# Let's create a small df with some new and some already existing order ids
print(f'\n Current orders in database: {len(order_ids)}')
incoming_data = {
    'order_id': [99991, 99992, 10248],  # 10248 Should already exist
    'customer_id': ['ALFKI', 'ANATR', 'VINET'],
    'product_id': [1, 2, 3],
    'quantity': [10, 20, 5],
    'unit_price': [15.0, 25.0, 10.0],
    'line_total': [150.0, 500.0, 50.0]
}

df_append = pd.DataFrame(incoming_data)
print(f'\n Incoming data to process: {len(df_append)}')
# 3. Filter the duplicates and only keep orders not already in the database
df_append_filtered = df_append[~df_append['order_id'].isin(order_ids)]
print(f'\n Filtered new record to insert: {len(df_append_filtered)}')

# 4. Append only the new rows to the database
# index=False ensures pandas doesnt write the dataframe row index as a column
if not df_append_filtered.empty:
    df_append_filtered.to_sql('fact_sales', engine, if_exists='append', index=False)
    print('\n Successfully appended new incremental records to PostgreSQL')
else:
    print('\n No new records to insert. All incoming data already exists')
