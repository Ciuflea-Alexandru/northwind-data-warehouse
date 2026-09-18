import pandas as pd
from sqlalchemy import create_engine

print(' Retrieving Data... ')
engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')

query = """
SELECT
    order_id,
    customer_id,
    product_id,
    quantity,
    unit_price,
    line_total
FROM fact_sales
"""

df = pd.read_sql_query(query, engine)
print(df.head(5))

print('\n Running data quality checks... ')
validation_passed = True
error_log = []

# CHECK 1: Completeness
null_counts = df[['order_id', 'customer_id', 'line_total']].isnull().sum().sum()
if null_counts > 0:
    validation_passed = False
    error_log.append(f'\n Fail: Found {null_counts} null values ')
else:
    print('\n Pass: Completeness check ')

# CHECK 2: Validity / Range
invalid_prices = df[df['unit_price'] < 0].shape[0]
invalid_quantities = df[df['quantity'] < 0].shape[0]

if invalid_prices > 0 or invalid_quantities > 0:
    validation_passed = False
    error_log.append(f'\n Fail: Found {invalid_prices} invalid prices and {invalid_quantities} invalid quantities ')
else:
    print('\n Pass: Range check ')

# CHECK 3: Logical Consistency
# line_total should roughly equal quantity * unit_price
df['expected_total'] = df['quantity'] * df['unit_price']

# Check where discrepancy is greater than 1 cent due to discounts or calculations bugs
mismatches = df[abs(df['line_total'] - df['expected_total']) > 0.05].shape[0]

if mismatches > 0:
    print(f'\n WARNING: {mismatches} rows have line_totals that differ from unit_price * quantity ')
else:
    print('\n Pass: calculation consistency check ')

if validation_passed:
    print('\n ALL CRITICAL QUALITY CHECKS PASSED! ')
else:
    print('\n Data quality violations detected! ')
    for error in error_log:
        print(error)
    raise ValueError('\n Data quality check failed. ')
