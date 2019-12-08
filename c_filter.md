## k-NN User-Based Collaborative Filtering model

### Overview

Given a given playlist of songs, assuming that users included songs that they deemed to be similar in the same playlist, we can predict songs in that playlist by finding a group of similar playlists to the input playlist and the songs that occur most frequently across these playlists.

Here, we can use a memory-based Collaborative Filtering model, which uses the k-NN algorithm to find $k$ number of playlists that are most similar to our given playlist. There are two types of Collaborative Filtering models - User-Based and Item-Based. In the context of Spotify playlists, these translate to Playlist-Based vs. Song-Based (based on song features).

As informed by our EDA, songs in the same playlist do not necessarily share the same features. Our baseline model employed a version of the Item-Based approach, which returned a low level of prediction accuracy. Hence, here, we will go with the User-Based (Playlist-Based) Collaborative Filtering approach in predicting songs.

The similarity metric between playlists can be calculated using cosine distance, based on the co-occurence of songs in training set playlists and the target playlist.

![](https://miro.medium.com/max/426/1*FjjcEChVVgb8fvUCVUL2mQ.png)

The Playlist-Based Collaborative Filtering approach is playfully illustrated in the following image: 

![](https://miro.medium.com/max/600/0*naixmLXwQl6lmdpt)

(Source: [Spotify's Recommendation Engine](https://medium.com/datadriveninvestor/behind-spotify-recommendation-engine-a9b5a27a935))

### Overview
