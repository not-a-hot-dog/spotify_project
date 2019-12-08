from sklearn.model_selection import train_test_split
import pandas as pd

playlist_list = pd.read_csv('./playlists.csv', usecols=['pid']).drop_duplicates()
train_pids, temp_pids = train_test_split(playlist_list, random_state=21, test_size=0.2)

val_pids, test_pids = train_test_split(temp_pids, random_state=21, test_size=0.5)

print('Train size: ', len(train_pids),
      '\nVal size: ', len(val_pids),
      '\nTest size: ', len(test_pids))

pd.DataFrame(train_pids).to_csv('./train_pids.csv', index=False)
pd.DataFrame(val_pids).to_csv('./val_pids.csv', index=False)
pd.DataFrame(test_pids).to_csv('./test_pids.csv', index=False)
