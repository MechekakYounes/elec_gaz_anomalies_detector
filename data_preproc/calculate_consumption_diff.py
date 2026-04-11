"""
calculate the difference in after converting to the same unit (Kwh)
and also calculate the balance ratio (gas-elec)/(gas+elec) to see how balanced the consumption is 
"""

import pandas as pd 
import time as tm
import numpy as np 


THERMIE_TO_KWH = 1.16222

path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\data_visualization\combined_consumption_24.csv" 
begin_opening = tm.perf_counter()
df = pd.read_csv(path)
end_opening = tm.perf_counter()
print(f"time taken to open file: {end_opening - begin_opening} seconds")
print(df.columns.tolist())

kwh_col = "Total energie (Kwh)"
therm_col = "Total energie (Thermie)"

df['Total gas energie (Kwh)'] = df[therm_col] * THERMIE_TO_KWH  # Convert Thermie to Kwh
df['Consumption Difference (gas-elec (Kwh))'] = df['Total gas energie (Kwh)'] - df[kwh_col]

df['balance_ratio'] = (df['Total gas energie (Kwh)'] - df[kwh_col]) / (df[kwh_col] + df['Total gas energie (Kwh)'] + 1e-9)

df.to_csv("combined_consumption_with_difference.csv", index=False)
print("all done ...")


