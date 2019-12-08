import pickle
import numpy as np
import pandas as pd
import time
from model.helper_functions import stub_withhold_split, val_test_features


start_time = time.time(), time.ctime()
print(f'Start time: {start_time[1]}')

# Build df of playlists to classify in clusters
val_pids = np.genfromtxt('../data/val_pids.csv', skip_header=1, dtype=int)

# Import data to memory so it is not loaded from disk for every loop iteration
playlist_df = pd.read_csv('../data/playlists.csv')
track_df = pd.read_csv('../data/songs_100000_feat_cleaned.csv', index_col='track_uri')
top_artists = np.genfromtxt('../data/top_playlist_defining_artists_train.csv', usecols=0,
                            skip_header=0, delimiter=',', dtype=str)

# Create output vessels
val_stub_feat_dfs = [None]*len(val_pids)
errors = 0

# Loop through pids and make features
for idx, pid in enumerate(val_pids):
    try:
        stub_tracks, withhold_tracks = stub_withhold_split(pid)
        stub_playlist_feats = val_test_features(stub_tracks, track_df=track_df, top_artists=top_artists)
        val_stub_feat_dfs[idx] = stub_playlist_feats
    except Exception as e:
        print(f'Error for pid {pid}: \n{e}')
        errors += 1

    if (idx + 1) % 100 == 0:
        print(f'[{time.ctime()}] Progress {idx+1} playlists and {errors} errors')

playlist_features_val = pd.concat(val_stub_feat_dfs, axis=0)

end_time = time.time(), time.ctime()
time_elapsed = end_time[0]-start_time[0]
time_elapsed = time.strftime('%H:%M:%S', time.gmtime(time_elapsed))
print(f'End time: {end_time[1]}, Time elapsed: {time_elapsed}')

# Save output
playlist_features_val.to_csv('../data/playlist_features_with_artists_val.csv', sep=',', index=True)
