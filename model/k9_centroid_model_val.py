import pickle
import numpy as np
import pandas as pd
import time
from model.helper_functions import stub_withhold_split, r_precision
from model.k5_centroid_model import predict_tracks

start_time = time.time(), time.ctime()
print(f'Start time: {start_time[1]}')

# Build df of playlists to classify in clusters
val_pids = np.genfromtxt('../data/val_pids.csv', skip_header=1, dtype=int)[:10]

# Import data to memory so it is not loaded from disk for every loop iteration
model = pickle.load(open('../model/nearest_cluster_train.pkl', 'rb'))
playlist_df = pd.read_csv('../data/playlists.csv')
track_df = pd.read_csv('../data/songs_100000_feat_cleaned.csv', index_col='track_uri')
top_artists = np.genfromtxt('../data/top_playlist_defining_artists_train.csv', usecols=0,
                            skip_header=0, delimiter=',', dtype=str)
frequency_dict = pickle.load(open('./cluster_track_frequencies.pkl', 'rb'))

# Create output vessels
val_results = pd.DataFrame(index=pd.Index(val_pids), columns=['cluster_id', 'r_precision'])
val_predictions = {}
val_withheld = {}

# Loop through pids and make predictions
for pid in val_pids:
    stub_tracks, withhold_tracks = stub_withhold_split(pid)
    cluster, predictions = predict_tracks(stub_tracks, n_tracks=len(withhold_tracks), frequency_dict=frequency_dict,
                                          playlist_df=playlist_df, track_df=track_df, model=model,
                                          top_artists=top_artists)
    rps = r_precision(predictions.track_uri, withhold_tracks)
    val_predictions[pid] = predictions
    val_withheld[pid] = withhold_tracks
    val_results.at[pid, :] = cluster, rps

end_time = time.time(), time.ctime()
time_elapsed = end_time[0]-start_time[0]
time_elapsed = time.strftime('%H:%M:%S', time.gmtime(time_elapsed))
print(f'End time: {end_time[1]}, Time elapsed: {time_elapsed}')
print('Mean r_precision score:', val_results.r_precision.mean())

# Save output
val_results.to_csv('./k_means_results_val', sep=',', index=None)
pickle.dump(val_predictions, open('./k_means_predictions_val.pkl', 'wb'))
pickle.dump(val_withheld, open('./k_means_withheld_val.pkl', 'wb'))
