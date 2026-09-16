import pandas as pd
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)
pd.set_option("display.width", 10000)

print(' Retrieving Data... ')
engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

query = """
WITH customer_summary AS (
SELECT
    c.customer_id,
    c.company_name,
    c.country,
    SUM(f.line_total) AS total_spend,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(AVG(f.line_total)::numeric, 2) AS avg_line_total
FROM fact_sales f
         JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.company_name, c.country
)
SELECT
    customer_id,
    company_name,
    country,
    total_spend,
    total_orders,
    avg_line_total,
    NTILE(4) OVER (ORDER BY total_spend DESC) AS spending_quartile
FROM customer_summary
ORDER BY customer_id;
"""

df = pd.read_sql(query, engine)

print(f'\n Total customers evaluated: {len(df)} ')
print(df.head(5))

print('\n Reshaping data with pandas pivot table... ')
df_pivot = pd.pivot_table(
    df,
    values='total_spend',
    index='customer_id',
    columns='spending_quartile',
    aggfunc='sum',
    fill_value=0
)

print('\n Revenue Distribution Matrix: ')
print(df_pivot.head(5))
