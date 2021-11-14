import pathlib

import bluetoothconnection.bluetooth_constants as bluetooth_constants
import pandas as pd
from bluetooth import *
import socket
import subprocess
import time
import threading
from os import listdir
from os.path import isfile, join

# Subprocess has to be run after bluetoothservice is up, therefore the sleep is there


class Bluetooth:
    cmd = 'hciconfig hci0 piscan'

    def __init__(self):

        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(("", PORT_ANY))
        self.server_sock.listen(1)

        self.port = self.server_sock.getsockname()[1]

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service(self.server_sock, "SampleServer",
                          service_id=uuid,
                          service_classes=[uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
                          #                   protocols = [ OBEX_UUID ]
                          )

        subprocess.check_output(self.cmd, shell=True)
        time.sleep(2)
        print("Waiting for connection on RFCOMM channel 1")
        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from ", self.client_info)
        self._gpio_callbacks = []
        self._bed_status_callbacks = []
        self._bed_status_automatic_callbacks = []
        self._bed_massage_callbacks = []
        # self.client_sock.send(self.get_ip())
        # print("IP address sent")

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def client_connect(self):
        # client_sock, client_info = self.server_sock.accept()
        print("Accepted connection from ", self.client_info)
        # self.client_sock.send(self.get_ip())
        try:
            while True:
                data = self.client_sock.recv(1024)
                if len(data) == 0: break
                self.switch_command(data)
                print("received [%s]" % data)

                # print("get ip: " + get_ip())

        except IOError:
            pass

# Add error checking when receiving the data
    def switch_command(self, data):
        temp = data.decode("utf-8")
        if len(temp) == 0: return
        if temp[0] == bluetooth_constants.INFLATABLE_REGION_HEADER:
            pin = int(temp[1])
            state = int(temp[2])
            self._notify_gpio_observers(pin, state)
            return
        if temp[0] == bluetooth_constants.MASSAGE_HEADER:
            value = int(temp[1])
            self._notify_bed_massage(value)
            #setup massage
            return
        if temp[0] == bluetooth_constants.BED_DATA_RESPONSE:
            self._notify_bed_status_observers() # send the bed json message back
            return
        if temp[0] == bluetooth_constants.BED_DATA_RESPONSE_AUTOMATIC:
            self._notify_bed_status_automatic_observers() # send the bed json message back
            return

    def _notify_bed_massage(self, value):
        for callback in self._bed_massage_callbacks:
            callback(value)

    def register_bed_massage_callback(self, callback):
        self._bed_massage_callbacks.append(callback)

    def _notify_bed_status_observers(self):
        for callback in self._bed_status_callbacks:
            callback()

    def register_bed_status_callback(self, callback):
        self._bed_status_callbacks.append(callback)

    def _notify_gpio_observers(self, new_value, state):
        # Send callback to set_relay function in gpio.py
        for callback in self._gpio_callbacks:
            callback(new_value, state)

    def register_gpio_callback(self, callback):
        self._gpio_callbacks.append(callback)

    def _notify_bed_status_automatic_observers(self, new_value, state):
        # Send callback to set_relay function in gpio.py
        for callback in self._gpio_callbacks:
            callback(new_value, state)

    def register_bed_status_automatic(self, callback):
        self._bed_status_automatic_callbacks.append(callback)

    def send_data(self, data, header_string):
        header = bytes(header_string, encoding='utf8')
        trailer = bytes(bluetooth_constants.TRAILER, encoding="utf8")
        temp = bytes(data, encoding='utf8')
        message = header + temp + trailer
        length = int(len(message) / 1024)

        for i in range(length + 1):
            if i * 1024 > len(message):
                print("Sending Final: ")
                print(message[i * 1024:len(message)])
                print(len(message[i * 1024:len(message)]))
                self.client_sock.send(message[i * 1024:len(message)])
                # time.sleep(0.2)
            else:
                print("Sending: ")
                print(message[i * 1024:(i + 1) * 1024])
                print(len(message[i * 1024:(i + 1) * 1024]))
                self.client_sock.send(message[i * 1024:(i + 1) * 1024])

    def send_dummy_data(self):
        current_path = str(pathlib.Path(__file__).parent.resolve())
        path_to_data = current_path + "/data/"
        only_files = [f for f in listdir(path_to_data) if isfile(join(path_to_data, f))]
        while True:
            for file in only_files:
                df = pd.read_csv(path_to_data + file)
                self.send_data(df["readings"][0], header_string=bluetooth_constants.BED_DATA_RESPONSE)
                time.sleep(3)

    def run(self, send_dummy_data):
        serveron = True
        thread1 = threading.Thread(target=self.client_connect)
        if send_dummy_data:
            thread2 = threading.Thread(target=self.send_dummy_data)
            thread1.start()
            thread2.start()
        else:
            thread1.start()
