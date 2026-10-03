import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

query = """
WITH customer_summary AS (
SELECT
    c.customer_id,
    c.country,
    SUM(f.line_total) AS total_spend
FROM fact_sales f 
         JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.customer_id, c.country
)
SELECT
    customer_id,
    country,
    total_spend,
    NTILE(4) OVER (ORDER BY total_spend DESC) AS spending_quartile
FROM customer_summary;
"""

df = pd.read_sql(query, engine)
df_grouped = df.groupby(['customer_id', 'country', 'spending_quartile'])['total_spend'].sum().reset_index()

# Pivot data: country as rows, quartiles (1 to 4) as columns
df_pivot = pd.pivot_table(
    df_grouped,
    values="total_spend",
    index='country',
    columns='spending_quartile',
    aggfunc='sum',
    fill_value=0
)

# Use pandas built in plot wrapper
fig, ax = plt.subplots(figsize=(20, 10))

# Plot as a stacked bar chart to show revenue chart to show revenue contribution per country
df_pivot.plot(
    kind='bar',
    stacked=True,
    ax=ax,
    color='black',
    edgecolor='black',
    linewidth=0.5
)

# Styling the chart for execute presentation
ax.set_title('Revenue contribution by country & Spending quartile', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Country', fontsize=11, labelpad=10)
ax.set_ylabel('Total revenue($)', fontsize=11, labelpad=10)
ax.legend(title='Spending quartile\n(1 = Top, 4 = Bottom)', bbox_to_anchor=(1.02, 1), loc='upper left')

# Rotate x-axis country labels for readability
plt.xticks(rotation=45, ha='right')

# Format y-axis with comas for currency look
ax.yaxis.set_major_formatter('${x:,.0f}')

# Display the chart
plt.show()
