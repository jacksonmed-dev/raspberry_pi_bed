import csv

import numpy as np
import ast
from matplotlib import pyplot as plt
import pandas as pd
import imageio
from PIL import Image
import os
import glob
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


# use glob to get all the csv files
# in the folder
path = './test_files/'
csv_files = glob.glob(os.path.join(path, 'sensor_data_dataframe*.csv'))

# loop over the list of csv files
i = 0
for f in csv_files:
    # read the csv file
    df = pd.read_csv(f)
    data = np.asarray(extract_sensor_dataframe(df['readings']), dtype=np.float64).reshape(64, 27)

    imageio.imwrite("./test_files/test_image/" + str(i) + '.jpg', data)
    # Giving The Original image Directory
    # Specified
    Original_Image = Image.open("./test_files/test_image/" + str(i)  + '.jpg')

    # Rotate Image By 180 Degree
    rotated_image1 = Original_Image.rotate(180)
    imageio.imwrite("./test_files/test_image/" + str(i)  + '.jpg', rotated_image1)
    i += 1

#sensor_data = pd.DataFrame(data)