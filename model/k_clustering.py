import numpy as np
from model.helper_functions import build_playlist_features
from sklearn.cluster import KMeans

playlist_list = np.genfromtxt('./data/train_pids.csv', skip_header=1, dtype=int)
playlist_features = build_playlist_features(playlist_list)

# Set desired number of clusters
n_clusters = int(np.sqrt(len(playlist_features)))

# Make clusters
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(playlist_features.iloc[:, 0:-2])

# See the clusters
print(kmeans.cluster_centers_)
