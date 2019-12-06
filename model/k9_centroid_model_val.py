import numpy as np

# Build df of playlists to classify in clusters

playlist_list = np.genfromtxt('./data/val_pids.csv', skip_header=1, dtype=int)[0:1]
# TODO: Keep in mind that for val/test pids you need to take in the pid, split it into train test songs,
#  and feed these train songs to the cluster predicting function




