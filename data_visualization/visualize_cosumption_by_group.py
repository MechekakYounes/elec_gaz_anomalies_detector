""" 
we mean by groups the different areas of the city
"""
import matplotlib.pyplot as plt
import pandas as pd

# Load the merged CSV
df = pd.read_csv("combined_consumption_24.csv")

# Assuming date column is named 'Date' or 'Votre date'
group_col = 'Groupe'  # change to actual name
kwh_col = "Total energie (Kwh)"
therm_col = "Total energie (Thermie)" 


# Convert from Excel serial if needed

# Then group by month
df['Group'] = df[group_col]
monthly = df.groupby('Group')[[kwh_col, therm_col]].sum()

monthly.plot(kind='bar', figsize=(12,5), color=['blue', 'orange'])
plt.title("Monthly Energy Consumption")
plt.ylabel("Energy")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.savefig("monthly_energy_consumption_2024.png")
