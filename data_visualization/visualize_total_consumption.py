import pandas as pd 
import time as tm
import numpy as np 
import matplotlib.pyplot as plt

begin_opening = tm.perf_counter()
path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\combined_consumption_cleaned.csv"
df = pd.read_csv(path)
end_opening = tm.perf_counter()

print(f"time taken to open file: {end_opening - begin_opening} seconds")
print(df.columns.tolist())


kwh_col = "Total energie (Kwh)"      
therm_col = "Total gas energie (Kwh)" 


# Calculate total energy
total_kwh = df[kwh_col].sum()
total_therm = df[therm_col].sum()
ratio = total_them / total_therm 

print(f"Total Electricity Consumption (kWh): {total_kwh:,.2f}")
print(f"Total Gas Consumption (Thermie): {total_therm:,.2f}")
print(f"Electricity to Gas Ratio: {ratio:.2f}")
# Create a simple bar chart
plt.figure(figsize=(6, 5))
bars = plt.bar(["Electricity (kWh)", "Gas (Thermie)"], [total_kwh, total_therm], 
               color=['blue', 'orange'], edgecolor='black')

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.02 * max(total_kwh, total_therm),
             f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

plt.title("Total Energy Consumption (2024)", fontsize=14)
plt.ylabel("Energy Amount")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
plt.savefig("sum_of_energy_consumption_2024.png")

