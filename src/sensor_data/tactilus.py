import pandas as pd


# This class will be used when we have access to the api to get sensor data
class PressureSensor:
    # watchDirectory = OnMyWatch(path="/home/dev/Desktop/sensor_data")
    # gpio pin list used to control relays
    __sensor_data = pd.DataFrame()
    ## Temp variable to store the sensor data.
    __current_frame = pd.DataFrame()
    __path = "/home/dev/Desktop/sensor_data"

    def __init__(self):
        pass

    def load_current_frame(self):
        return

    def get_sensor_data(self):
        return self.__sensor_data

    def get_current_frame(self):
        return self.__current_frame

    def set_current_frame(self, df):
        self.__current_frame = df

    def set_sensor_data(self, df):
        self.__sensor_data = df
