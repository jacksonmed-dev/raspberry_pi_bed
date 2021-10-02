class Bluetooth:
    def send_data(self, data):
        temp = bytes(data, encoding='utf8')
        print("send_data function called")
        print("Data sent: ")
        length = int(len(temp)/1024)
        length2 = len(temp)/1024

        for i in range(length + 1):
            if i == range(len(temp)):
                print(temp[i * 1024:len(temp)])
                print(len(temp[i * 1024:len(temp)]))
            else:
                print(temp[i * 1024:(i+1)*1024])
                print(len(temp[i * 1024:(i+1)*1024]))

