import pickle

import pandas as pd
import numpy as np

print('Read in cluster labels')
playlist_cluster_labels = pd.read_csv('./playlist_cluster_labels_train.csv', header=None, delimiter=',', dtype=int,
                                      names=['pid', 'cluster_id'])
clusters = np.unique(playlist_cluster_labels.cluster_id)

print('Read in the playlist dataframe')
playlistfile = '../data/playlists.csv'
playlist_df = pd.read_csv(playlistfile, header=0, usecols=('pid', 'track_uri'))

frequency_dict = {}

print('Loop through the clusters and return the frequency each track for each cluster')
for cluster in clusters:
    cluster_pids = playlist_cluster_labels.pid[playlist_cluster_labels.cluster_id == cluster]
    tracks = playlist_df.track_uri[playlist_df.pid.isin(cluster_pids)]
    track_frequencies = tracks.value_counts(normalize=True)
    frequency_dict[cluster] = track_frequencies

pickle.dump(frequency_dict, open('./cluster_track_frequencies.pkl', 'wb'))

