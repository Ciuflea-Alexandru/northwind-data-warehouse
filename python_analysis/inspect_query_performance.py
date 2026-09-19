import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

query = """
EXPLAIN ANALYZE
SELECT 
    c.country,
    SUM(f.line_total) AS total_revenue
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.country;
"""

with engine.connect() as connection:
    # EXPLAIN ANALYZE returns multiple rows of text performance plans
    execution_plan = connection.execute(text(query)).fetchall()

    print('📊 Postgresql Query Execution Plan: ')
    for row in execution_plan:
        print(row[0])
