import json
import threading
from datetime import timedelta

import pandas as pd


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

    def __init__(self):
        self.__body_stats_df['time'] = timedelta(0)
        self.lock = threading.Lock()
        pass

    def set_body_stats_df(self, new_df):
        self.lock.acquire()
        try:
            self.__body_stats_df = new_df
            print("Lock acquired")
        finally:
            self.lock.release()
            print("Lock released")

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
