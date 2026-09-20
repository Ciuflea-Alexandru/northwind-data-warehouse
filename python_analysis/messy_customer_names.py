import pandas as pd
from rapidfuzz import fuzz, process

master_customers = [
    'Alfreds Futterkiste',
    'Ana Trujillo Emparedados',
    'Antonio Moreno Taquria',
    'Aground the Horn',
    'Berglunds snabbkop'
]

incoming_customer = {
    'raw_name': [
    'Afgreds Futterkist',       # Missing 'e'
    'Ana Trujillo Empareddos',  # Typo in 'Emparedados'
    'Antonio Moreno Taqueria',  # Missing accent mark
    'Around the Hrn',           # Typo
    'Totally Unknown Company'   # Brand new/unmatched anomaly
],
    'order_amount': [150.0, 320.0, 450.0, 120.0, 999.0]
}

df = pd.DataFrame(incoming_customer)
print(' Raw Messy Data:')
print(df)

print('\n Applying rapidfuzz matching... ')


def best_match(query_name, choices, threshold=80):
    result = process.extractOne(query_name, choices, scorer=fuzz.ratio)

    if result and result[1] >= threshold:
        return result[0]
    else:
        return 'UNKNOWN / FLAG FOR REVIEW'


df['cleaned_name'] = df['raw_name'].apply(lambda x: best_match(x, master_customers, threshold=75))

print('\n Cleaned Dataframe with fuzzy matching:')
print(df[['raw_name', 'cleaned_name', 'order_amount']])
