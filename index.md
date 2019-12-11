<div style="text-align: right"> <a href="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/master/Spotify_Playlist_Generation_Group_21_Models.ipynb">Download Notebook</a> </div>  
<div style="text-align: right"> <a href="https://drive.google.com/file/d/1vKTZ4S0wiGxiffjPxnth1rrBXIOTcLCQ/view?usp=sharing">Download Data</a> </div>  
## Project Overview 
Playlists are at the core of Spotify's business. Playlists are made up of collections of tracks that cater to different occasions, mood or listening styles. Tracks in the same playlist are meant to be similar, at least to a significant subset of listeners. Spotify itself actively curates Playlists that are followed by millions of Spotify listeners. Knowing which song to add to a Playlist forms the basis of recommender systems used by music companies such as Spotify. By applying available machine learning techniques to existing Spotify playlist and track data, our project goal is that of automatic playlist generation, where we create models for song discovery by starting with an initial playlist chosen by a user.

<br>

<p align="center">
<img src="https://image.roku.com/blog/wp-content/uploads/2018/10/Spotify-Landing-Page-900.jpg" height="400"/>
</p>

This project comes on the back of Spotify's [RecSys Challenge 2018](https://recsys-challenge.spotify.com/), which uses the Spotify Million Playlist dataset to help users to create and extend their own playlist. 

To predict new songs that could be added to a playlist, we first have to start with an initial playlist chosen by a user - in some cases, these playlists could contain user/context information that might be relevant in selecting similar playlists. Using the models we have developed, we then recommend additional songs for users by suggesting tracks based on their similarity to the existing tracks, either by feature similarity or in terms of co-occurence in a playlist.

Here, in this project, we take a sample of 16000+ playlists from this same Spotify Million Playlist dataset to form our training, test and validation sets, as we go forth and attempt to generate songs based on playlists given to our models. Our dataset is also supplemented with the Spotify Track API data, available from Spotify. 

## Methodology
For the purposes of this project, in our test set of playlists, we only feed 70% of all tracks in the playlist as **calibration** for the models, keeping 30% of tracks **withheld** as the ground truth, to test our predictions against. While this might mean that there could be the scenario that our model recommends songs that the playlist user would like but are not covered in the test set, we find that this methodology of measuring success is by far the most objective way of comparing the quality of our recommendations across the models we have developed.

We have created 3 models for our objective: Collaborative Filtering, k-means Clustering and Naive Bayes Classifier. Details are in each model's individual page.

## Measures of Success
We define a relevant track as a track with its track uri in both the predicted dataset and the playlist's withheld dataset.

We have identified the three metrics (RPS, NDCG and hit-rate) to evaluate our model. We calculated RPS and NDCG for two different number of recommendations produced by the model, `k` and `7/3` where `k` is the number of songs in a particular playlist withheld from the model. Our choice of using `7/3*k` is because this number represents the number of songs used to calibrate the model to the playlist, based on our 70:30 split of the test set. We also calculated hit-rate for 10 recommendations produced by the model to check how accurate our first 10 recommendations are.

To obtain the final metrics, we compute the mean of the scores across all the playlists in the test set, across different values for number of recommendations.

### Hit Rate
Hit rate is the number of predicted relevant tracks divided by the total number of predicted tracks. This metric differs from R-precision score in the sense that we are taking the number of predicted tracks as the denominator to give us a sense of how accurate our first 10 predictions are. This places a stricter burden on our model to ensure that playlist songs are among the top predicted songs.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/intro_hit_rate.png" title="High-Level Playlist Features" height="48"/>
</p>

### R-precision
R-precision is the number of predicted relevant tracks divided by the total number of withheld songs in the playlist.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/intro_r_precision.png" title="High-Level Playlist Features" height="48"/>
</p>

### Normalized discounted cumulative gain (NDCG)
Discounted cumulative gain measures the ranking quality of the recommended tracks, increasing when relevant tracks are placed higher in the list. Since we are not concerned about the order of the tracks in the withheld set we give any relevant track a value of 1.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/intro_dcg.png" title="High-Level Playlist Features" height="42"/>
</p>
