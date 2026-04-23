import pandas as pd 
import time as tm
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib as mpl

mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 0.1   # default 0.111, lower = more simplification
mpl.rcParams['agg.path.chunksize'] = 10000      # break path into chunks


begin_opening = tm.perf_counter()
path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\cleaned_consumption_{timestamp}.csv"
df = pd.read_csv(path)
end_opening = tm.perf_counter()
print(f"time taken to open file: {end_opening - begin_opening} seconds")
print(df.columns.tolist())

elec_col = "Total energie (Kwh)"        # electricity in kWh
gas_col  = "Total energie (Thermie)"    # gas already in kWh
group_col = "Groupe"  # if we want to group by client reference for time series analysis
month_col = "month"
balance_col = "balance_ratio"
diff_col = "consumption difference"     # signed difference
client_type_col = "client_type_encoded"

# Select features for PCA
features = [elec_col, gas_col, diff_col, balance_col, month_col, client_type_col]
X = df[features].dropna()  # Drop rows with missing values
# Standardize features
X_scaled = (X - X.mean()) / X.std()
# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
# Create a DataFrame for PCA results
pca_df = pd.DataFrame(data=X_pca, columns=['Principal Component 1', 'Principal Component 2'])
pca_df[month_col] = df[month_col].sort_values() # Add month for coloring in the plot

feature_columns = [
X_pca[:, 0],          # Principal Component 1
X_pca[:, 1],          # Principal Component 2
month_col,       
]

iso_forest = IsolationForest(
    n_estimators=200,
    max_samples='auto',
    contamination=0.004,        
    random_state=42,
    verbose=0
)

pca_df['anomaly'] = iso_forest.fit_predict(X)   # -1 = anomaly, 1 = normal
pca_df['anomaly_score'] = iso_forest.decision_function(X)  # lower = more anomalous

# 5. Save results
output_path = "isolation_forest_results.csv"
pca_df.to_csv(output_path, index=False)
print(f"Results saved to {output_path}")
print(f"Number of anomalies detected: {(pca_df['anomaly'] == -1).sum()}")

# 6. Visualizations
# 6.1 Scatter plot: Electricity vs Gas (colored by anomaly)
plt.figure(figsize=(10, 6))
normal = pca_df[pca_df['anomaly'] == 1]
anomaly = pca_df[pca_df['anomaly'] == -1]

plt.scatter(normal['Principal Component 1'], normal['Principal Component 2'], c='steelblue', label='Normal', alpha=0.6)
plt.scatter(anomaly['Principal Component 1'], anomaly['Principal Component 2'], c='red', label='Anomaly', edgecolors='black', s=80)
plt.xlabel(f'Principal Component 1')
plt.ylabel(f'Principal Component 2')
plt.title('Isolation Forest: Normal vs Anomalous Consumption')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('anomaly_scatter.png', dpi=150)
plt.show()

# 6.2 Time series: Anomaly score over date
plt.figure(figsize=(12, 5))
plt.plot(pca_df[date_col], pca_df['anomaly_score'], 'o-', markersize=3, alpha=0.7)
plt.axhline(y=np.percentile(pca_df['anomaly_score'], 5), color='red', linestyle='--', 
            label='5th percentile threshold')
plt.xlabel('Date')
plt.ylabel('Anomaly Score (lower = more anomalous)')
plt.title('Isolation Forest Anomaly Scores Over Time')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('anomaly_scores_timeseries.png', dpi=150)
plt.show()

# 6.3 Histogram of anomaly scores
plt.figure(figsize=(8, 5))
plt.hist(pca_df['anomaly_score'], bins=50, edgecolor='black', alpha=0.7)
plt.axvline(x=np.percentile(pca_df['anomaly_score'], 5), color='red', linestyle='--', 
            label='5th percentile (anomaly threshold)')
plt.xlabel('Anomaly Score')
plt.ylabel('Frequency')
plt.title('Distribution of Anomaly Scores')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('anomaly_score_distribution.png', dpi=150)
plt.show()

# 6.4 (Optional) Balance ratio distribution for anomalies
plt.figure(figsize=(8, 5))
plt.hist(pca_df[pca_df['anomaly']==1][balance_col], bins=30, alpha=0.6, label='Normal', color='blue')
plt.hist(pca_df[pca_df['anomaly']==-1][balance_col], bins=30, alpha=0.6, label='Anomaly', color='red')
plt.xlabel('Balance Ratio (elec - gas)/(elec+gas)')
plt.ylabel('Frequency')
plt.title('Balance Ratio: Normal vs Anomaly')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('balance_ratio_anomalies.png', dpi=150)
plt.show()

print("Visualizations saved as PNG files.")
