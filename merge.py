import pandas as pd

google = pd.read_csv('voc_fashion_raw.csv')
mouthshut = pd.read_csv('mouthshut_raw.csv')
cleaned_sample = pd.read_csv('abb_cleaned_google_mouthshut_only.csv')
manual_extra = pd.read_csv('abb_manual_myntra_twitter_instagram.csv')

combined = pd.concat([google, mouthshut, cleaned_sample, manual_extra], ignore_index=True)
combined = combined.drop_duplicates(subset=['row_hash'])
combined.to_csv('voc_fashion_final.csv', index=False)
print(f'Final combined: {len(combined)} rows')