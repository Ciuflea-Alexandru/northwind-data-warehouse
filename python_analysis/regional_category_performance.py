import pandas as pd
from sqlalchemy import create_engine

print(' Retrieving Data... ')
engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

query = """
SELECT
    c.country,
    p.category_name,
    SUM(f.line_total) AS total_revenue,
    SUM(f.quantity) AS total_units,
    COUNT(DISTINCT f.order_id) AS unique_orders
FROM fact_sales f
         JOIN dim_customers c ON c.customer_id = f.customer_id
         JOIN dim_products p ON p.product_id = f.product_id
GROUP BY country, category_name
"""

df = pd.read_sql(query, engine)
print(df.head(5))

print('\n Filtering Data... ')
df_filtered = df[
    (df['total_revenue'] > 10000) &
    (df['unique_orders'] > 10)
]
print(df_filtered.head(5))

print('\n Sorting Data... ')
df_sorted = df_filtered.sort_values(by='total_revenue', ascending=False)

print(df_sorted.head(5))
