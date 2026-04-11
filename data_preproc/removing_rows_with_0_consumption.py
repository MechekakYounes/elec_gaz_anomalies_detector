import pandas as pd

# Load your CSV file
path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\combined_consumption_encoded.csv"
df = pd.read_csv(path)

# Count rows before deletion
initial_rows = len(df)
print(f"Initial rows: {initial_rows}")

# Delete rows where both electricity and gas consumption are zero
df_cleaned = df[~(df['Total energie (Kwh)'] == 0) ]
df_cleaned = df_cleaned[~(df_cleaned['Total gas energie (Kwh)'] == 0)]

# Count rows after deletion
final_rows = len(df_cleaned)
print(f"Rows after deletion: {final_rows}")
print(f"Removed {initial_rows - final_rows} rows with zero consumption for both energies.")

# Save the cleaned file (overwrite or create new)
output_file = "combined_consumption_cleaned.csv"
df_cleaned.to_csv(output_file, index=False)
print(f"Cleaned data saved to {output_file}")