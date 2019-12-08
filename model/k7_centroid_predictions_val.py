import pickle
import numpy as np
import pandas as pd
import time
from model.helper_functions import stub_withhold_split
from model.k5_centroid_model import predict_tracks

start_time = time.time(), time.ctime()
print(f'Start time: {start_time[1]}')

# Build df of playlists to classify in clusters
val_pids = np.genfromtxt('../data/val_pids.csv', skip_header=1, dtype=int)

# Import data to memory so it is not loaded from disk for every loop iteration
model = pickle.load(open('../model/nearest_cluster_train.pkl', 'rb'))
playlist_df = pd.read_csv('../data/playlists.csv')
track_df = pd.read_csv('../data/songs_100000_feat_cleaned.csv', index_col='track_uri')
top_artists = np.genfromtxt('../data/top_playlist_defining_artists_train.csv', usecols=0,
                            skip_header=0, delimiter=',', dtype=str)
frequency_dict = pickle.load(open('./cluster_track_frequencies.pkl', 'rb'))
features_df = pd.read_csv('../data/playlist_features_with_artists_val.csv', index_col=0)

# Create output vessels
val_clusters = pd.DataFrame(index=pd.Index(val_pids), columns=['cluster_id', 'n_predictions'])
val_predictions = {}
val_withheld = {}
errors = 0

# Loop through pids and make predictions
for idx, pid in enumerate(val_pids):
    try:
        stub_tracks, withhold_tracks = stub_withhold_split(pid)
        cluster, predictions = predict_tracks(track_uri_array=stub_tracks, n_tracks=len(stub_tracks), frequency_dict=frequency_dict,
                                              playlist_df=playlist_df, track_df=track_df, model=model,
                                              top_artists=top_artists, pid=pid, features_df=features_df)
        val_predictions[pid] = predictions
        val_withheld[pid] = withhold_tracks
        val_clusters.at[pid, :] = cluster, predictions.shape[0]
    except Exception as e:
        print(f'Error for pid {pid}: \n{e}')
        val_clusters.at[pid, :] = np.NaN, np.NaN
        errors += 1

    if (idx + 1) % 100 == 0:
        print(f'[{time.ctime()}] Progress {idx+1} playlists and {errors} errors')


end_time = time.time(), time.ctime()
time_elapsed = end_time[0]-start_time[0]
time_elapsed = time.strftime('%H:%M:%S', time.gmtime(time_elapsed))
print(f'End time: {end_time[1]}, Time elapsed: {time_elapsed}')

# Save output
val_clusters.to_csv('./k_means_clusters_val.csv', sep=',', index=True)
pickle.dump(val_predictions, open('./k_means_predictions_val.pkl', 'wb'))
pickle.dump(val_withheld, open('./k_means_withheld_val.pkl', 'wb'))

