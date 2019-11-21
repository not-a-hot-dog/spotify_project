import pandas as pd
import numpy as np

# Helper function to get tracks for a pid
def get_tracks(pid, playlistfile = './data/playlists.csv'):
    playlist_df = pd.read_csv(playlistfile)
    tracks = list(playlist_df.loc[playlist_df['pid'] == pid, 'track_uri'])
    return tracks

# Helper function to get summary of track features from an array of tracks (e.g., get_tracks output)
def get_summary_features(track_uri_array, trackfile = './data/songs_100000_feat_cleaned.csv'):
    track_df = pd.read_csv(trackfile, index_col='track_uri')
    track_df = track_df.loc[track_uri_array,:]
    features_mean = track_df.describe().loc[['std'], :].reset_index(drop = True)
    features_mean.columns = [str(col) + '_mean' for col in features_mean.columns]
    features_std = track_df.describe().loc[['std'], :].reset_index(drop = True)
    features_std.columns = [str(col) + '_std' for col in features_std.columns]
    artist_uri_freq = track_df.artist_uri.value_counts(normalize=True)[0]
    if artist_uri_freq > 0.3: # If the top artist doesn't have 30% of track in the playlist, ignore
        top_artist = pd.DataFrame([{'artist_uri_top': track_df.artist_uri.value_counts(normalize=True).index[0],
                                    'artist_uri_freq': artist_uri_freq
                                    }]).reset_index(drop=True)
    else:
        top_artist = pd.DataFrame([{'artist_uri_top': np.NaN, 'artist_uri_freq': np.NaN}])

    features = pd.concat([features_mean, features_std, top_artist], axis=1, sort=False)
    return features

def build_playlist_features(pid_list):
    output = pd.DataFrame()
    for pid in pid_list:
        output = output.append(get_summary_features(get_tracks(pid)))
    output = output.set_index(pd.Index(pid_list))
    return output