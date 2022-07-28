import os
import sys
import unittest

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(dir_path, '../src/')

full_path = os.path.join(dir_path, path)
sys.path.append(os.path.abspath(full_path))

from bluetoothconnection.bluetooth_connection_dummy import Bluetooth
import decision_algorithm.decision_algorithm as da

from bed.bed import Bed
from body.body import Patient


# if os.uname()[4][:3] == 'arm':
#     path = "/home/pi/Desktop/sensor_data"
#     from test_bluetoothconnection.bluetooth_connection import Bluetooth as Bluetooth
#
# else:
#     path = "/home/cjstanfi/Desktop/sensor_data"
#     from test_bluetoothconnection.bluetooth_connection_dummy import Bluetooth as Bluetooth

class TestDecision(unittest.TestCase):


    def setUp(self):
        self.bluetooth = Bluetooth()
        self.Bed = Bed(patient=Patient(bluetooth=self.bluetooth), bluetooth=self.bluetooth)
        self.old_sensor_coord = {'head': [0, 1, 2, 3, 4, 5, 6, 7, 8], 'shoulder': [10, 11, 12, 13, 14, 15],
                            'arm': [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
                            'buttocks': [34, 35, 36, 37, 38, 39, 40, 41, 42],
                            'leg': [44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56],
                            'heels': [58, 59, 60, 61, 62, 63]}
        self.old_tube_coord = {'head': [0], 'arm': [2, 3], 'shoulder': [1], 'buttocks': [4], 'leg': [5, 6], 'heel': [7]}
        self.new_sensor_coord = {'head': [13, 14], 'shoulder': [20, 21, 22, 23, 24, 25], 'arm': [21, 22, 23, 24, 25, 26, 27],
                            'buttocks': [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44],
                            'leg': [56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],
                            'heel': [69, 70, 71]}
        self.new_tube_coord = {'head': [1], 'shoulder': [2, 3], 'arm': [2, 3], 'buttocks': [3, 4, 5], 'leg': [6, 7, 8],
                          'heel': [8]}

        self.sensor = self.Bed.get_pressure_sensor()

        self.curpath = os.path.join(os.getcwd(), '..\\src\\')
        # self.BODY_MODEL_DIR = os.path.join(self.curpath, "decision_algorithm\\ml\\training\\model_file\\mask_rcnn_body parts_0050.h5")
        self.TEST_FILE_DIR = os.path.join(os.getcwd(), "test_files/sensor_data/sensor_data_dataframe86.csv")
        self.LSTM_MODEL_DIR = os.path.join(self.curpath, "decision_algorithm/ml/training/model_file/LSTM_model.h5")
        self.TEST_CSV_DIR = os.path.join(self.curpath, "decision_algorithm/ml/test_result/lstm_result.csv")
        self.BODY_MODEL_DIR = "C:\\Users\\mojca\\Desktop\\EPICS\\JacksonMedical\\Github\src\\decision_algorithm\ml\\training\\model_file\\mask_rcnn_body parts_0025.h5"
        pass

    def tearDown(self):
        pass

    def test_body_part_location_update(self):
        self.assertEqual(self.sensor.get_sensor_body_composition(),self.old_sensor_coord)
        self.assertEqual(self.Bed.get_tube_body_composition(),self.old_tube_coord)
        da.body_part_location_update(self.Bed, self.TEST_FILE_DIR, self.BODY_MODEL_DIR)
        self.assertEqual(self.sensor.get_sensor_body_composition(), self.new_sensor_coord)
        self.assertEqual(self.Bed.get_tube_body_composition(), self.new_tube_coord)

    def test_part1_adjustment(self):
        self.assertEqual(da.part1_adjustment(self.Bed,self.TEST_FILE_DIR,self.BODY_MODEL_DIR), True)

    def test_algorithm_part2(self):
        self.assertEqual(da.body_part_location_update(self.Bed,self.TEST_FILE_DIR,self.BODY_MODEL_DIR),{'head': [], 'shoulder': [[[7, 14], [7, 20], [14, 14], [14, 20]], [[8, 7], [8, 13], [14, 7], [14, 13]]], 'buttocks': [[[23, 7], [23, 17], [31, 7], [31, 17]]], 'leg': [[[34, 11], [34, 19], [55, 11], [55, 19]], [[46, 3], [46, 6], [63, 3], [63, 6]]], 'arm': [[[7, 21], [7, 22], [20, 21], [20, 22]]], 'heel': []})
        self.assertEqual(da.algorithm_part2(self.Bed, self.LSTM_MODEL_DIR, self.TEST_CSV_DIR), True)

    def test_part3_adjustment(self):
        # da.part3_adjustment(self.Bed)
        # self.assertEqual(self.Bed.get_massage(),True)
        self.assertEqual(da.part3_adjustment(self.Bed),True)

    def test_main_algorithm(self):
        self.assertEqual(da.main_algorithm(),True)
if __name__ == '__main__':
    unittest.main()