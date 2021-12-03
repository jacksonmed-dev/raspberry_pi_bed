import random
import string
import time
from unittest import TestCase
from bluetoothconnection.bluetooth_connection_dummy import Bluetooth
import bluetoothconnection.bluetooth_constants as bluetooth_constants
from bed.sensor.dummy_gpio import Gpio



class TestBluetoothConnection(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file = "test_files/data.csv"
        cls.bluetooth_connection = Bluetooth()
        cls.bluetooth_connection.run(send_dummy_data=False)
        cls.dummy_gpio = Gpio(inflatable_regions=20)

    def test_bluetooth_decode(self):
        message = b'!Hello World*'
        self.bluetooth_connection.client_connect(message)

    def test_gpio_callback(self):
        self.bluetooth_connection.register_gpio_callback(self.dummy_gpio.set_relay)
        data = b'!11'
        self.bluetooth_connection.client_connect(data)

    def test_send_dummy_data(self):
        self.bluetooth_connection.send_dummy_data()

    def test_bluetooth_queue_1(self):
        try:
            message = "Hello World"
            self.bluetooth_connection.enqueue_bluetooth_data(message, bluetooth_constants.MASSAGE_START)
        except Exception as e:
            self.fail(e)


    def test_bluetooth_queue_2(self):
        try:
            for i in range(1, 100):
                message = "Hello World{}".format(i)
                self.bluetooth_connection.enqueue_bluetooth_data(message, bluetooth_constants.MASSAGE_START)
        except Exception as e:
            self.fail(e)

    def test_bluetooth_queue_3(self):
        try:
            for i in range(1, 100):
                message = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1500)) + str(i)
                self.bluetooth_connection.enqueue_bluetooth_data(message, bluetooth_constants.MASSAGE_START)
        except Exception as e:
            self.fail(e)
        time.sleep(5)
        return

