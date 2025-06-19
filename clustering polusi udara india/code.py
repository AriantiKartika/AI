import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

df = pd.read_csv(r'D:\sem 4\AI\UAS\bagian2\clustering polusi udara india\city_day.csv')
fitur = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'O3']

data_kota = df.groupby('City')[fitur].mean()
data_kota_clean = data_kota.dropna()

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_kota_clean)

kmeans = KMeans(n_clusters=3, random_state=42)
data_kota_clean['Cluster'] = kmeans.fit_predict(data_scaled)

pca = PCA(n_components=2)
pca_result = pca.fit_transform(data_scaled)
data_kota_clean['PCA1'] = pca_result[:, 0]
data_kota_clean['PCA2'] = pca_result[:, 1]

colors = ['green', 'orange', 'black']
labels = ['polusi rendah', 'polusi sedang', 'polusi tinggi']

plt.figure(figsize=(10, 6))
for cluster_id in range(3):
    subset = data_kota_clean[data_kota_clean['Cluster'] == cluster_id]
    plt.scatter(subset['PCA1'], subset['PCA2'], 
                c=colors[cluster_id], label=labels[cluster_id], s=100)

    for kota, row in subset.iterrows():
        plt.text(row['PCA1'] + 0.1, row['PCA2'], kota, fontsize=8)

plt.legend(title='Keterangan Cluster')
plt.title('Clustering Kota Berdasarkan Polusi Udara')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.grid(True)
plt.show()


for kota, row in data_kota_clean.iterrows():
    plt.text(row['PCA1'] + 0.1, row['PCA2'], kota, fontsize=8)

plt.title('Clustering Kota Berdasarkan Polusi Udara')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.grid(True)
plt.show()

