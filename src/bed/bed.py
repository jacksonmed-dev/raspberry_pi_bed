import pandas as pd

from src.sensor_data.tactilus import PressureSensor
from src.body.body import Patient
from src.sensor_data.util.sensor_data_utils import extract_sensor_dataframe
from datetime import timedelta


class Bed:
    # A bed contains the following:
    #   Patient
    #   Sensor
    #   Relays to control the valves
    __inflatable_regions = 10
    __pressure_sensor = PressureSensor(__inflatable_regions)
    __relay_count = 1
    __body_stats_df = pd.DataFrame(0, index=['head', 'shoulders', 'back', 'butt', 'calves', 'feet'],
                                   columns=['time', 'max_pressure', 'inflatable_region'])

    def __init__(self, patient: Patient):
        self.__patient = patient
        self.__body_stats_df['time'] = timedelta(0)
        return

    # Main algorithm to make decision. Only looks at time spent under "high pressure"
    def analyze_sensor_data(self):
        #### Work on this ###
        ### function should generate a dataframe with pressure regions ###
        time_diff = self.__pressure_sensor.get_time()
        sensor_data = extract_sensor_dataframe(self.__pressure_sensor.get_current_frame())
        sensor_composition = self.__pressure_sensor.get_sensor_body_composition()

        # Identify regions of the body that are in a high pressure state
        for body_part, value in sensor_composition.items():
            data = sensor_data.loc[value]
            max_value = data.max().max()
            self.__body_stats_df.at[body_part, 'max_pressure'] = max_value

            if max_value > self.__pressure_sensor.get_sensor_threshold():
                current_time = self.__body_stats_df.at[body_part, 'time']
                new_time = current_time + time_diff
                self.__body_stats_df.at[body_part, 'time'] = new_time
            else:
                self.__body_stats_df.at[body_part, 'time'] = timedelta(0)

        # identify regions to inflate/deflate
        for body_part, value in sensor_composition.items():
            time = self.__body_stats_df.at[body_part, 'time']
            if time == timedelta(0):
                self.calculate_deflatable_regions(body_part)
            elif time > timedelta(minutes=5):
                self.calculate_inflatable_regions(body_part)
        return

    # Should be pre computed. Change this!!! Save in dictionary. Should only called if the body region state needs to
    # change
    def calculate_inflatable_regions(self, body_part):
        sensor_region_body = self.__pressure_sensor.get_sensor_body_composition()[body_part]
        sensor_data_df = extract_sensor_dataframe(self.__pressure_sensor.get_current_frame()).loc[sensor_region_body]

        sensor_data_row_max = sensor_data_df.max(axis=1)
        sensor_data_row_max_indices = sensor_data_row_max.index.tolist()

        sensor_threshold = self.__pressure_sensor.get_sensor_threshold()
        for index, array in enumerate(self.__pressure_sensor.get_sensor_inflatable_composition()):
            if any(x in sensor_data_row_max for x in array):
                # temp2 = [x for x in sensor_data_max_index if x in array]
                max_sensor_value = sensor_data_row_max[[x in array for x in sensor_data_row_max_indices]].max()
                if max_sensor_value > sensor_threshold:
                    self.enable_relays([index])
            return

    def calculate_deflatable_regions(self, body_part):
        sensor_region_body = self.__pressure_sensor.get_sensor_body_composition()[body_part]
        sensor_data_df = extract_sensor_dataframe(self.__pressure_sensor.get_current_frame()).loc[sensor_region_body]

        sensor_data_row_max = sensor_data_df.max(axis=1)

        for index, array in enumerate(self.__pressure_sensor.get_sensor_inflatable_composition()):
            if any(x in sensor_data_row_max for x in array):
                self.disable_relays([index])
            return

    def enable_relays(self, pins):
        # enable all pins
        for pin in pins:
            print("Relay %d Enabled" % pin)

    def disable_relays(self, pins):
        for pin in pins:
            print("Relay %d Disabled" % pin)

    # Getters/Setters
    def get_pressure_sensor(self):
        return self.__pressure_sensor

    def get_relay_count(self):
        return self.__relay_count

    def get_patient(self):
        return self.__patient

    def get_inflatable_regions(self):
        return self.__inflatable_regions

    def set_pressure_sensor(self, pressure_sensor: PressureSensor):
        self.__pressure_sensor = pressure_sensor

    def set_relay_count(self, relay_count):
        self.__relay_count = relay_count

    def set_patient(self, patient: Patient):
        self.__patient = patient

    def set_inflatable_regions(self, count):
        self.__inflatable_regions = count
