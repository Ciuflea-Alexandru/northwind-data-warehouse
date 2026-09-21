import pandas as pd
from sqlalchemy import create_engine
from rapidfuzz import fuzz, process

print('Retrieving Data...')
engine = create_engine('postgresql://postgres:12345@localhost:5432/northwind_olap')
df = pd.read_sql("SELECT customer_id, company_name, country FROM dim_customers", engine)

messy_injection = pd.DataFrame([
    {'customer_id': 'TEST1', 'company_name': 'Alfred Futterkist', 'country': 'Germany'},  # Missing trailing 'e'
    {'customer_id': 'TEST2', 'company_name': 'Around the Hrn', 'country': 'UK'},  # Typo in 'Horn'
    {'customer_id': 'TEST3', 'company_name': 'Ana Trujillo Empareddos', 'country': 'Mexico'},  # Typo in 'Emparedados'
])

# Combine real database row with the messy variants
df_test = pd.concat([df, messy_injection], ignore_index=True)
print(f' Tota; records loaded for entity resolution: {len(df_test)}')

print('\n Running Entity Resolution...')

names = df_test['company_name'].tolist()
resolved_clusters = []
seen = set()

for _, row in df_test.iterrows():
    name = row['company_name']

    if name in seen:
        continue

    # Use process.extract to find all similar string variants in the dataset
    # scorer=fuzz.token_sort_ratio handles word-order differences
    matches = process.extract(name, names, scorer=fuzz.token_sort_ratio, limit=10)

    # Filter for high-confidence matches (score >= 85
    close_matches = [m for m in matches if m[1] >= 85 and m[0] != name]

    if close_matches:
        variant_names = [m[0] for m in close_matches]
        resolved_clusters.append({
            'master_entity': name,
            'detected_variants': variant_names,
            'match_scores': [m[1] for m in close_matches]
        })

        for v in variant_names:
            seen.add(v)

    # Add variants to 'seen' so we don't recreate duplicate for them
    seen.add(name)

df_clusters = pd.DataFrame(resolved_clusters)

if not df_clusters.empty:
    print('\n Successfully detected entity clusters:')
    print(df_clusters.to_string(index=False))
else:
    print('\n No fuzzy duplicates detected with the current threshold')
