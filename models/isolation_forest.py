import pandas as pd
import numpy as np
import time as tm
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib as mpl
mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 0.1   # default 0.111, lower = more simplification
mpl.rcParams['agg.path.chunksize'] = 10000      # break path into chunks

begin_opening = tm.perf_counter()
path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\combined_consumption_cleaned.csv"
df = pd.read_csv(path)
end_opening = tm.perf_counter()
print(f"time taken to open file: {end_opening - begin_opening} seconds")
print(df.columns.tolist())



elec_col = "Total energie (Kwh)"        # electricity in kWh
gas_col  = "Total gas energie (Kwh)"    # gas already in kWh (converted)
date_col = "Date"
diff_col = "Consumption Difference (gas-elec (Kwh))"
client_type_col = "client_type_encoded"
nature_col = "nature_encoded"
group_col = "Groupe"  # if we want to group by client reference for time series analysis
balance_col = "balance_ratio"

# Ensure date column is datetime
if df[date_col].dtype in ['int64', 'float64']:
    df[date_col] = pd.to_datetime(df[date_col], unit='D', origin='1899-12-30')
else:
    df[date_col] = pd.to_datetime(df[date_col])

#features selection
feature_columns = [
    elec_col,          
    gas_col,            
    diff_col,           # signed difference
    balance_col,
    nature_col,
    client_type_col,
    group_col, #city/area
    'month_sin',       # cyclic month so dec will be near jan
    'month_cos',
    'is_winter', 
    'is_summer'        
]

# Drop rows with missing values
df_clean = df[feature_columns + [date_col]].dropna()
X = df_clean[feature_columns]

# 3. Scale features (optional but recommended)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Train Isolation Forest
iso_forest = IsolationForest(
    n_estimators=100,
    max_samples='auto',
    contamination=0.0005,        # 0.05% of data considered anomalies
    random_state=42,
    verbose=0
)

df_clean['anomaly'] = iso_forest.fit_predict(X_scaled)   # -1 = anomaly, 1 = normal
df_clean['anomaly_score'] = iso_forest.decision_function(X_scaled)  # lower = more anomalous

# 5. Save results
output_path = "isolation_forest_results.csv"
df_clean.to_csv(output_path, index=False)
print(f"Results saved to {output_path}")
print(f"Number of anomalies detected: {(df_clean['anomaly'] == -1).sum()}")

# 6. Visualizations
# 6.1 Scatter plot: Electricity vs Gas (colored by anomaly)
plt.figure(figsize=(10, 6))
normal = df_clean[df_clean['anomaly'] == 1]
anomaly = df_clean[df_clean['anomaly'] == -1]

plt.scatter(normal[elec_col], normal[gas_col], c='steelblue', label='Normal', alpha=0.6)
plt.scatter(anomaly[elec_col], anomaly[gas_col], c='red', label='Anomaly', edgecolors='black', s=80)
plt.xlabel(f'Electricity (kWh)')
plt.ylabel(f'Gas (kWh)')
plt.title('Isolation Forest: Normal vs Anomalous Consumption')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('anomaly_scatter.png', dpi=150)
plt.show()

# 6.2 Time series: Anomaly score over date
plt.figure(figsize=(12, 5))
plt.plot(df_clean[date_col], df_clean['anomaly_score'], 'o-', markersize=3, alpha=0.7)
plt.axhline(y=np.percentile(df_clean['anomaly_score'], 5), color='red', linestyle='--', 
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
plt.hist(df_clean['anomaly_score'], bins=50, edgecolor='black', alpha=0.7)
plt.axvline(x=np.percentile(df_clean['anomaly_score'], 5), color='red', linestyle='--', 
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
plt.hist(df_clean[df_clean['anomaly']==1][balance_col], bins=30, alpha=0.6, label='Normal', color='blue')
plt.hist(df_clean[df_clean['anomaly']==-1][balance_col], bins=30, alpha=0.6, label='Anomaly', color='red')
plt.xlabel('Balance Ratio (elec - gas)/(elec+gas)')
plt.ylabel('Frequency')
plt.title('Balance Ratio: Normal vs Anomaly')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('balance_ratio_anomalies.png', dpi=150)
plt.show()

print("Visualizations saved as PNG files.")