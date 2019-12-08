import pandas as pd
import numpy as np


# Helper function to get tracks for a pid
from sklearn.model_selection import train_test_split


def get_tracks(pid, playlist_df):
    tracks = list(playlist_df.loc[playlist_df['pid'] == pid, 'track_uri'])
    return tracks


# Helper function to get summary of track features from an array of tracks (e.g., get_tracks output)
def get_summary_features(track_uri_array, track_df):
    subset_track_df = track_df.loc[track_uri_array, :]
    features_mean = subset_track_df.describe().loc[['std'], :].reset_index(drop=True)
    features_mean.columns = [str(col) + '_mean' for col in features_mean.columns]
    features_std = subset_track_df.describe().loc[['std'], :].reset_index(drop=True)
    features_std.columns = [str(col) + '_std' for col in features_std.columns]
    artist_uri_freq = subset_track_df.artist_uri.value_counts(normalize=True)[0]
    if artist_uri_freq > 0.3:  # If the top artist doesn't have 30% of track in the playlist, ignore
        top_artist = pd.DataFrame([{'artist_uri_top': subset_track_df.artist_uri.value_counts(normalize=True).index[0],
                                    'artist_uri_freq': artist_uri_freq
                                    }]).reset_index(drop=True)
    else:
        top_artist = pd.DataFrame([{'artist_uri_top': np.NaN, 'artist_uri_freq': 0}])

    features = pd.concat([features_mean, features_std, top_artist], axis=1, sort=False)
    return features


def val_test_features(track_uri_array, track_df, top_artists):
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
    top_artist_dummies = pd.concat([top_artist_dummies, stub_artist_dummies], axis=0, sort=False)
    top_artist_dummies.fillna(0, inplace=True)
    stub_playlist_features = pd.concat([stub_playlist_features, top_artist_dummies], axis=1)
    stub_playlist_features.drop(['artist_uri_top'], axis=1, inplace=True)
    stub_playlist_features.index = [pid]

    return stub_playlist_features


def build_playlist_features(pid_list, playlist_df, track_df):
    output = pd.DataFrame()
    for pid in pid_list:
        output = output.append(get_summary_features(get_tracks(pid, playlist_df), track_df))
    output = output.set_index(pd.Index(pid_list))
    return output


def stub_withhold_split(pid: int, playlist_df: pd.DataFrame=None):
    if playlist_df is None: playlist_df = pd.read_csv('../data/playlists.csv')
    tracks = get_tracks(pid, playlist_df)
    stub_tracks, withhold_tracks = train_test_split(tracks, random_state=21, test_size=0.3)
    return stub_tracks, withhold_tracks


# Model Evaluation Metrics, adapted from https://recsys-challenge.spotify.com/rules
def r_precision(predicted_tracks: np.ndarray, withhold_tracks: np.ndarray):
    mask = np.isin(withhold_tracks, predicted_tracks) # Give credit for predicting a track that's in withhold twice!
    r_precision_score = np.sum(mask)/len(withhold_tracks)
    return r_precision_score


def hit_rate(predicted_tracks: np.ndarray, withhold_tracks: np.ndarray):
    mask = np.isin(predicted_tracks, withhold_tracks)
    hit_rate_score = np.sum(mask)/len(predicted_tracks)
    return hit_rate_score


def dcg(withhold_tracks, predicted_tracks):
    try:
        mask = np.isin(predicted_tracks, withhold_tracks)
        score = np.sum(mask[0]) + np.sum(mask[1:] / np.log2(np.arange(2, mask.size + 1)))
    except Exception:
        score = np.NaN
    return score


def idcg(withhold_tracks):
    n_withheld = len(withhold_tracks)
    ones = np.ones(n_withheld-1)
    score = 1 + np.sum(ones / np.log2(np.arange(2, n_withheld + 1)))
    return max(score, 1)


def ndcg(withhold_tracks, predicted_tracks):
    dcg_score = dcg(withhold_tracks=withhold_tracks, predicted_tracks=predicted_tracks)
    idcg_score = idcg(withhold_tracks)
    ndcg_score = dcg_score/idcg_score
    return ndcg_score

