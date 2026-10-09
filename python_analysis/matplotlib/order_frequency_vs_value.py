import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

query = '''
SELECT 
    c.customer_id,
    c.company_name,
    COUNT(DISTINCT f.order_id) AS order_frequency,
    AVG(line_total) AS avg_order_value
FROM fact_sales f 
    JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.company_name
'''

df = pd.read_sql_query(query, engine)

fig, ax = plt.subplots(figsize=(10, 5))

ax.scatter(
    df['order_frequency'],
    df['avg_order_value'],
    color='purple',
    alpha=0.7,
    edgecolors='black',
    s=80
)

ax.set_title('Customer Order Frequency vs Average Order Value', fontsize=15, fontweight='bold')
ax.set_xlabel('Order Frequency', fontsize=15)
ax.set_ylabel('Average Order Value ($)', fontsize=15)
ax.yaxis.set_major_formatter('${x:,.0f}')

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
