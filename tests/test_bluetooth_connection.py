import random
import string
import time
from unittest import TestCase
from bluetoothconnection.bluetooth_connection_dummy import Bluetooth
import bluetoothconnection.bluetooth_constants as bluetooth_constants
from bed.sensor.dummy_gpio import Gpio

# import os
# import configparser
# dir_path = os.path.dirname(os.path.realpath(__file__))
# file = os.path.join(dir_path, '..\\config.ini')
# config = configparser.ConfigParser()
# config.read(file)
# config_blue = config['BLUETOOTHCONNECTION']


class TestBluetoothConnection(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file = "test_files/data.csv" #Added to config: config_blue['TEST_FILES']
        cls.bluetooth_connection = Bluetooth()
        cls.bluetooth_connection.run(send_dummy_data=False) #Added to config: config_blue.getboolean('SEND_DUMMY')
        cls.dummy_gpio = Gpio(inflatable_regions=20) #Added to config: int(config_blue['INFLATABLE_REGIONS']), 20)

    def test_bluetooth_decode(self):
        message = b'!Hello World*'
        self.bluetooth_connection.receive_data(message)

    def test_gpio_callback(self):
        self.bluetooth_connection.register_gpio_callback(self.dummy_gpio.set_relay)
        data = b'!11'
        self.bluetooth_connection.receive_data(data)

    def test_send_dummy_data(self):
        self.bluetooth_connection.send_dummy_data()

    def test_bluetooth_queue_1(self):
        try:
            message = "Hello World"
            self.bluetooth_connection.enqueue_bluetooth_data(message, bluetooth_constants.MASSAGE_START)#Added to config: config_blue['MESSAGE_START']
        except Exception as e:
            self.fail(e)


    def test_bluetooth_queue_2(self):
        try:
            for i in range(1, 100):
                message = "Hello World{}".format(i)
                self.bluetooth_connection.enqueue_bluetooth_data(message, bluetooth_constants.MASSAGE_START)#Added to config: config_blue['MESSAGE_START']
        except Exception as e:
            self.fail(e)

    def test_bluetooth_queue_3(self):
        try:
            for i in range(1, 100):
                message = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1500)) + str(i)
                self.bluetooth_connection.enqueue_bluetooth_data(message, bluetooth_constants.MASSAGE_START)#Added to config: config_blue['MESSAGE_START']
        except Exception as e:
            self.fail(e)
        time.sleep(5)
        return

