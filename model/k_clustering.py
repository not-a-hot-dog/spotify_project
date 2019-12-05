import pandas as pd
import numpy as np
from model.helper_functions import build_playlist_features
from sklearn.cluster import KMeans
import pickle

print('Finding playlist features')
playlist_list = np.genfromtxt('./data/train_pids.csv', skip_header=1, dtype=int)
playlist_features = build_playlist_features(playlist_list)
playlist_features.to_csv('./data/playlist_features.csv')

print('Finding top artists')
# Find the top artists who dominate playlists
top_playlist_defining_artists = playlist_features.artist_uri_top.value_counts(normalize=False)
top_playlist_defining_artists.to_csv('./data/top_playlist_defining_artists_train_all.csv', header=True)
top_playlist_defining_artists = playlist_features.artist_uri_top.value_counts().index.values[:50]
np.savetxt('./data/top_playlist_defining_artists_train.csv', top_playlist_defining_artists, delimiter=',', fmt="%s")

# Keep only those artists who dominate playlists and one hot encode
artists_to_keep = playlist_features.artist_uri_top.isin(top_playlist_defining_artists)
playlist_features.artist_uri_top = playlist_features.artist_uri_top[artists_to_keep]
playlist_features.artist_uri_freq = playlist_features.artist_uri_freq[artists_to_keep]
playlist_features.artist_uri_freq.fillna(0, inplace=True)


top_artist_dummies = pd.get_dummies(playlist_features.artist_uri_top)
playlist_features = pd.concat([playlist_features, top_artist_dummies], axis=1)
playlist_features.drop(['artist_uri_top'], axis=1, inplace=True)
playlist_features.to_csv('./data/playlist_features_with_artists.csv')

# Set desired number of clusters
n_clusters = int(np.sqrt(len(playlist_features)))

print('Making clusters')
# Make clusters
kmeans = KMeans(n_clusters=n_clusters, verbose=0, algorithm='auto')
kmeans.fit(playlist_features)


print('Saving clusters')
# Saving the clusters
pickle.dump(kmeans, open('./model/kmeans_cluster_train.pickle', 'wb'))
cluster_centers = kmeans.cluster_centers_
np.savetxt('./model/kmeans_cluster_centers_train.csv', cluster_centers, delimiter=',')

