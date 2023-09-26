import pandas as pd
import matplotlib.pyplot as plt
from utils import get_data, pre_process, plots


data = pd.read_csv('C:\\Users\\Pichau\\PycharmProjects\\worldgym\\data\\data_raw.csv', index_col=0)

pd.set_option('mode.chained_assignment', None)
# data.drop(columns=['registerCancelDate', 'minPeriodStayMembership], inplace=True, errors= 'ignore')
# data = data.iloc[:20]




# dataset.loc[:, 'lastAccessDate'] = pd.to_datetime(dataset['lastAccessDate'], errors='coerce')
# today = pd.Timestamp(datetime.now().date())
# valid_timestamp_mask = dataset['lastAccessDate'].apply(lambda x: isinstance(x, pd.Timestamp)) # Mask for rows where lastAccessDate is a valid timestamp
# dataset.loc[valid_timestamp_mask, 'date_since_last_access'] = (today - dataset.loc[valid_timestamp_mask, 'lastAccessDate'])
# dataset['date_since_last_access'] = pd.to_timedelta(dataset['date_since_last_access']).dt.days
# print(dataset['date_since_last_access'].describe())

(dataset['date_since_last_access'][dataset['date_since_last_access'] < 600].hist(bins=30))
plt.show()
