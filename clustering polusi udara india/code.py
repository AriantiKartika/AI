# Import library
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# 1. Load data
df = pd.read_csv(r'D:\sem 4\AI\UAS\bagian2\clustering polusi udara india\city_day.csv')

# 2. Pilih fitur polusi yang relevan
fitur = ['PM2.5', 'PM10', 'NO2', 'CO', 'SO2', 'O3']

# 3. Kelompokkan berdasarkan kota dan hitung rata-rata tiap parameter
data_kota = df.groupby('City')[fitur].mean()

# 4. Hapus kota yang memiliki nilai NaN
data_kota_clean = data_kota.dropna()

# 5. Normalisasi data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_kota_clean)

# 6. Clustering dengan K-Means (jumlah cluster = 3)
kmeans = KMeans(n_clusters=3, random_state=42)
data_kota_clean['Cluster'] = kmeans.fit_predict(data_scaled)

# 7. Reduksi dimensi dengan PCA untuk visualisasi 2D
pca = PCA(n_components=2)
pca_result = pca.fit_transform(data_scaled)
data_kota_clean['PCA1'] = pca_result[:, 0]
data_kota_clean['PCA2'] = pca_result[:, 1]

# 8. Visualisasi hasil clustering
colors = ['red', 'orange', 'black']
labels = ['Cluster 0', 'Cluster 1', 'Cluster 2']

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


# Tambahkan label nama kota
for kota, row in data_kota_clean.iterrows():
    plt.text(row['PCA1'] + 0.1, row['PCA2'], kota, fontsize=8)

plt.title('Clustering Kota Berdasarkan Polusi Udara')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.grid(True)
plt.show()
