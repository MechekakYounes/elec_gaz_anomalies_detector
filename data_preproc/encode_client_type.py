import pandas as pd
import time as tm

begin_opening = tm.perf_counter()
path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\csv_archive\combined_consumption_with_difference.csv"
df = pd.read_csv(path)
end_opening = tm.perf_counter()
print(f"time taken to open file: {end_opening - begin_opening} seconds")
print(df.columns.tolist())

client_type_col = "Type client"
nature_col = "Nature"
# Define mapping for client types
client_type_mapping = {
    "FSM": 0,
    "AO": 1
}

nature_mapping = {
    "Annul": 0,
    "Ems Cycl": 1,
    "Ems HC": 2
}

# Apply mapping to create a new encoded column
df['client_type_encoded'] = df[client_type_col].map(client_type_mapping)
df['nature_encoded'] = df[nature_col].map(nature_mapping)

# Save the updated DataFrame with the new encoded column
df.to_csv("combined_consumption_encoded.csv", index=False)
print("Client type encoding completed and saved to combined_consumption_with_client_type.csv")