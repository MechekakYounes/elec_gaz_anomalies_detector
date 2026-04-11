import pandas as pd 
import matplotlib.pyplot as plt

path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\combined_consumption_with_difference.csv"
df = pd.read_csv(path)
elec_col = "Total energie (Kwh)"
gas_col = "Total gas energie (Kwh)"
diff_col = "Consumption Difference (gas-elec (Kwh))"
balance_col = "balance_ratio"
date_col = "Date" 

if df[date_col].dtype in ['int64', 'float64']:
    df[date_col] = pd.to_datetime(df[date_col], unit='D', origin='1899-12-30')
else:
    df[date_col] = pd.to_datetime(df[date_col])  # convert to datetime anyway

df = df.sort_values(date_col)

plt.figure(figsize=(12, 6))
plt.plot(df[date_col], df[diff_col], marker='o', linestyle='-', 
         markersize=4, linewidth=1, color='steelblue', alpha=0.7)

# Add a horizontal line at zero (balanced consumption)
plt.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Balanced (Elec = Gas)')

plt.xlabel('Date', fontsize=12)
plt.ylabel('Energy Difference (kWh) – Positive = more gas', fontsize=12)
plt.title('Gas - Electricity Consumption Difference Over Time', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
plt.savefig("consumption_difference_over_time.jpg")



