import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

query = """
SELECT
    p.category_name,
    t.month,
    SUM(f.line_total) AS total
FROM fact_sales f
         JOIN dim_time t ON f.date_key = t.date_key
         JOIN dim_products p ON f.product_id = p.product_id
    GROUP BY p.category_name, t.month
    ORDER BY t.month
"""

df = pd.read_sql(query, engine)

df_pivot = pd.pivot_table(
    df,
    values='total',
    index='month',
    columns='category_name',
    fill_value=0
)

fig, ax = plt.subplots(figsize=(15, 10))

df_pivot.plot(
    kind='line',
    ax=ax,
    marker='o',
    linewidth=2,
)

ax.set_title('Monthly Revenue by Product Category', fontsize=20, pad=10)
ax.set_xlabel('Month', fontsize=20, labelpad=10)
ax.set_ylabel('Total Revenue ($)', fontsize=20, labelpad=10)

ax.yaxis.set_major_formatter('${x:,.0f}')

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
