import pandas as pd
import matplotlib.pyplot as plt

# Load the merged CSV
path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\combined_consumption_cleaned.csv"
df = pd.read_csv(path)

# --- Adjust these column names to match your actual file ---
kwh_col = "Total energie (Kwh)"
therm_col = "Total gas energie (Kwh)"
# -----------------------------------------------------------

# Drop any rows where either consumption value is missing
df_clean = df[[kwh_col, therm_col]].dropna()

# Create scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df_clean[kwh_col], df_clean[therm_col], 
            alpha=0.6, c='steelblue', edgecolors='black', s=50)

# Labels and title
plt.xlabel(f"Electricity Consumption ({kwh_col})", fontsize=12)
plt.ylabel(f"Gas Consumption ({therm_col})", fontsize=12)
plt.title("Individual Record: Electricity vs Gas Consumption", fontsize=14)

# Add a diagonal reference line (optional) – shows where consumption is equal in scale
max_val = max(df_clean[kwh_col].max(), df_clean[therm_col].max())
plt.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='Equal consumption (scaled)')

plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()