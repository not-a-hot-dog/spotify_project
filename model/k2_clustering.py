import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import pickle

# Get the train features dataframe
playlist_features = pd.read_csv('./data/playlist_features_with_artists_train.csv', index_col=0, header=0)
playlist_list = playlist_features.index.values

# Set desired number of clusters
n_clusters = int(np.sqrt(len(playlist_features)))

print('Making clusters')
# Make clusters
kmeans = KMeans(n_clusters=n_clusters, verbose=0, algorithm='auto')
kmeans.fit(playlist_features)


print('Saving clusters')
# Saving the clusters
pickle.dump(kmeans, open('./model/kmeans_cluster_train.pkl', 'wb'))
cluster_centers = kmeans.cluster_centers_
np.savetxt('./model/kmeans_cluster_centers_train.csv', cluster_centers, delimiter=',')

# Saving the cluster label for each playlist in train (e.g., for track frequency table by cluster)
cluster_labels = kmeans.labels_
playlist_cluster_labels = np.column_stack((playlist_list, cluster_labels))
np.savetxt('./model/playlist_cluster_labels_train.csv', playlist_cluster_labels, delimiter=',', fmt='%i')
