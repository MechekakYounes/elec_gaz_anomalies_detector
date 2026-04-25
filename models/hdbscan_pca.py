import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import hdbscan
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib as mpl

mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 0.1
mpl.rcParams['agg.path.chunksize'] = 10000

output_path = "hdbscan_clustering_results.csv"
path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\cleaned_consumption_{timestamp}.csv"
df = pd.read_csv(path)
print("Columns:", df.columns.tolist())

elec_col = "Total energie (Kwh)"
gas_col  = "Total energie (Thermie)"
diff_col = "consumption difference"
balance_col = "balance_ratio"
client_type_col = "client_type_encoded"
group_col = "Groupe"
month_col = "month"


# Feature list – you can add or remove as needed
feature_columns = [
    elec_col, gas_col, diff_col, balance_col,
    month_col, client_type_col, group_col
]

return_columns = ['Reference', 'Numero Facture'] + feature_columns

# Drop missing values
df_clean = df[return_columns].dropna().copy()
X = df_clean[feature_columns]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
print(f"Explained variance by PC1: {pca.explained_variance_ratio_[0]:.3f}")
print(f"Explained variance by PC2: {pca.explained_variance_ratio_[1]:.3f}")
print(f"Total: {pca.explained_variance_ratio_.sum():.3f}")

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=100,        # minimum number of points to form a cluster
    min_samples=3,              # higher = more points marked as noise
    metric='euclidean',
    cluster_selection_method='eom'   # 'eom' (excess of mass) or 'leaf'
)

df_clean['cluster'] = clusterer.fit_predict(X_pca)
# cluster = -1 means noise (anomaly)
# cluster >= 0 means a specific cluster

df_clean['PC1'] = X_pca[:, 0]
df_clean['PC2'] = X_pca[:, 1]
df_clean.to_csv(output_path, index=False)
print(f"Results saved to {output_path}")
print(f"Number of clusters found: {len(set(df_clean['cluster'])) - (1 if -1 in df_clean['cluster'] else 0)}")
print(f"Number of noise points (anomalies): {(df_clean['cluster'] == -1).sum()}")


plt.figure(figsize=(12, 6))
# Get unique clusters (excluding -1 for separate colour)
clusters = sorted(set(df_clean['cluster']))
for cluster in clusters:
    if cluster == -1:
        continue
    subset = df_clean[df_clean['cluster'] == cluster]
    plt.scatter(subset['PC1'], subset['PC2'], label=f'Cluster {cluster}', alpha=0.6, s=20)

# Plot noise (anomalies) in red
noise = df_clean[df_clean['cluster'] == -1]
plt.scatter(noise['PC1'], noise['PC2'], c='red', label='Noise (Anomaly)', edgecolors='black', s=80, marker='x')

plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
plt.title('HDBSCAN Clustering on PCA Components')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('hdbscan_pca_clusters.png', dpi=150)
plt.show()


# Additional analysis: cluster characteristics
print("\nCluster summary (size, average electricity, gas, balance ratio):")
cluster_summary = df_clean.groupby('cluster').agg({
    elec_col: 'mean',
    gas_col: 'mean',
    balance_col: 'mean',
    client_type_col: 'mean',
    group_col: lambda x: x.mode().iloc[0] if len(x.mode())>0 else np.nan,
    'PC1': 'mean',
    'PC2': 'mean'
}).round(3)
print(cluster_summary)

# Save summary
cluster_summary.to_csv("hdbscan_cluster_summary.csv")
print("\nCluster summary saved to hdbscan_cluster_summary.csv")