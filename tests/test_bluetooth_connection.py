from unittest import TestCase
from bluetoothconnection.bluetooth_connection_dummy import Bluetooth
from bed.sensor.dummy_gpio import Gpio



class TestBluetoothConnection(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file = "test_files/data.csv"
        cls.bluetooth_connection = Bluetooth()
        cls.dummy_gpio = Gpio(inflatable_regions=20)

    def test_bluetooth_decode(self):
        message = b'!Hello World*'
        self.bluetooth_connection.client_connect(message)

    def test_gpio_callback(self):
        self.bluetooth_connection.register_gpio_callback(self.dummy_gpio.set_relay)
        data = b'!11'
        self.bluetooth_connection.client_connect(data)

