from unittest import TestCase
from decision_algorithm.decision_algorithm import Decision_Algorithm
from bed.sensor.util.sensor_data_utils import load_sensor_dataframe
from body.body import Patient
import os
from bluetoothconnection.bluetooth_connection_dummy import Bluetooth as Bluetooth

# if os.uname()[4][:3] == 'arm':
#     path = "/home/pi/Desktop/sensor_data"
#     from test_bluetoothconnection.bluetooth_connection import Bluetooth as Bluetooth
#
# else:
#     path = "/home/cjstanfi/Desktop/sensor_data"
#     from test_bluetoothconnection.bluetooth_connection_dummy import Bluetooth as Bluetooth

class TestBed(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_file = "test_files/sensor_data/sensor_data_dataframe237.csv"
        bluetooth = Bluetooth()
        cls.Decision_Algorithm = Decision_Algorithm(patient=Patient(bluetooth=bluetooth), bluetooth=bluetooth)
        data_df = load_sensor_dataframe(cls.test_file)
        sensor = cls.Decision_Algorithm.get_pressure_sensor()
        sensor.append_sensor_data(data_df)
        sensor.set_current_frame(data_df)
        # cls.test_bed.analyze_sensor_data()


    def test_analyze_sensor_data(self):
        self.Decision_Algorithm.analyze_sensor_data()
        self.fail()

    def test_calculate_deflatable_regions(self):
        self.fail()

    def test_calculate_inflatable_regions(self):
        self.fail()

    def test_print_stats(self):
        self.fail()

    def test_generate_bed_status_json(self):
        Decision_Algorithm = self.Decision_Algorithm
        Decision_Algorithm.generate_bed_status_json()
        return

    def test_bed_status_callback(self):
        self.Decision_Algorithm.get_bluetooth().register_bed_status_callback(self.Decision_Algorithm.send_bed_status_bluetooth)
        data = b'#'
        self.Decision_Algorithm.get_bluetooth().receive_data(data)
        self.Decision_Algorithm.send_bed_status_bluetooth()

