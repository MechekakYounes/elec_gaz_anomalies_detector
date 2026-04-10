import pandas as pd
import numpy as np
import time as tm

dir_path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\raw_data"
begin_opening = tm.perf_counter()
elec = pd.read_excel(dir_path + r"\Detail_Ventes Elec 2024.xlsx")
gas = pd.read_excel(dir_path + r"\Detail_Ventes Gaz 2024.xlsx")
end_opening = tm.perf_counter()

print(f"time taken to open files: {end_opening - begin_opening} seconds")
print("Electricity columns:", elec.columns.tolist())
print("Gas columns:", gas.columns.tolist())
# Merge datasets using reference and date
merged = pd.merge(
    elec,
    gas,
    on=["Reference", "Numero Facture"],
    how="inner"   # keeps only matching records
)

# Save result
merged.to_csv("combined_consumption_24.csv", index=False)

print("Datasets merged successfully!")
print(merged.head())

