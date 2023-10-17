import pandas as pd
from pandasgui import show
import matplotlib.pyplot as plt
from utils import get_data, pre_process, plots


data = pd.read_csv('C:\\Users\\Pichau\\PycharmProjects\\worldgym\\data\\data_raw.csv', index_col=0)

pd.set_option('mode.chained_assignment', None)
print(data.columns)
show(data)
