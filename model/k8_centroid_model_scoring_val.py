from model.helper_functions import r_precision, hit_rate, ndcg
import pickle
import numpy as np

# Load predictions for the validation set
val_clusters = np.genfromtxt('./k_means_clusters_val.csv', skip_header=1, dtype=int, delimiter=',', usecols=[0, 1])
val_predictions = pickle.load(open('./k_means_predictions_val.pkl', 'rb'))
val_withheld = pickle.load(open('./k_means_withheld_val.pkl', 'rb'))

# Create output vessel
val_scores = np.zeros((val_clusters.shape[0], 7))

for idx, (pid, cluster_id) in enumerate(val_clusters):
    # Load list of withheld tracks
    withhold_tracks = val_withheld[pid]

    # Load list of predicted tracks
    predictions = val_predictions[pid].track_uri

    # Figure out how many tracks to use in the scoring (and don't score for more than predicted)
    n_predictions = len(predictions)
    n_10 = min(n_predictions, 10)
    n_withheld = min(n_predictions, len(withhold_tracks))
    n_7withheld_over_3 = min(n_predictions, int(n_withheld * 7/3))

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
    val_scores[idx] = pid, cluster_id, hit_rate_10, rps_withheld, rps_7withheld_over_3, ndcg_withheld, ndcg_7withheld_over_3

np.savetxt("./k9_scores_val.csv", val_scores, delimiter=",",
           header='pid,cluster_id,hit_rate_10,rps_withheld,rps_7withheld_over_3,ndcg_withheld,ndcg_7withheld_over_3')
