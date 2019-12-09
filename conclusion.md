## Conclusion

### Comparison of Models and Performance
<!-- How did individual modeling approches compare to each other and score? You can include the three sets of model metrics charts here side by side in a table -->

Each of our three approaches leads to similar distributions of the evaluation metrics. The following table summarizes our results by presenting the means of our evaluation metrics, evaluated for all 3 approaches, in all five different scenarios.

| Evaluation  | Collaborative Filtering | K Means | Naive Bayes |
|-------------|-------------------------|---------|-------------|
| **Hit Rate (10 predictions)**    | 0.136                   | 0.195   | 0.191       |
| **R Precision (# of withheld tracks)** | 0.152                   | 0.133   | 0.145       |
| **R Precision (# of calibration tracks)** | 0.313                   | 0.219   | 0.116       |
| **NDCG (# of withheld tracks)**        | 0.152                   | 0.154   | 0.163       |
| **NDCG (# of calibration tracks)**        | 0.249                   | 0.203   | 0.234       |

This is a rather surprising result, especially since the techniques differ fundamentally in how they approach the problem. Further, it seems that the choice of model depends extensively on the evaluation metric chosen and the particular scenario it is applied in. For instance, `K Means` has the highest hit rate in the top 10 predictions, but with `NDCG`, Collaborative filtering does the best when number of predicted songs is larger than the withheld set size. When The number of predicted songs is equal to the number of withheld songs, naive Bayes has the best NDCG score.

It is clear that for collaborative filtering and K means, a larger number of predicted tracks improves the metric being measured (higher NDCG and R Precision). However, for naive Bayes, this trend gets reversed in the case of R precision. A more principled analysis of the behaviour of each evaluation metric in relation to various instantiations of number of predicted tracks, number of withheld tracks, and number of callibration tracks is required to draw meaninful conclusions from this. The state space here is extremely large, and each experimental run takes a long time to complete, thus we leave this exercise for the future.

Based on the current results table, however, we can conjecture the following hypotheses to test:
1. There is an optimal number of tracks to predict where the hit-rate peaks.
2. R precision and NDCG always increases monotonically with increase in number of predicted tracks, in the case of collaborative filtering.
3. NDCG always increases monotonically with increase in number of predicted tracks, in the case of collaborative filtering, K means, and naive Bayes.
4. Limiting the runtime of the model prediciton generation step favours naive Bayes over the other techniques.

### Specific Improvements for Future Iterations

#### Naive Bayes
Naive Bayes has the specific ability to incorporate prior information in the model. This was not utilised to the fullest extent in our current implementation. While we did incorporate some domain knowledge (such as considering every pair of songs to reflect a situation such that either song belongs to the callibration set), we did not account for various side-effects of this constraint. For instance, our model would predict with high probabilities **all** the songs that a playlist should contain, given a callibration set, it would not assign high probabilities only to the **withheld** songs. This directly impacts each of our evaluation metrics negatively, as we end up recommending songs already in the callibration set. It is trivial to correct this however, by setting the prior for each song from the callibration set to zero, so that they never get recommended. A future implementation of this appraoch should definitely incorporate this extra information.

#### Collaborative Filtering
In the k-NN Collaborative Filtering model, we only consider track co-occurence between playlists and assign a 1 or 0 based on its occurence in the playlist. Going forward, if we are able to obtain ratings on how well a song fits a playlist, possibly based on user ratings, the model could more closely resemble the User-Based Collaborative Filtering models used for more sophisticated recommender systems used by the likes of Netflix. This would definitely improve our ability to predict songs that are likely to be in a playlist.

#### K Means
k-Means Clustering has the ability to find patterns unsupervised and in high dimensional input data. One area where we did not use this to the fullest was by not including Genre information. This was  due to the limitations of the Genre data in the Spotify API. While the Spotify API associates genres with specific artists, it does not contain the actual Genre of an individual track. Furthermore, the Genres associated with artists are highly specific, and there is no existing grouping of similar Genres (e.g., 'dfw rap', 'melodic rap', 'pop', and 'rap' are all associated with Post Malone, while 'atl hip hop', 'atl trap', 'gangster rap', 'melodic rap' are associated with Young Thug). Making use of this data will require additional pre-processing in the future. 

### Discussion
We return to our performance on the `hit-rate` measure as an indicator of how well our model performs in the context of how real humans would interact with it. On average, our k-Means and Naive Bayes models were able to correctly predict 2 "withheld" songs out of our top 10 predictions for a given calibration playlist. Anecdotally, this is on par with our team members' experiences with the recommendation engine built in to the Spotify application: for every 10 songs recommended, about 2 actually fit the mood of the current playlist. That said, because our models were not tested by humans, we weren't able to consider a key performance indicator: whether the recommended tracks are a better fit for the calibration playlist than the songs which were withheld at random for scoring purposes.

<p align="center">
<img src="https://raw.githubusercontent.com/not-a-hot-dog/spotify_project/gh-pages/_images/spotify_recommendations.png" title="Spotify's Actual Recommendation Engine"/>
</p>

Outside of the Spotify playlist recommendation use case, we wonder if we may extend these same approaches to another task that benefits are community. Could we, for example, predict courses a student may like based on their course reviews and others' course reviews, as well as the student's concentration and other courses in their Crimson Cart? Or could these methods be applied to identify post-operative patients who may be at risk for opiod addiction, and flag them to their medical care team for a proactive, opt-in intervention? These are highly adaptable, powerful methods, with the ability to make significant impacts in decisions that enhance human experiences, big and small.
