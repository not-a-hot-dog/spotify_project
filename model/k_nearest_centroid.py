import pickle
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from model.helper_functions import build_playlist_features

cluster_centers = np.genfromtxt('./model/kmeans_cluster_centers_train.csv', skip_header=0, delimiter=',')

# Fit the neighbors classifier
nearest_cluster = NearestNeighbors(n_neighbors=1)
nearest_cluster.fit(cluster_centers)
pickle.dump(nearest_cluster, open('./model/nearest_cluster_train.pickle', 'wb'))

# Build df of playlists to classify in clusters
playlist_list = np.genfromtxt('./data/val_pids.csv', skip_header=1, dtype=int)[0:1]
test_playlist_features = build_playlist_features(playlist_list)

top_playlist_defining_artists = np.genfromtxt('./data/top_playlist_defining_artists_train.csv', usecols=0, skip_header=0, delimiter=',', dtype=str)

# Keep only those artists who dominate playlists and one hot encode
artists_to_keep = test_playlist_features.artist_uri_top.isin(top_playlist_defining_artists)
test_playlist_features.artist_uri_top = test_playlist_features.artist_uri_top[artists_to_keep]
test_playlist_features.artist_uri_freq = test_playlist_features.artist_uri_freq[artists_to_keep]
test_playlist_features.artist_uri_freq.fillna(0, inplace=True)
test_artist_dummies = pd.get_dummies(test_playlist_features.artist_uri_top)
top_artist_dummies = pd.DataFrame(columns=top_playlist_defining_artists)

top_artist_dummies = pd.concat([top_artist_dummies, test_artist_dummies], axis=1)
top_artist_dummies.fillna(0, inplace=True)

test_playlist_features = pd.concat([test_playlist_features, top_artist_dummies], axis=1)
test_playlist_features.drop(['artist_uri_top'], axis=1, inplace=True)

dist, cluster_id = nearest_cluster.kneighbors(test_playlist_features)

