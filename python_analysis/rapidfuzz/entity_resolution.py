import pandas as pd
from sqlalchemy import create_engine
from rapidfuzz.distance import Levenshtein

print('Retrieving Data...')
engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')
df = pd.read_sql("SELECT customer_id, company_name, country FROM dim_customers", engine)

target_name = "Around the Horses"

print(f"\n Calculating raw levenshtein edit distance against target: '{target_name}'")

# Calculate exact number of single-character changes needed using rapidfuzz.distance.Levenshtein
df['levenshtein_distance'] = df['company_name'].apply(
    lambda name: Levenshtein.distance(name, target_name)
)

# Filter for records within a strict edit-distance threshold (e.g., 3 or fewer typos)
df_resolved = df[df['levenshtein_distance'] <= 3].sort_values('levenshtein_distance')

print("\n Entity resolution results:")
print(df_resolved[['company_name', 'country', 'levenshtein_distance']].to_string(index=False))