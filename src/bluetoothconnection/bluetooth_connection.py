from bluetooth import *
import socket
import subprocess
import time
import threading

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
        #self.client_sock.send(self.get_ip())
        try:
            while True:
                data = self.client_sock.recv(1024)
                if len(data) == 0: break
                print("received [%s]" % data)
                # print("get ip: " + get_ip())
        except IOError:
            pass

    def send_data(self, data):
        header = bytes("!", encoding='utf8')
        trailer = bytes("*", encoding="utf8")
        temp = bytes(data, encoding='utf8')
        message = header + temp + trailer
        length = int(len(message) / 1024)

        for i in range(length + 1):
            if i == range(len(message)):
                print("Sending: ")
                print(message[i * 1024:len(message)])
                print(len(message[i * 1024:len(message)]))
                self.client_sock.send(message[i * 1024:len(message)])
                time.sleep(0.2)
            else:
                print("Sending Final: ")
                print(message[i * 1024:(i + 1) * 1024])
                print(len(message[i * 1024:(i + 1) * 1024]))
                self.client_sock.send(message[i * 1024:(i + 1) * 1024])

    def send_dummy_data(self):
        time.sleep(4)
        i = 0
        while True:
            self.send_data("Sending Dummy Data {}".format(i))
            i = i + 1
            time.sleep(5)

    def run(self):
        serveron = True
        thread1 = threading.Thread(target=self.client_connect)
        # thread2 = threading.Thread(target=self.send_dummy_data)
        thread1.start()
        # thread2.start()