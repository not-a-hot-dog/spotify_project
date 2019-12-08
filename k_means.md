## k-Centroid Model

### Overview
Provided a list of tracks selected by a user, we can evaluate the distribution of features in these tracks, identify a cluster of similar playlists, and recommend additional tracks for the user that are appear frequently in the cluster.

We implemented this using a k-Centroid approach. We first use k-means clustering on the full training dataset of 13084 playlists in an attempt to algorithmically identify natural clusters of playlists in high-dimensional space. Next we use the  playlists (with cluster labels) to build a  to build a frequency distribution of songs likely to mesh well with a playlist in a given cluster. Finally, we fit a k-NearestNeighbors model to predict the nearest cluster for a given playlist, and use this cluster to recommend songs from the frequency distribution.

### Data Preparation

#### Train/Test/Val
#### Calibration/Withhold

#### Playlist Features


### Methodology
#### Cluster Identification - k-Means
We used k-Means Clustering to identify groups of playlists that have similar features. k-Means Clustering is an unsupervised machine learning algorithm which groups similar observations together in a fixed number of `k` clusters to discover underlying patterns.

The k-Means algorithm tries to cluster data by separating observations into groups of equal variance. Based on the model parameters, namely the number of clusters `k`, and a vector of unlabeled input data, the k-Means algorithm first proposes a center for each cluster. Next, it assigns each data point to its nearest cluster centroid. Then, it iterates over the cluster centers in an attempt to reduce `inertia` - the within cluster sum of squares. The algorithm continues to iterate until it converges to an inertia value that is below a threshold. 

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/k_means_inertia.png" title="Inertia" height="100"/>
</p>

As k-Means is unsupervised, it is a powerful method for identifying patterns in unlabeled data where the ground truth is not known. Given that our exploratory data analysis found that individual song features do not differentiate individual playlists, k-Means Clustering allows us to consider the group characteristics of groups of playlists in the absence of manually labelled groupings. This gives us a baseline from which to build a k-NearestNeighbor model to classify heretofore unseen playlists in clusters of similar playlists. 

In our implementation of k-means, we specified `k=114` clusters.

#### Cluster Prediction - k-NearestNeighbors
We used k-Nearest neighbors to predict a cluster for a never-before-seen user-specified playlist.
 
k-NearestNeighbors is an unsupervised neighbors-based machine learning method. Given an as of yet unseen data point, it finds the `k` training samples closest in distance to the unseen data point and uses this to predict a classification.

In our implementation for k-Centroid, we used `k=1` neighbors for our k-NearestNeighbor classifier. This is because for each cluster centroid in the data we used to fit the k-NN model, we only had one observation, as each cluster centroid is in itself a representation of an arbitrary number of playlists.

### Implementation

#### High Level Summary
Once we fitted the model, we had to create a separate method make_recommendations that would take in the Playlist ID and return a list of recommended tracks. Using the validation set, we fine-tuned number of neighbors as a parameter to identify the optimal number of neighbors that would return the highest score on the success metric.

Without going through the specific code, broadly, this is how it would work:

Use the k-NN model to find the k nearest neighbors to the given Playlist ID, based on the calibration songs that were passed into the matrix
For all the k nearest neighbor playlists found, create a frequency table of all the songs that appear in all the playlists
Select the top songs from the frequency table and return a list of recommended songs as output
When we run the ‘make_recommendations’ method, it produces the following output of tracks for a given playlist.

#### User Interface


### Model Performance
We have identified three metrics - RPS, NDCG and hit-rate - to evaluate all models we developed for this project. To obtain the final metrics for a given model, we compute the mean of the scores across all the playlists in the test set, and across different values for number of recommendations.

The histograms below show the distribution of scores across the three different metrics, with two distributions for RPS and NDCG, one each for the case where the number of recommendations equals the number of songs used for calibration and where it equals the number of withheld songs.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/k_centroid_performance.png" title="k-Centroid Model Performance"/>
</p>

Overall, the k-Centroid model achieved an R-Precision score of 0.219 and a Normalized Discounted Cumulative Gain (NDCG) score of 0.203 when producing the same number of recommendations as the number of songs used to calibrate the model. The R-precision score of 0.219 implies that if given a list of 100 songs, the model predicts 100 songs, out of which 22 on average would be songs that were in list of withheld songs not provided to the model initially.

### Discussion
TODO: Write about when the predictions are better than withheld.
