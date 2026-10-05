import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

query = '''
WITH product_revenue AS (
SELECT 
    p.product_name,
    SUM(f.line_total) AS total_revenue
FROM fact_sales f 
    JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.product_name
),
    ranked_products AS (
    SELECT
        product_name,
        total_revenue,
        SUM(total_revenue) OVER(ORDER BY total_revenue DESC) AS running_total,
        SUM(total_revenue) OVER() AS grand_total
    FROM product_revenue
    )
    SELECT 
        product_name,
        total_revenue,
        (running_total * 100.0 / grand_total) AS cumulative_percentage
    FROM ranked_products
    ORDER BY total_revenue DESC
'''

df = pd.read_sql_query(query, engine)

# Take the top 20 products
df_top = df.head(20).copy()

# Create figure with a single set of axes
fig, ax1 = plt.subplots(figsize=(20, 6))

# Primary Axis: Bar chart for individual product revenues
ax1.bar(
    df_top['product_name'],
    df_top['total_revenue'],
    color='steelblue',
    edgecolor='black',
    linewidth=0.5,
)

ax1.set_xlabel('Product Name', fontsize=20, labelpad=10)
ax1.set_ylabel('Revenue ($)', fontsize=20, labelpad=10, color='steelblue')
ax1.tick_params(axis='x', rotation=45)
ax1.yaxis.set_major_formatter('${x:,.0f}')

# Secondary Axis: Line chart for cumulative percentage using twinx()
ax2 = ax1.twinx()
ax2.plot(
    df_top['product_name'],
    df_top['cumulative_percentage'],
    color='darkorange',
    marker='o',
    linewidth=2,
)

ax2.set_ylabel('Cumulative Percentage (%)', fontsize=20, color='darkorange', labelpad=10)
ax2.set_ylim(0, 105)

# Add 80% reference threshold line (the core of the Pareto principle)
ax2.axhline(80, color='gray', linestyle='--', linewidth=1, label='80% Threshold')

plt.title('Product Pareto Analysis (Top 20 Revenue Drivers)', fontsize=30, fontweight='bold')
plt.tight_layout()
plt.show()
