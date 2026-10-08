import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')


query = '''
SELECT
    c.customer_id,
    c.company_name,
    SUM(f.line_total) AS total_spend
FROM fact_sales f 
         JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.company_name
ORDER BY total_spend DESC
'''

df = pd.read_sql_query(query, engine)

# Select the top and bottom 10 customers based on how much they spend
df_top_10 = df.head(10).sort_values('total_spend', ascending=True)
df_worst_10 = df.tail(10).sort_values('total_spend', ascending=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Top 10 best customers
ax1.barh(
    df_top_10['company_name'],
    df_top_10['total_spend'],
    color='green',
    edgecolor='black',
    linewidth=0.5,
)
ax1.set_title('Top 10 Best Customers', fontsize=24, fontweight='bold')
ax1.set_xlabel('Total Revenue ($)', fontsize=12, labelpad=8)
ax1.xaxis.set_major_formatter('${x:,.0f}')

# Top 10 worst customers
ax2.barh(
    df_worst_10['company_name'],
    df_worst_10['total_spend'],
    color='red',
    edgecolor='black',
    linewidth=0.5,
)
ax2.set_title('Top 10 Worst Customers', fontsize=24, fontweight='bold')
ax2.set_xlabel('Total Revenue ($)', fontsize=12, labelpad=8)
ax2.xaxis.set_major_formatter('${x:,.0f}')

plt.tight_layout()
plt.show()
