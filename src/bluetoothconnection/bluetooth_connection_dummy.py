class Bluetooth:

    def __init__(self):

        # self.server_sock = BluetoothSocket(RFCOMM)
        # self.server_sock.bind(("", PORT_ANY))
        # self.server_sock.listen(1)
        #
        # self.port = self.server_sock.getsockname()[1]
        #
        # uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        #
        # advertise_service(self.server_sock, "SampleServer",
        #                   service_id=uuid,
        #                   service_classes=[uuid, SERIAL_PORT_CLASS],
        #                   profiles=[SERIAL_PORT_PROFILE],
        #                   #                   protocols = [ OBEX_UUID ]
        #                   )
        #
        # subprocess.check_output(self.cmd, shell=True)
        # time.sleep(2)
        # print("Waiting for connection on RFCOMM channel 1")
        # self.client_sock, self.client_info = self.server_sock.accept()
        # print("Accepted connection from ", self.client_info)
        self._gpio_callbacks = []
        # self.client_sock.send(self.get_ip())
        # print("IP address sent")

    def send_data(self, data):
        temp = bytes(data, encoding='utf8')
        print("send_data function called")
        print("Data sent: ")
        length = int(len(temp) / 1024)
        length2 = len(temp) / 1024

        for i in range(length + 1):
            if i == range(len(temp)):
                print(temp[i * 1024:len(temp)])
                print(len(temp[i * 1024:len(temp)]))
            else:
                print(temp[i * 1024:(i + 1) * 1024])
                print(len(temp[i * 1024:(i + 1) * 1024]))

    def client_connect(self, data):
        print("Accepted connection from ", "Python Test")
        try:
            if len(data) == 0: return
            self.switch_command(data)
            print("received [%s]" % data)
        except IOError:
            pass

    def switch_command(self, data):
        temp = data.decode("utf-8")
        if len(temp) == 0: return
        if temp[0] == '!':
            pin = int(temp[1])
            state = int(temp[2])
            self._notify_gpio_observers(pin, state)

    def _notify_gpio_observers(self, new_value, state):
        # Send callback to set_relay function in gpio.py
        for callback in self._gpio_callbacks:
            callback(new_value, state)

    def register_gpio_callback(self, callback):
        self._gpio_callbacks.append(callback)

