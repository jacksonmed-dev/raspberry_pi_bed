import threading
import time

import pandas as pd
import numpy as np
import threading
from datetime import datetime, timedelta
from sseclient import SSEClient
import pathlib
import os
from os.path import isfile, join


from configuration import config,is_raspberry_pi
config_bed = config['BED']
config_paths = config['PATHS']


# This class will be used when we have access to the api to get sensor data
class PressureSensor(threading.Thread):
    # watchDirectory = OnMyWatch(path="/home/dev/Desktop/sensor")
    # gpio pin list used to control relays
    __current_frame = pd.DataFrame()
    __sensor_ip = config_bed['SENSOR_IP']
    __sensor_data = pd.DataFrame()
    __sensor_threshold = int(config_bed['SENSOR_THRESHOLD'])
    __sensor_body_composition = {
        "head": [i for i in range(0, 9)],
        "shoulder": [i for i in range(10, 16)],
        "arm": [i for i in range(17, 33)],
        "buttocks": [i for i in range(34, 43)],
        "leg": [i for i in range(44, 57)],
        "heels": [i for i in range(58, 64)]
    }
    __sensor_rows = int(config_bed['SENSOR_ROWS'])
    __sensor_columns = int(config_bed['SENSOR_COLUMNS'])
    __path = config_paths['BED']

    def __init__(self, inflatable_regions):
        temp = np.arange(int(self.__sensor_rows / inflatable_regions) + 1, self.__sensor_rows,
                         int(self.__sensor_rows / inflatable_regions) + 1)
        self.lock = threading.Lock()
        self.__sensor_inflatable_composition = np.split(np.arange(0, self.__sensor_rows), temp)
        self._callbacks = []
        self._bluetooth_callback = []

        # if os.uname()[4][:3] == 'arm':
        #     self.isRaspberryPi = True
        # else:
        #     self.isRaspberryPi = True
        # return

        self.isRaspberryPi = is_raspberry_pi

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
            callback(new_value, "!")

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

    def get_current_frame_array(self):
        temp = self.__current_frame
        temp = (temp['readings'][0])[1:-1].split(',')
        temp = np.array(temp).astype(np.uint8)
        return temp

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

    def set_sensor_body_composition(self, new_dict):
        temp = {"head": [], "shoulder": [], "arm": [], "buttocks": [], "leg": [], "heel": []}
        for key in temp:
            a = len(new_dict[key])

            if a == 1:
                min_y = new_dict[key][0][0][0]
                max_y = new_dict[key][0][2][0]
                temp_list = [i for i in range(min_y, max_y + 1)]  # model output is 0 indexed?
                temp[key] = temp_list

            # in the case of arm, leg, shoulder and heel we might have two objects so take lowest and highes toint of both
            elif a == 2:
                min_y = min(new_dict[key][0][0][0], new_dict[key][1][0][0])
                max_y = max(new_dict[key][0][2][0], new_dict[key][1][2][0])
                temp_list = [i for i in range(min_y, max_y + 1)]  # model output is 0 indexed?
                temp[key] = temp_list

            # if there is no signal in shoulder area keep the default coordinates
            elif a == 0:
                temp[key] = self.__sensor_body_composition[key]

        self.__sensor_body_composition = temp

    def append_sensor_data(self, df):
        self.__sensor_data = self.__sensor_data.append(df)

    def get_time(self):
        if self.__sensor_data is None:
            return None
        if len(self.__sensor_data) <= 1:
            return timedelta(0)
        else:
            try:
                date_format = config_bed['DATE_FORMAT']
                length = len(self.__sensor_data)
                sensordata = self.__sensor_data
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
        if self.isRaspberryPi:
            url = config_bed['URL']
            sse = SSEClient(url)
            for response in sse:
                df = pd.read_json(response.data)
                self.save_sensor_data(df)
                if "readings" in df.columns:
                    index = index + 1
                    readings_array = str(df["readings"][0])
                    self._notify_bluetooth_observers(readings_array)
                    self.current_frame(df)
                    # print(df)
    #
    # def start_sse_client_dummy(self):
    #     # Get the files from test/test_files/sensor_data
    #     # 406 total files
    #     current_path = str(pathlib.Path(__file__).parent.resolve())
    #     path_to_data = current_path + config_paths['TEST_DATA']
    #     only_files = [f for f in os.listdir(path_to_data) if isfile(join(path_to_data, f))]
    #     while True:
    #         for file in only_files:
    #         # Loop over each file and notify bluetooth observers
    #         # Set the current dataframe
    #         # Use current dataframe to run decision algorithm
    #         # time.sleep(3)
    #             df = pd.read_csv(path_to_data+file)
    #             readings_array = str(df["readings"][0])
    #             self._notify_bluetooth_observers(readings_array)
    #             self.current_frame(df)
    #             self.set_current_frame(df)
    #             time.sleep(3)

    def save_sensor_data(self, df: pd.DataFrame): #should I leave it all this way or try and add some stuff to configuration?
        directory = os.getcwd()
        temp = "{}/sensor_data".format(directory)
        files = os.listdir(r"{}/test_files/sensor_data".format(directory))
        index1 = files[(len(files)-1)][21:]
        index = int(files[(len(files)-1)][21:][:len(index1)-4])
        df.to_csv("{}/test_files/sensor_data_dataframe{}.csv".format(temp, index + 1))

    def run(self):
        if self.isRaspberryPi:
            thread = threading.Thread(target=self.start_sse_client())
            thread.start()
        else:
            thread = threading.Thread(target=self.start_sse_client_dummy())
            thread.start()

# print("data received {}".format(index))
# df.to_csv(
#     "/Users/colestanfield/PycharmProjects/raspberry_pi_bed/tests/test_files/test_image/sensor_data_dataframe{}.csv".format(
#         index))
