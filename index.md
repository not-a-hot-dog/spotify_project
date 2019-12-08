<div style="text-align: right"> <a href="./notebook.ipynb">Download Notebook</a> </div>
<div style="text-align: right"> <a href="https://drive.google.com/file/d/1vKTZ4S0wiGxiffjPxnth1rrBXIOTcLCQ/view?usp=sharing">Download Data</a> </div>
## Introduction

### Purpose:
Starting with a initial playlist of songs chosen by a user, we recommend additional songs for the user by suggesting songs that appear in similar playlists.

### Measures of Success
We define a relevant track as a track uri that is in the predicted dataset and the playlist's withheld dataset.

#### Hit Rate
Hit rate is the number of predicted relevant tracks divided by the total number of predicted tracks.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/intro_hit_rate.png" title="High-Level Playlist Features" height="54"/>
</p>

#### R-precision
R-precision is the number of predicted relevant tracks divided by the total number of withheld songs in the playlist.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/intro_r_precision.png" title="High-Level Playlist Features" height="48"/>
</p>

#### Normalized discounted cumulative gain (NDCG)
Discounted cumulative gain measures the ranking quality of the recommended tracks, increasing when relevant tracks are placed higher in the list. Since we are not concerned about the order of the tracks in the withheld set we give any relevant track a value of 1.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/intro_dcg.png" title="High-Level Playlist Features" height="48"/>
</p>
