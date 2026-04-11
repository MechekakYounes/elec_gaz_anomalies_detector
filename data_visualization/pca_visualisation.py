import pandas as pd 
import time as tm
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

begin_opening = tm.perf_counter()
path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\combined_consumption_cleaned.csv"
df = pd.read_csv(path)
end_opening = tm.perf_counter()
print(f"time taken to open file: {end_opening - begin_opening} seconds")
print(df.columns.tolist())

elec_col = "Total energie (Kwh)"        # electricity in kWh
gas_col  = "Total gas energie (Kwh)"    # gas already in kWh
group_col = "Groupe"  # if we want to group by client reference for time series analysis
month_sin_col = "month_sin"
month_cos_col = "month_cos"
month_col = "month"
balance_col = "balance_ratio"
diff_col = "Consumption Difference (gas-elec (Kwh))"
client_type_col = "client_type_encoded"

# Select features for PCA
features = [elec_col, gas_col, diff_col, balance_col, month_sin_col, month_cos_col, client_type_col]
X = df[features].dropna()  # Drop rows with missing values
# Standardize features
X_scaled = (X - X.mean()) / X.std()
# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
# Create a DataFrame for PCA results
pca_df = pd.DataFrame(data=X_pca, columns=['Principal Component 1', 'Principal Component 2'])
pca_df[month_col] = df[month_col].sort_values() # Add month for coloring in the plot

# Plot PCA results
plt.figure(figsize=(10, 7))
for month in pca_df[month_col].unique():
    indices = pca_df[month_col] == month
    plt.scatter(pca_df.loc[indices, 'Principal Component 1'], 
                pca_df.loc[indices, 'Principal Component 2'], 
                label=month, alpha=0.5)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of Energy Consumption Data')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
plt.savefig("pca_all_features_by_month.png")