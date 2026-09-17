import pandas as pd
from sqlalchemy import create_engine

pd.set_option('display.max_columns', None)
pd.set_option("display.width", 10000)

print(' Retrieving Data... ')
engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

query = """
WITH order_totals AS (
SELECT
    f.order_id,
    f.customer_id,
    SUM(f.line_total) AS order_amount,
    Max(t.full_date) AS order_date
FROM fact_sales f
    JOIN dim_time t ON f.date_key = t.date_key
GROUP BY order_id, customer_id
)
SELECT
    c.customer_id,
    c.company_name,
    c.country,
    COUNT(ot.order_id) AS total_orders,
    SUM(ot.order_amount) AS lifetime_spend,
    ROUND(AVG(ot.order_amount)::numeric, 2) AS avg_order_value,
    MAX(ot.order_date) - MIN(ot.order_date) AS customer_lifespan_days
FROM order_totals ot
    JOIN dim_customers c ON ot.customer_id = c.customer_id
    GROUP BY c.customer_id, c.company_name, c.country
"""

df = pd.read_sql(query, engine)
print(f'\n Loaded {len(df)} customer rows... ')
print(df.head(5))

# transform() calculates the mean per country and matches every row back to its original shape
df['country_avg_spend'] = df.groupby('country')['lifetime_spend'].transform('mean')

df['spend_vs_country_avg'] = df['lifetime_spend'] - df['country_avg_spend']
df_sorted = df.sort_values(by=['lifetime_spend'], ascending=False)

print('\n Customer behaviour: ')
print(df_sorted[['company_name', 'country', 'lifetime_spend', 'country_avg_spend', 'spend_vs_country_avg']].head(5))
