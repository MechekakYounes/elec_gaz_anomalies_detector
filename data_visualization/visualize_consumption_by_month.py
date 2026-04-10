import pandas as pd
import matplotlib.pyplot as plt

# Load the merged CSV
df = pd.read_csv("combined_consumption_24.csv")

# Assuming date column is named 'Date' or 'Votre date'
date_col = 'Date'  # change to actual name
kwh_col = "Total energie (Kwh)"
therm_col = "Total energie (Thermie)" 


# Convert from Excel serial if needed
if df[date_col].dtype in ['int64', 'float64']:
    df[date_col] = pd.to_datetime(df[date_col], unit='D', origin='1899-12-30')

# Then group by month
df['Month'] = df[date_col].dt.to_period('M')
monthly = df.groupby('Month')[[kwh_col, therm_col]].sum()

monthly.plot(kind='bar', figsize=(12,5), color=['blue', 'orange'])
plt.title("Monthly Energy Consumption")
plt.ylabel("Energy")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.savefig("monthly_energy_consumption_2024.png")