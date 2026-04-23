import pandas as pd 
import time as tm

THERMIE_TO_KWH = 1.16222
GAS_TO_ELEC = 0.09 * THERMIE_TO_KWH  # 1 Thermie is approximately 0.9 Kwh of electricity to better balance
#specify columns to read from the excel files to save memory
gas_columns = ["Reference", "Numero Facture", "Date", "Total energie (Thermie)", "Type client", "Groupe", "Nature"]
elec_columns = ["Reference", "Numero Facture", "Total energie (Kwh)"]

#read the files 
start_reading = tm.perf_counter()
dir_path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\raw_data"
file1 = r"\Detail_Ventes Elec 2025.xlsx"
file2 = r"\Detail_Ventes Gaz 2025.xlsx"
elec = pd.read_excel(dir_path + file1, usecols=elec_columns)
gas = pd.read_excel(dir_path + file2, usecols=gas_columns)
end_reading = tm.perf_counter()
print(f"Time to read files: {end_reading - start_reading:.2f} seconds")

gas_columns = ["Reference", "Numero Facture", "Date", "Total energie (Thermie)", "Type client", "Groupe", "Nature"]
elec_columns = ["Reference", "Numero Facture", "Date", "Total energie (Kwh)"]
#merging the datasets on reference and facture number
merged = pd.merge(
    elec,
    gas,
    on=["Reference", "Numero Facture"],
    how="inner"   # keeps only matching records
)

# Delete rows where electricity or gas consumption are zero
merged_cleaned = merged[~(merged['Total energie (Kwh)'] == 0) ]
merged_cleaned = merged_cleaned[~(merged_cleaned['Total energie (Thermie)'] == 0)]

#based on consumption visualisation we decided to represent the gas consumption by this.
merged_cleaned ["Total energie (Thermie)"] = merged_cleaned["Total energie (Thermie)"] * GAS_TO_ELEC

#calculate the differnece and a banalce ratio
merged_cleaned['consumption difference'] = merged_cleaned['Total energie (Thermie)'] - merged_cleaned["Total energie (Kwh)"]
merged_cleaned['balance_ratio'] = (merged_cleaned['Total energie (Thermie)'] - merged_cleaned["Total energie (Kwh)"]) / (merged_cleaned["Total energie (Kwh)"] + merged_cleaned['Total energie (Thermie)'] + 1e-9)

#encode client type and nature 
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
merged_cleaned['client_type_encoded'] = merged_cleaned['Type client'].map(client_type_mapping)
merged_cleaned['nature_encoded'] = merged_cleaned['Nature'].map(nature_mapping)

#adding month and seasonal flags
date_col = "Date"
if merged_cleaned[date_col].dtype in ['int64', 'float64']:
    merged_cleaned[date_col] = pd.to_datetime(merged_cleaned[date_col], unit='D', origin='1899-12-30')
else:
    merged_cleaned[date_col] = pd.to_datetime(merged_cleaned[date_col])

merged_cleaned['month'] = merged_cleaned[date_col].dt.month
merged_cleaned['is_winter'] = merged_cleaned['month'].isin([12,1,2,3]).astype(int)
merged_cleaned['is_summer'] = merged_cleaned['month'].isin([6,7,8,9]).astype(int)
#save the cleaned and merged dataset to a new csv file
merged_cleaned.to_csv("cleaned_consumption_{timestamp}.csv", index=False)
print(merged_cleaned["Total energie (Thermie)"].head())
print(f"Electricity rows after cleaning: {len(merged_cleaned)}")
print(f"Gas rows after cleaning: {len(merged_cleaned)}")

