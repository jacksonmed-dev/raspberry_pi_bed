import unittest
from os.path import dirname, join, realpath, abspath
import sys

import configparser

dir_path = dirname(realpath(__file__))
file = join(dir_path, '..\\config.ini')
config = configparser.ConfigParser()
config.read(file)
bluetooth = config['BLUETOOTHCONNECTION']

full_path = join(dir_path, config['PATHS']['BLUE'])
sys.path.append(abspath(full_path))

import bluetooth_constants as bluetooth_constants

class TestConfig(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_paths(self):
        self.assertEqual(config.sections(), ['PATHS','BLUETOOTHCONNECTION'])
        self.assertEqual(config['PATHS']['ML'], '..\src\decision_algorithm\ml')

    def test_bluetooth(self):
        self.assertFalse(bluetooth.getboolean('SEND_DUMMY'))
        self.assertEqual(int(bluetooth['INFLATABLE_REGIONS']), 20)

        self.assertEqual(bluetooth_constants.INFLATABLE_REGION_HEADER, bluetooth['INFLATABLE_REGION_HEADER'])
        self.assertEqual(bluetooth_constants.PATIENT_STATUS_HEADER, bluetooth['PATIENT_STATUS_HEADER'])
        self.assertEqual(bluetooth_constants.BED_DATA_RESPONSE_AUTOMATIC, bluetooth['BED_DATA_RESPONSE_AUTOMATIC'])
        self.assertEqual(bluetooth_constants.BED_STATUS_RESPONSE, bluetooth['BED_STATUS_RESPONSE'])
        self.assertEqual(bluetooth_constants.TRAILER, bluetooth['TRAILER'])
        self.assertEqual(bluetooth_constants.BED_DATA_RESPONSE, bluetooth['BED_DATA_RESPONSE'])

        self.assertEqual(bluetooth_constants.MASSAGE_START, bluetooth['MASSAGE_START'])


if __name__ == '__main__':
    unittest.main()
