import json
import threading
from datetime import timedelta
import pandas as pd
import os
import bluetoothconnection.bluetooth_constants as bluetooth_constants


if os.uname()[4][:3] == 'arm' and not "MacBook" in os.uname().nodename:
    from bed.sensor.gpio import Gpio
    from bluetoothconnection.bluetooth_connection import Bluetooth
else:
    from bed.sensor.dummy_gpio import Gpio
    from bluetoothconnection.bluetooth_connection_dummy import Bluetooth

class Patient(object):
    __body_stats_df = pd.DataFrame(0, index=['head', 'shoulders', 'back', 'butt', 'calves', 'feet'],
                                   columns=['time', 'max_pressure'])
    __body = {
        "first_name": " Ben",
        "last_name": "Dover",
        "age": 36,
        "height": 72,
        "weight": 190
    }

    __patient_history = {

    }

    __patient_nutrition = {

    }

    def __init__(self, bluetooth: Bluetooth):
        self.__bluetooth = bluetooth
        self.__body_stats_df['time'] = timedelta(0)
        self.lock = threading.Lock()
        self.__bluetooth.register_patient_status_observers(self.send_patient_status)
        pass

    def set_body_stats_df(self, new_df):
        self.lock.acquire()
        try:
            self.__body_stats_df = new_df
        finally:
            self.lock.release()

    def get_body(self):
        return self.__body

    def get_body_stats_df(self):
        return self.__body_stats_df

    def get_body_stats_df_json(self):
        temp = self.__body_stats_df.to_json()
        return temp

    def get_patient_info_json(self):
        temp = json.dumps(self.__body)
        return temp

    def send_patient_status(self):
        data = self.get_patient_info_json()
        self.__bluetooth.enqueue_bluetooth_data(data, bluetooth_constants.PATIENT_STATUS_HEADER)
        return

