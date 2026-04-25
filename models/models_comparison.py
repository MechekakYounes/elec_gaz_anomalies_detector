import pandas as pd 
import numpy as np
from functools import reduce
from collections import Counter

hdbsca_results_path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\hdbscan_clustering_results.csv"
iso_forest_results_path = r"C:\Users\Administrator\Desktop\elec_gaz_anomalies_detector\isolation_forest_results.csv"
output_path = "models_comparison_results.csv"

hdbscan_df = pd.read_csv(hdbsca_results_path)
iso_forest_df = pd.read_csv(iso_forest_results_path)

hdbscan_anomalies = hdbscan_df[hdbscan_df['cluster'] == -1]
iso_forest_anomalies = iso_forest_df[iso_forest_df['anomaly'] == -1]

print(f"HDBSCAN found {len(hdbscan_anomalies)} anomalies.")
print(f"Isolation Forest found {len(iso_forest_anomalies)} anomalies.")
common_refs_count = {}
for ref in hdbscan_anomalies['Reference']:
    for ref2 in iso_forest_anomalies['Reference']:
        if ref == ref2:
           if ref not in common_refs_count:
              common_refs_count[ref] = 1
           common_refs_count[ref] += 1

result_df = pd.DataFrame(list(common_refs_count.items()), columns=['Reference', 'occurrence_count'])
result_df.to_csv(output_path, index=False)
print(f"Output saved to {output_path}")

print(f"Number of common anomalies: {len(common_refs_count)}")
