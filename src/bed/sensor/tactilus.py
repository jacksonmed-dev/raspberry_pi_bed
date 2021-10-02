import threading
import time

import pandas as pd
import numpy as np
import threading
from datetime import datetime, timedelta
from sseclient import SSEClient


# This class will be used when we have access to the api to get sensor data
class PressureSensor(threading.Thread):
    # watchDirectory = OnMyWatch(path="/home/dev/Desktop/sensor")
    # gpio pin list used to control relays
    __current_frame = pd.DataFrame()
    __sensor_ip = "192.168.86.51"
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
    __path = "/home/dev/Desktop/sensor_data"

    def __init__(self, inflatable_regions):
        temp = np.arange(int(self.__sensor_rows / inflatable_regions) + 1, self.__sensor_rows,
                         int(self.__sensor_rows / inflatable_regions) + 1)
        self.lock = threading.Lock()
        self.__sensor_inflatable_composition = np.split(np.arange(0, self.__sensor_rows), temp)
        self._callbacks = []
        self._bluetooth_callback = []
        return

    def current_frame(self):
        return self.__current_frame

    def current_frame(self, new_value):
        self.lock.acquire()
        try:
            self.__current_frame = new_value
        finally:
            self.lock.release()
            self._notify_observers()

    def _notify_observers(self):
        for callback in self._callbacks:
            callback()

    def _notify_bluetooth_observers(self, new_value):
        for callback in self._bluetooth_callback:
            callback(new_value)

    def register_callback(self, callback):
        self._callbacks.append(callback)

    def register_bluetooth_callback(self, callback):
        self._bluetooth_callback.append(callback)

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

    def get_sensor_ip_address(self):
        return self.__sensor_ip

    def start_sse_client(self):
        url = "http://10.0.0.1/api/sse"
        sse = SSEClient(url)
        for response in sse:
            df = pd.read_json(response.data)
            if "readings" in df.columns:
                self._notify_bluetooth_observers(response.data)
                self.current_frame(df)
                print(df)


    def run(self):
        self.start_sse_client()