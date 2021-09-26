from bluetooth import *
import socket
import subprocess
import time

# Subprocess has to be run after bluetoothservice is up, therefore the sleep is there


class Bluetooth:
    cmd = 'hciconfig hci0 piscan'


    def __init__(self):

        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(("", PORT_ANY))
        self.server_sock.listen(1)

        port = self.server_sock.getsockname()[1]

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        advertise_service(self.server_sock, "SampleServer",
                          service_id=uuid,
                          service_classes=[uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
                          #                   protocols = [ OBEX_UUID ]
                          )

        subprocess.check_output(self.cmd, shell=True)
        time.sleep(2)
        print("Waiting for connection on RFCOMM channel %d" % self.port)
        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from ", self.client_info)
        self.client_sock.send(self.get_ip())


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
        while True:
            self.client_sock.send(bytes("Hello Back", "utf-8"))
            time.sleep(5)
        # try:
        #     while True:
        #         data = client_sock.recv(1024)
        #         if len(data) == 0: break
        #         print("received [%s]" % data)
        #         # print("get ip: " + get_ip())
        #         client_sock.send(bytes("Hello Back", "utf-8"))
        # except IOError:
        #     pass




    def run(self):
        serveron = True
        while (serveron == True):
            self.client_connect()
            print("disconnected")
            # client_sock.close()
            self.server_sock.close()
