## Conclusion

### Comparison of Models and Performance
<!-- How did individual modeling approches compare to each other and score? You can include the three sets of model metrics charts here side by side in a table -->

Each of our three approaches leads to similar distributions of the evaluation metrics. The following table summarises our results by presenting the means of our evaluation metrics, evaluated for all 3 approaches, in all five different scenarios.

| Evaluation  | Collaborative Filtering | K Means | Naive Bayes |
|-------------|-------------------------|---------|-------------|
| **Hit Rate (10 predictions)**    | 0.136                   | 0.195   | 0.191       |
| **R Precision (# of withheld tracks)** | 0.152                   | 0.133   | 0.145       |
| **R Precision (# of calibration tracks)** | 0.313                   | 0.219   | 0.116       |
| **NDCG (# of withheld tracks)**        | 0.152                   | 0.154   | 0.163       |
| **NDCG (# of calibration tracks)**        | 0.249                   | 0.203   | 0.234       |

This is a rather surprising result, especially since the techniques differ fundamentally in how they approach the problem. Further, it seems that the choice of model depends extensively on the evaluation metric chosen and the particular scenario it is applied in. For instance, `K Means` has the highest hit rate in the top 10 predictions, but with `NDCG`, Collaborative filtering does the best when number of predicted songs is larger than the withheld set size. When The number of predicted songs is equal to the number of withheld songs, naive Bayes has the best NDCG score.

It is clear that for collaborative filtering and K means, a larger number of predicted tracks improves the metric being measured (higher NDCG and R Precision). However, fo naive Bayes, this trend gets reversed in the case of R precision. A more principled analysis of the behaviour of each evaluation metric in relation to various instantiations of number of predicted tracks, number of withheld tracks, and number of callibration tracks is required to draw meaninful conclusions from this. The state space here is extremely large, and each experimental run takes a long time to complete, thus we leave this exercise for the future.

Based on the current results table, however, we can conjecture the following hypotheses to test:
1. There is an optimal number of tracks to predict where the hit-rate peaks.
2. R precision and NDCG always increases monotonically with increase in number of predicted tracks, in the case of collaborative filtering.
3. NDCG always increases monotonically with increase in number of predicted tracks, in the case of collaborative filtering, K means, and naive Bayes.
4. Limiting the runtime of the model prediciton generation step favours naive Bayes over the other techniques.


### Discussion
<!-- How did we do overall? Are the scores comparable to other models? Is there a chance that some of our predictions were better than what was in the original playlists? -->

### Specific Improvements for Future Iterations

#### Naive Bayes
Naive Bayes has the specific ability to incorporate prior information in the model. This was not utilised to the fullest extent in our current implementation. While we did incorporate some domain knowledge (such as considering every pair of songs to reflect a situation such that either song belongs to the callibration set), we did not account for various side-effects of this constraint. For instance, our model would predict with high probabilities **all** the songs that a playlist should contain, given a callibration set, it would not assign high probabilities only to the **withheld** songs. This directly impacts each of our evaluation metrics negatively, as we end up recommending songs already in the callibration set. It is trivial to correct this however, by setting the prior for each song from the callibration set to zero, so that they never get recommended. A future implementation of this appraoch should definitely incorporate this extra information.

#### Collaborative Filtering

#### K Means

<!-- Could we incorporate additional data, like Genre, into a future iteration -->
<!-- Would we want to adapt the code for scalability and performance -->
<!-- Could we extend these approaches to another task, e.g., predicting courses you may like based on your course reviews and others' course reviews, as well as you major and other courses in your Crimson Cart? -->
