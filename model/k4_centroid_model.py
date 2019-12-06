import pickle
import pandas as pd
import numpy as np
from model.helper_functions import get_summary_features, get_tracks



def predict_cluster(track_uri_array):

    """
    :param track_uri_array: an array of tracks
    :return: the predicted cluster id for the array of tracks provided
    """

    # Load nearest cluster model
    nearest_cluster = pickle.load(open('./model/nearest_cluster_train.pkl', 'rb'))

    # Load list of dominating artists
    top_playlist_defining_artists = np.genfromtxt('./data/top_playlist_defining_artists_train.csv', usecols=0,
                                                  skip_header=0, delimiter=',', dtype=str)

    # Get summary features
    stub_playlist_features = get_summary_features(track_uri_array, trackfile='./data/songs_100000_feat_cleaned.csv')

    artists_to_keep = stub_playlist_features.artist_uri_top.isin(top_playlist_defining_artists)

    stub_playlist_features.artist_uri_top = stub_playlist_features.artist_uri_top[artists_to_keep]
    stub_playlist_features.artist_uri_freq = stub_playlist_features.artist_uri_freq[artists_to_keep]
    stub_playlist_features.artist_uri_freq.fillna(0, inplace=True)
    stub_artist_dummies = pd.get_dummies(stub_playlist_features.artist_uri_top)
    top_artist_dummies = pd.DataFrame(columns=top_playlist_defining_artists)

    top_artist_dummies = pd.concat([top_artist_dummies, stub_artist_dummies], axis=1)
    top_artist_dummies.fillna(0, inplace=True)

    stub_playlist_features = pd.concat([stub_playlist_features, top_artist_dummies], axis=1)
    stub_playlist_features.drop(['artist_uri_top'], axis=1, inplace=True)

    dist, cluster_id = nearest_cluster.kneighbors(stub_playlist_features)

    return cluster_id


def predict_songs(track_uri_array, n_tracks=30):
    # TODO: Make this a function that takes in an array of tracks and predicts new songs
    """
    :param track_uri_array: an array of tracks
    :param n_tracks: The number of tracks to predict
    :return: an array of predicted tracks and probabilities of length n_songs
    """

    cluster = predict_cluster(track_uri_array)

    pass

# pid = 22124
# print(predict_cluster(get_tracks(pid)))
