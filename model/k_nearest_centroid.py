import pickle
import numpy as np
from sklearn.neighbors import NearestNeighbors

cluster_centers = np.genfromtxt('./model/kmeans_cluster_centers_train.csv', skip_header=0, delimiter=',')

# Fit the neighbors classifier
nearest_cluster = NearestNeighbors(n_neighbors=1)
nearest_cluster.fit(cluster_centers)
pickle.dump(nearest_cluster, open('./model/nearest_cluster_train.pickle', 'wb'))
