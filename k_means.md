# k-Centroid Model

## Overview
For this model, we attempt, provided a list of tracks, to evaluate the distribution of features in these tracks, identify a cluster of similar playlists, and recommend a list of additional tracks that are popular in the cluster for the user.

We implemented this using a k-Centroid approach. We first use k-means clustering on the full training dataset of 13084 playlists in an attempt to algorithmically identify natural clusters of playlists in high-dimensional space. Next we use the  playlists (with cluster labels) to build a  to build a frequency distribution of songs likely to mesh well with a playlist in a given cluster. Finally, we fit a k-NearestNeighbors classifier to predict the nearest cluster for a given playlist, and use this cluster to recommend songs from the frequency distribution.

## Methodology
### Cluster Identification - k-Means
We used k-Means Clustering to identify groups of playlists that have similar features. k-Means Clustering is an unsupervised machine learning algorithm which groups similar observations together in a fixed number of `k` clusters to discover underlying patterns.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/k_means_example.png" title="4-means clustering" width="400"/>
</p>

The k-Means algorithm tries to cluster data by separating observations into groups of equal variance. Based on the input parameters, namely the number of clusters `k`, and a vector of unlabeled input data, the k-Means algorithm first proposes a center for each cluster. Next, it assigns each data point to its nearest cluster centroid. Then, it iterates over the cluster centers in an attempt to reduce `inertia` - the within cluster sum of squares. The algorithm continues to iterate until it converges to an inertia value that is below a threshold. 

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/k_means_inertia.png" title="Inertia" height="100"/>
</p>

As k-Means is unsupervised, it is a powerful method for identifying patterns in unlabeled data where the ground truth is not known. Given that our exploratory data analysis found that individual song features do not differentiate individual playlists, k-Means Clustering allows us to consider the group characteristics of groups of playlists in the absence of manually labelled groupings. This gives us a baseline from which to build a k-NearestNeighbor classifier to classify heretofore unseen playlists in clusters of similar playlists. 

In our implementation of k-means, we specified `k=114` clusters.

### Cluster Prediction - k-NearestNeighbors
We used k-Nearest neighbors to predict a cluster for a never-before-seen user-specified playlist.
 
k-NearestNeighbors is an unsupervised neighbors-based machine learning method. Given an as of yet unseen data point, it finds the `k` training samples closest in distance to the unseen data point and uses this to predict a classification.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/k_nearest_neighbor_meme.jpeg" title="Show me your best friend" width="400"/>
</p>

In our implementation for k-Centroid, we used `k=1` neighbors for our k-NearestNeighbor classifier. This is because for each cluster centroid in the data we used to fit the k-NN classifier, we only had one observation, as each cluster centroid is in itself a representation of an arbitrary number of playlists.

## Implementation
### Data Preparation
We trained our k-Means Clustering learner on an array of playlist features. In this array, each row is one of the 13,084 playlist in the training data set, and each column represents a summary of the features of the tracks in the playlist. Namely, these included:
* Mean value for of the `audio-features` (e.g., `acousticness`, `danceability`, `energy`, `tempo`, etc.) computed along the tracks in a playlist
* Standard deviation for of the `audio-features` (e.g., `acousticness`, `danceability`, `energy`, `tempo`, etc.) computed along the tracks in a playlist
* For playlists where more than 30% of tracks are by a "Top 50" artist 
    - The leading "Top 50" artist featured in the playlist (one-hot encoded)
    - The percentage of songs in the playlist by the leading artist
    - Note: Top 50 artists were selected from those appearing most frequently in training playlists

We constructed a `build_playlist_features` function to automate the construction of this dataset. It takes as an input a playlist `pid`, a `playlist` dataframe which maps playlists to tracks and artists, and an `audio-features` dataframe with estimated features of each track (e.g., Acousticness, Danceability, Energy, Tempo, etc.).

### K-Centroid Model and Predictions
#### Model Fitting
Our model fitting took these high-level steps:
1. Generate summary features of each train playlist
2. Use k-Means Clustering to define clusters of similar playlists (and their centroids)
3. Develop a `track_frequencies` dataframe of tracks that appear in each cluster
4. Fit the `nearest_cluster` k-NearestNeighbor classifier on the centroids of each cluster, to predict a cluster given an array of tracks

#### Predictions
To facilitate predictions for model validation, model testing, and end users, we developed the function `predict_tracks` to take a `track_uri_array` and return a sorted array of `track_predictions`. It does the following:
1. Construct the array of summary `playlist_features` for the input `track_uri_array`, using the `val_test_features` function which ensures compatibility of the returned array with the `nearest_cluster` classifier
2. Call the function `predict_cluster` to classify the `track_uri_array` into a playlist cluster using the `nearest_cluster` classifier and its `playlist_features`
3. Load `track_frequency` of each track in the `predicted_cluster`
4. Return a sorted array of `track_predictions` that occurred in the `predicted_cluster` but were not present in the input `track_uri_array`

### Model Validation and Testing
Our model validation and testing methodology requires that we randomly split the tracks in each playlist from the 1636 `validation` playlists and 1636 `test` [playlists] into an array of `stub_tracks` to calibrate the k-NearestNeighbor `nearest_cluster` classifier and an array of `withhold_tracks` to score the model predictions returned by `predict_tracks`. This function takes as input a playlist `pid` and a `playlist` dataframe of track in the playlist. It returns an array of `stub_tracks` for calibration (fixed at 70% of the songs in each playlist) and an array of `withhold_tracks` for scoring predictions (fixed at 30% of the tracks in the playlist).
 
We developed functions for `hit_rate`, `r_precision`, and `ncdg` to standardize the evaluation of model performance across models given an array of the `predicted_tracks` and `withhold_tracks` for each playlist in the `validation` and `test` sets.

## Model Performance
We have identified three metrics - RPS, NDCG and hit-rate - to evaluate all models we developed for this project. To obtain the final metrics for a given model, we compute the mean of the scores across all the playlists in the test set, and across different values for number of recommendations.

The histograms below show the distribution of scores across the three different metrics, with two distributions for RPS and NDCG, one each for the case where the number of recommendations equals the number of songs used for calibration and where it equals the number of withheld songs.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/k_centroid_performance.png" title="k-Centroid Model Performance"/>
</p>

Overall, the k-Centroid model achieved an R-Precision score of 0.219 and a Normalized Discounted Cumulative Gain (NDCG) score of 0.203 when producing the same number of recommendations as the number of songs used to calibrate the model. The R-precision score of 0.219 implies that if given a list of 100 songs, the model predicts 100 songs, out of which 22 on average would be songs that were in list of withheld songs not provided to the model initially.
