import pickle
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from model.helper_functions import stub_withhold_split, val_test_features, r_precision, hit_rate, ndcg
from model.k5_centroid_model import predict_tracks

start_time = time.time(), time.ctime()
print(f'Start time: {start_time[1]}')

# Build df of playlists to classify in clusters
test_pids = np.genfromtxt('../data/test_pids.csv', skip_header=1, dtype=int)

# Import data to memory so it is not loaded from disk for every loop iteration
playlist_df = pd.read_csv('../data/playlists.csv')
track_df = pd.read_csv('../data/songs_100000_feat_cleaned.csv', index_col='track_uri')
top_artists = np.genfromtxt('../data/top_playlist_defining_artists_train.csv', usecols=0,
                            skip_header=0, delimiter=',', dtype=str)

# Create output vessels
test_stub_feat_dfs = [None] * len(test_pids)
errors = 0

# Loop through pids and make features
for idx, pid in enumerate(test_pids):
    try:
        stub_tracks, withhold_tracks = stub_withhold_split(pid)
        stub_playlist_feats = val_test_features(stub_tracks, track_df=track_df, top_artists=top_artists, pid=pid)
        test_stub_feat_dfs[idx] = stub_playlist_feats
    except Exception as e:
        print(f'Error for pid {pid}: \n{e}')
        errors += 1

    if (idx + 1) % 100 == 0:
        print(f'[{time.ctime()}] Progress {idx + 1} playlists and {errors} errors')

playlist_features_test = pd.concat(test_stub_feat_dfs, axis=0)

end_time = time.time(), time.ctime()
time_elapsed = end_time[0] - start_time[0]
time_elapsed = time.strftime('%H:%M:%S', time.gmtime(time_elapsed))
print(f'End time: {end_time[1]}, Time elapsed: {time_elapsed}')

# Save output
playlist_features_test.to_csv('../data/playlist_features_with_artists_test.csv', sep=',', index=True)

start_time = time.time(), time.ctime()
print(f'Start time: {start_time[1]}')

# Build df of playlists to classify in clusters

# Import data to memory so it is not loaded from disk for every loop iteration
model = pickle.load(open('../model/nearest_cluster_train.pkl', 'rb'))
playlist_df = pd.read_csv('../data/playlists.csv')
track_df = pd.read_csv('../data/songs_100000_feat_cleaned.csv', index_col='track_uri')
top_artists = np.genfromtxt('../data/top_playlist_defining_artists_train.csv', usecols=0,
                            skip_header=0, delimiter=',', dtype=str)
frequency_dict = pickle.load(open('./cluster_track_frequencies.pkl', 'rb'))
features_df = pd.read_csv('../data/playlist_features_with_artists_test.csv', index_col=0)

# Create output vessels
test_clusters = pd.DataFrame(index=pd.Index(test_pids), columns=['cluster_id', 'n_predictions'])
test_predictions = {}
test_withheld = {}
errors = 0

# Loop through pids and make predictions
for idx, pid in enumerate(test_pids):
    try:
        stub_tracks, withhold_tracks = stub_withhold_split(pid)
        cluster, predictions = predict_tracks(track_uri_array=stub_tracks, n_tracks=len(stub_tracks),
                                              frequency_dict=frequency_dict,
                                              playlist_df=playlist_df, track_df=track_df, model=model,
                                              top_artists=top_artists, pid=pid, features_df=features_df)
        test_predictions[pid] = predictions
        test_withheld[pid] = withhold_tracks
        test_clusters.at[pid, :] = cluster, predictions.shape[0]
    except Exception as e:
        print(f'Error for pid {pid}: \n{e}')
        test_clusters.at[pid, :] = np.NaN, np.NaN
        errors += 1

    if (idx + 1) % 100 == 0:
        print(f'[{time.ctime()}] Progress {idx + 1} playlists and {errors} errors')

end_time = time.time(), time.ctime()
time_elapsed = end_time[0] - start_time[0]
time_elapsed = time.strftime('%H:%M:%S', time.gmtime(time_elapsed))
print(f'End time: {end_time[1]}, Time elapsed: {time_elapsed}')

# Save output
test_clusters.to_csv('./k_means_clusters_test.csv', sep=',', index=True)
pickle.dump(test_predictions, open('./k_means_predictions_test.pkl', 'wb'))
pickle.dump(test_withheld, open('./k_means_withheld_test.pkl', 'wb'))

# Load predictions for the test set
test_clusters = np.genfromtxt('./k_means_clusters_test.csv', skip_header=1, dtype=int, delimiter=',', usecols=[0, 1])
test_predictions = pickle.load(open('./k_means_predictions_test.pkl', 'rb'))
test_withheld = pickle.load(open('./k_means_withheld_test.pkl', 'rb'))

# Create output vessel
test_scores = np.zeros((test_clusters.shape[0], 7))

for idx, (pid, cluster_id) in enumerate(test_clusters):
    # Load list of withheld tracks
    withhold_tracks = test_withheld[pid]

    # Load list of predicted tracks
    predictions = test_predictions[pid].track_uri

    # Figure out how many tracks to use in the scoring (and don't score for more than predicted)
    n_predictions = len(predictions)
    n_10 = min(n_predictions, 10)
    n_withheld = min(n_predictions, len(withhold_tracks))
    n_7withheld_over_3 = min(n_predictions, int(n_withheld * 7 / 3))

    predictions_10 = predictions[:n_10]
    predictions_n_withheld = predictions[:n_withheld]
    predictions_7withheld_over_3 = predictions[:n_7withheld_over_3]

    # Score the predictions!
    hit_rate_10 = hit_rate(withhold_tracks=withhold_tracks, predicted_tracks=predictions_10)
    rps_withheld = r_precision(withhold_tracks=withhold_tracks, predicted_tracks=predictions_n_withheld)
    rps_7withheld_over_3 = r_precision(withhold_tracks=withhold_tracks, predicted_tracks=predictions_7withheld_over_3)
    ndcg_withheld = ndcg(withhold_tracks=withhold_tracks, predicted_tracks=predictions_n_withheld)
    ndcg_7withheld_over_3 = ndcg(withhold_tracks=withhold_tracks, predicted_tracks=predictions_7withheld_over_3)

    # Write to array
    test_scores[
        idx] = pid, cluster_id, hit_rate_10, rps_withheld, rps_7withheld_over_3, ndcg_withheld, ndcg_7withheld_over_3

np.savetxt("./k9_scores_test.csv", test_scores, delimiter=",",
           header='pid,cluster_id,hit_rate_10,rps_withheld,rps_7withheld_over_3,ndcg_withheld,ndcg_7withheld_over_3')

# Load score data
plot_scores = test_scores[:, 2:]
score_names = ['Hit Rate (10 Predictions)', 'R-Precision (# of Withheld Tracks)',
               'R-Precision (# of Calibration Tracks)', 'NDCG (# of Withheld Tracks)', 'NDCG (# of Calibration Tracks)']
model_name = 'K Centroid'
set_name = 'Test'

# Plot each score
fig, ax = plt.subplots(5, 1, figsize=(7, 25))
for i in range(plot_scores.shape[1]):
    scores = plot_scores[:, i]
    sns.distplot(scores, kde=False, rug=False, hist_kws={'rwidth': 1, 'edgecolor': 'white', 'alpha': 1}, ax=ax[i],
                 color="#1db954")
    ax[i].axvline(np.mean(scores), label='Mean = {}'.format(round(np.mean(scores), 3)), color='k')
    ax[i].legend()
    ax[i].set_title(f'{score_names[i]} on the {set_name} Set, {model_name}')
fig.tight_layout(rect=[0, 0.03, 1, 0.97])
fig.suptitle(f'{model_name} Model Evaluation Metrics on the {set_name} Set', size='xx-large')
plt.show()
