import pandas as pd
import time as tm
import numpy as np

path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\combined_consumption_encoded.csv"

begin_opening = tm.perf_counter()
df = pd.read_csv(path)
end_opening = tm.perf_counter()
print(f"time taken to open file: {end_opening - begin_opening} seconds")
print(df.columns.tolist())

date_col = "Date"
# --- Convert date to datetime ---
if df[date_col].dtype in ['int64', 'float64']:
    df[date_col] = pd.to_datetime(df[date_col], unit='D', origin='1899-12-30')
else:
    df[date_col] = pd.to_datetime(df[date_col])

df['month'] = df[date_col].dt.month

# Cyclical encoding of month (so Dec and Jan are neighbours)
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

# Seasonal flags according to the local climate
df['is_winter'] = df['month'].isin([12,1,2]).astype(int)   
df['is_summer'] = df['month'].isin([6,7,8]).astype(int)    

df.to_csv("combined_consumption_encoded.csv", index=False)
print("Date encoding completed and saved to combined_consumption_encoded.csv")