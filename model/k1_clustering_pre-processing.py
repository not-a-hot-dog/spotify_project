import pandas as pd
import numpy as np
from model.helper_functions import build_playlist_features

print('Reading data into memory')
pid_list = np.genfromtxt('../data/train_pids.csv', skip_header=1, dtype=int)
playlistfile = '../data/playlists.csv'
playlist_df = pd.read_csv(playlistfile)
trackfile = '../data/songs_100000_feat_cleaned.csv'
track_df = pd.read_csv(trackfile, index_col='track_uri')

print('Finding playlist features')
playlist_features = build_playlist_features(pid_list, playlist_df, track_df)
playlist_features.to_csv('../data/playlist_features_train.csv')

print('Finding top artists')
# Find the top artists who dominate playlists
top_playlist_defining_artists = playlist_features.artist_uri_top.value_counts(normalize=False)
top_playlist_defining_artists.to_csv('../data/top_playlist_defining_artists_train_all.csv', header=True)
top_playlist_defining_artists = playlist_features.artist_uri_top.value_counts().index.values[:50]
np.savetxt('../data/top_playlist_defining_artists_train.csv', top_playlist_defining_artists, delimiter=',', fmt="%s")

# Keep only those artists who dominate playlists and one hot encode
artists_to_keep = playlist_features.artist_uri_top.isin(top_playlist_defining_artists)
playlist_features.artist_uri_top = playlist_features.artist_uri_top[artists_to_keep]
playlist_features.artist_uri_freq = playlist_features.artist_uri_freq[artists_to_keep]
playlist_features.artist_uri_freq.fillna(0, inplace=True)

top_artist_dummies = pd.get_dummies(playlist_features.artist_uri_top)
playlist_features = pd.concat([playlist_features, top_artist_dummies], axis=1)
playlist_features.drop(['artist_uri_top'], axis=1, inplace=True)
playlist_features.to_csv('../data/playlist_features_with_artists_train.csv')
