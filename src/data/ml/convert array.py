import csv
import pandas as pd
import numpy as np
import ast
from matplotlib import pyplot as plt

def extract_sensor_dataframe(df):
    data = df.iloc[0]
    try:
        if type(data) == str:
            data = ast.literal_eval(data)
        # df = pd.DataFrame(data)
        return data
    except Exception as e:
        print(e)
    else:
        return None
df = pd.read_csv('/home/justin/PycharmProjects/raspberry_pi_bed/tests/test_files/sensor_data_dataframe11.csv')
data = np.asarray(extract_sensor_dataframe(df['readings']),dtype=np.float64).reshape(64,27)
plt.pcolormesh( data , cmap = 'hot' )

plt.savefig("test7.png")

#sensor_data = pd.DataFrame(data)