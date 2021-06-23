import pandas as pd
from bed.sensor.tactilus import PressureSensor
from body.body import Patient
from bed.sensor.util.sensor_data_utils import extract_sensor_dataframe
from datetime import timedelta
import os
if os.uname()[4][:3] == 'arm':
    from bed.sensor.gpio import Gpio
else:
    from bed.sensor.dummy_gpio import Gpio


# A bed contains the following:
#   Patient
#   Sensor
#   Relays to control the valves
class Bed:
    # Same value for inflatable_regions and relay count. There may be a situation where there are more relays than
    # inflatable regions. For now, the variable serves no purpose
    __inflatable_regions = 20
    __relay_count = 20
    __bed_gpio = Gpio(inflatable_regions=__inflatable_regions)
    __pressure_sensor = PressureSensor(__inflatable_regions)
    __body_stats_df = pd.DataFrame(0, index=['head', 'shoulders', 'back', 'butt', 'calves', 'feet'],
                                   columns=['time', 'max_pressure'])

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

        # Demo method!!
        for body_part, value in sensor_composition.items():
            pressure = self.__body_stats_df.at[body_part, 'max_pressure']
            if pressure > self.__pressure_sensor.get_sensor_threshold():
                self.calculate_deflatable_regions(body_part)
            else:
                self.calculate_inflatable_regions(body_part)

        self.__bed_gpio.change_relay_state()
        return

    # Should be pre computed. Change this!!! Save in dictionary. Should only called if the body region state needs to
    # change
    def calculate_deflatable_regions(self, body_part):
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
                    self.__bed_gpio.set_relay(pin=index, state=0)
        return

    def calculate_inflatable_regions(self, body_part):
        sensor_region_body = self.__pressure_sensor.get_sensor_body_composition()[body_part]
        sensor_data_df = extract_sensor_dataframe(self.__pressure_sensor.get_current_frame()).loc[sensor_region_body]

        sensor_data_row_max = sensor_data_df.max(axis=1)

        for index, array in enumerate(self.__pressure_sensor.get_sensor_inflatable_composition()):
            if any(x in sensor_data_row_max for x in array):
                self.__bed_gpio.set_relay(pin=index, state=1)
        return


    def print_stats(self):
        print("Directory Modified")
        print("Body Stats:\n{}\n".format(self.__body_stats_df))
        print("Relays:\t{}\n\n".format(self.__bed_gpio.get_gpio_pins()))

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
