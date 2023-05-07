import pandas as pd
import numpy as np
import pgeocode
nomi = pgeocode.Nominatim('ca')

# New columns to store latitude and longitude
df = pd.read_csv('./data/radon-concentration.csv', encoding='latin-1')
df["latitude"] = np.nan
df["longitude"] = np.nan

for row in df.index:
    location = nomi.query_postal_code(df['ForwardSortationAreaCodes'][row])
    df['latitude'][row] = location.latitude
    df['longitude'][row] = location.longitude

# Remove Naan values for plotting purposes
df = df.dropna()

df.to_csv('radon-concentration.csv', index = False) 

# Drop Radon/Thoron columns for linear regression