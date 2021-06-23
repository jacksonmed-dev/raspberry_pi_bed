import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# This class will be used when we have access to the api to get sensor data
class PressureSensor:
    # watchDirectory = OnMyWatch(path="/home/dev/Desktop/sensor")
    # gpio pin list used to control relays
    __sensor_data = pd.DataFrame()
    __sensor_threshold = 0.65
    __sensor_body_composition = {
        "head": [i for i in range(0, 9)],
        "shoulders": [i for i in range(10, 16)],
        "back": [i for i in range(17, 33)],
        "butt": [i for i in range(34, 43)],
        "calves": [i for i in range(44, 57)],
        "feet": [i for i in range(58, 64)]
    }
    __sensor_rows = 65
    __sensor_columns = 27
    ## Temp variable to store the sensor data.
    __current_frame = pd.DataFrame()
    __path = "/home/dev/Desktop/sensor_data"

    def __init__(self, inflatable_regions):
        temp = np.arange(int(self.__sensor_rows/inflatable_regions) + 1, self.__sensor_rows, int(self.__sensor_rows/inflatable_regions)+1)
        self.__sensor_inflatable_composition = np.split(np.arange(0, self.__sensor_rows), temp)
        return

    def load_current_frame(self):
        return

    def get_sensor_data(self):
        return self.__sensor_data

    def get_current_frame(self):
        return self.__current_frame

    def get_sensor_threshold(self):
        return self.__sensor_threshold

    def get_sensor_body_composition(self):
        return self.__sensor_body_composition

    def get_sensor_inflatable_composition(self):
        return self.__sensor_inflatable_composition

    # This method needs a test. Handle error where data frame passed is larger than one
    def set_current_frame(self, df):
        self.__current_frame = df

    def set_sensor_data(self, df):
        self.__sensor_data = df

    def set_sensor_threshold(self, new_value):
        self.__sensor_threshold = new_value

    def set_sensor_inflatable_composition(self, values):
        self.__sensor_inflatable_composition = values

    def append_sensor_data(self, df):
        self.__sensor_data = self.__sensor_data.append(df)

    def get_time(self):
        if self.__sensor_data is None:
            return None
        if len(self.__sensor_data) <= 1:
            return timedelta(0)
        else:
            try:
                date_format = '%Y-%m-%d %H:%M:%S.%f'
                length = len(self.__sensor_data)
                time1 = self.__sensor_data.index.values[length - 1]
                time2 = self.__sensor_data.index.values[length - 2]
                time_diff = datetime.strptime(time1, date_format) - datetime.strptime(time2, date_format)
                return time_diff
            except ValueError as e:
                print("DateTime format error: {}".format(e))
            else:
                return None



