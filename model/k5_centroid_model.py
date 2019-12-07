import pickle
import pandas as pd
import numpy as np

from model.helper_functions import get_summary_features, get_tracks, stub_withold_split


def predict_cluster(track_uri_array, playlist_df, track_df, model, top_artists):
    """
    :return: the predicted cluster id for the array of tracks provided
    """

    # Load nearest cluster model
    nearest_cluster = model

    # Load list of dominating artists
    top_playlist_defining_artists = top_artists

    # Get summary features
    stub_playlist_features = get_summary_features(track_uri_array, track_df)

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

    return int(cluster_id)


def predict_tracks(track_uri_array, n_tracks=30, frequency_dict: dict = None, playlist_df: pd.DataFrame = None,
                   track_df: pd.DataFrame = None, model=None,
                   top_artists: np.ndarray = None):
    """
    :param top_artists:
    :param model:
    :param track_df:
    :param playlist_df:
    :param frequency_dict:
    :param track_uri_array: an array of tracks
    :param n_tracks: The number of tracks to predict
    :return: an array of predicted tracks and probabilities of length n_songs
    """

    # Load nearest cluster model
    if model is None: model = pickle.load(open('../model/nearest_cluster_train.pkl', 'rb'))
    if playlist_df is None: playlist_df = pd.read_csv('../data/playlists.csv')
    if track_df is None: track_df = pd.read_csv('../data/songs_100000_feat_cleaned.csv', index_col='track_uri')
    if top_artists is None: top_artists = np.genfromtxt('../data/top_playlist_defining_artists_train.csv', usecols=0,
                                                        skip_header=0, delimiter=',', dtype=str)
    if frequency_dict is None: frequency_dict = pickle.load(open('./cluster_track_frequencies.pkl', 'rb'))

    # Predict the cluster given the provided track_uris
    predicted_cluster = predict_cluster(track_uri_array, playlist_df, track_df, model, top_artists)

    # Find the frequency with which tracks appear in that cluster
    track_frequencies = frequency_dict[predicted_cluster]

    # Exclude tracks which are already in the input track_uri_array
    excluded_recommendations = track_frequencies.index.isin(track_uri_array)
    track_frequencies = track_frequencies[~excluded_recommendations]

    # Return n_tracks predictions
    track_predictions = track_frequencies.reset_index()
    track_predictions.columns = ['track_uri', 'probability']
    track_predictions = track_predictions.nlargest(n_tracks, 'probability')
    return predicted_cluster, track_predictions


# It works!
# pid = 22124
# stub_tracks, withold_tracks = stub_withold_split(pid)
# cluster, predictions = predict_tracks(stub_tracks)
# print(predictions)
