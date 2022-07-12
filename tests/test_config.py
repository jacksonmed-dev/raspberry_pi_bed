import unittest
from os.path import dirname, join, realpath, abspath
import sys
import ast

import configparser

dir_path = dirname(realpath(__file__))
file1 = join(dir_path, '..\\config.ini')
file2 = join(dir_path, '..\\config_for_tests.ini')
config = configparser.ConfigParser()
config.read(file1)
bluetooth = config['BLUETOOTHCONNECTION']
massage = config['MASSAGE']
model = config['MODEL']
config_tests = configparser.ConfigParser()
config_tests.read(file2)
tests_blue = config_tests['BLUETOOTHCONNECTION']


full_path = join(dir_path, config['PATHS']['BLUE'])
sys.path.append(abspath(full_path))

import bluetooth_constants as bluetooth_constants

class TestConfig(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_paths(self):
        self.assertEqual(config.sections(), ['PATHS','BED','BLUETOOTHCONNECTION','MODEL', 'MASSAGE','SERVER'])
        self.assertEqual(config['PATHS']['ML'], '..\src\decision_algorithm\ml')

    def test_bluetooth(self):
        self.assertEqual(bluetooth_constants.INFLATABLE_REGION_HEADER, bluetooth['INFLATABLE_REGION_HEADER'])
        self.assertEqual(bluetooth_constants.PATIENT_STATUS_HEADER, bluetooth['PATIENT_STATUS_HEADER'])
        self.assertEqual(bluetooth_constants.BED_DATA_RESPONSE_AUTOMATIC, bluetooth['BED_DATA_RESPONSE_AUTOMATIC'])
        self.assertEqual(bluetooth_constants.BED_STATUS_RESPONSE, bluetooth['BED_STATUS_RESPONSE'])
        self.assertEqual(bluetooth_constants.TRAILER, bluetooth['TRAILER'])
        self.assertEqual(bluetooth_constants.BED_DATA_RESPONSE, bluetooth['BED_DATA_RESPONSE'])

        self.assertEqual(bluetooth_constants.MASSAGE_START, bluetooth['MASSAGE_START'])

    def test_massage(self):
        self.assertTrue(massage.getboolean('STATUS'))
        self.assertEqual(int(massage['TYPE']), 1)

    def test_model(self):
        self.assertEqual(['BG','head','shoulder','buttocks','leg','arm','heel'], ast.literal_eval(model['CLASS_NAMES']))

    def test_config_for_tests(self):
        self.assertFalse(tests_blue.getboolean('SEND_DUMMY'))
        self.assertEqual(int(tests_blue['INFLATABLE_REGIONS']), 20)


if __name__ == '__main__':
    unittest.main()
