import pandas as pd
import matplotlib.pyplot as plt

# Load the merged CSV
path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\combined_consumption_cleaned.csv"
df = pd.read_csv(path)

# Assuming date column is named 'Date' or 'Votre date'
month_col = 'month'  # change to actual name
kwh_col = "Total energie (Kwh)"
therm_col = "Total gas energie (Kwh)" 


# Convert from Excel serial if needed

# Then group by month
monthly = df.groupby(month_col)[[kwh_col, therm_col]].sum()

monthly.plot(kind='bar', figsize=(12,5), color=['blue', 'orange'])
plt.title("Monthly Energy Consumption")
plt.ylabel("Energy")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.savefig("monthly_energy_consumption_2024.png")