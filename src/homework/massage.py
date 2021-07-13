import random
import threading
import time


class Massage(threading.Thread):
    # Same value for inflatable_regions and relay count. There may be a situation where there are more relays than
    # inflatable regions. For now, the variable serves no purpose

    # __pressure_sensor = PressureSensor(__inflatable_regions)
    # __body_stats_df = pd.DataFrame(0, index=['head', 'shoulders', 'back', 'butt', 'calves', 'feet'],
    #                                columns=['time', 'max_pressure'])
    __composition = {
        "head": [i for i in range(0, 3)],
        "shoulders": [i for i in range(4, 5)],
        "back": [i for i in range(6, 10)],
        "butt": [i for i in range(11, 13)],
        "calves": [i for i in range(14, 17)],
        "feet": [i for i in range(18, 20)]
    }

    __massage = True

    def __init__(self, gpio):
        super(Massage, self).__init__()
        self.lock = threading.Lock()
        self.__gpio = gpio
        return

    # def run_massage_thread(self):
    #     threading.Thread(self.start())

    def set_message(self, value: bool):
        self.lock.acquire()
        self.__massage = value
        self.lock.release()


    def run(self):
        print("Starting Message \n\n\n")
        # self.inflate_all()
        print("Check complete... Massage Starting")
        while self.__massage:
            self.basic_wave()
            time.sleep(2)
        # while self.__massage:
        #     self.message_wave_two()
        #     time.sleep(10)
        #     self.message_feet()
        #     time.sleep(10)
        #     self.message_head()
        #     time.sleep(10)
        #     self.message_wave_two()
        #     time.sleep(10)
        #     self.message_head()
        #     time.sleep(10)
        #     self.message_feet()
        #     time.sleep(10)
        # print("Massage Stopped")
        return

    def basic_wave(self):
        print("Message Wave Two")
        offset = 3
        max_val = self.__gpio.get_num_gpio_pins() - 1
        for i in range(max_val + offset + 1):
            if (i - offset) >= 0:
                print("Setting Relay: {}, State: 1".format(i - offset))
                self.__gpio.set_relay(i - offset, state=1)
            if i <= max_val:
                print("Setting Relay: {}, State: 0".format(i))
                self.__gpio.set_relay(i, state=0)
            else:
                print("Setting Relay: {}, State: 1".format(i - offset))
                self.__gpio.set_relay(i - offset, state=1)
            self.__gpio.change_relay_state()
            time.sleep(1)
        return

    def inflate_all(self):
        self.head_inflate()
        self.shoulders_inflate()
        self.back_inflate()
        self.butt_inflate()
        self.calves_inflate()
        self.feet_inflate()

    def inflate_all_slowly(self):
        print("Inflating everything Slowly")
        max_val = 20 - 1
        for i in range(1, max_val):
            random_val = random.randint(1, max_val)
            self.__gpio.set_relay(random_val, state=0)
            self.__gpio.change_relay_state()
            time.sleep(0.5)
            self.__gpio.set_relay(random_val, state=1)
            self.__gpio.change_relay_state()
            time.sleep(5)
        return

    def message_wave_one(self):
        time_inflate = 2
        time_deflate = 1
        self.head_deflate()
        time.sleep(time_deflate)
        self.shoulders_deflate()
        time.sleep(time_deflate)
        self.back_deflate()
        time.sleep(time_deflate)
        self.butt_deflate()
        time.sleep(time_deflate)
        self.head_inflate()
        self.calves_deflate()
        time.sleep(time_inflate)
        self.shoulders_inflate()
        self.feet_inflate()
        time.sleep(time_inflate)
        self.back_inflate()
        time.sleep(time_inflate)
        self.butt_inflate()
        time.sleep(time_inflate)
        self.calves_inflate()
        time.sleep(time_inflate)
        self.feet_inflate()
        self.inflate_all()
        time.sleep(10)
        return

    def message_head(self):
        self.head_deflate()
        time.sleep(15)
        self.head_inflate()
        time.sleep(30)

    def message_calves(self):
        print("Message Calves")
        min_val = 11
        offset = 3
        max_val = 17
        for i in range(min_val, max_val + offset):
            if (i - offset) > 0:
                print("Setting Relay: {}, State: 1".format(i - offset))
                self.__gpio.set_relay(i - offset, state=1)
            if i < max_val:
                print("Setting Relay: {}, State: 0".format(i))
                self.__gpio.set_relay(i, state=0)
            else:
                print("Setting Relay: {}, State: 1".format(i - offset))
                self.__gpio.set_relay(i - offset, state=1)
            self.__gpio.change_relay_state()
            time.sleep(2)
        time.sleep(10)
        return

    def rand_inflate_quick(self):
        print("Inflating Random quickly")
        self.inflate_all()
        max_val = 20 - 1
        for i in range(1, 10):
            random_val_1 = random.randint(1, max_val)
            random_val_2 = random.randint(1, max_val)
            self.__gpio.set_relays([random_val_1, random_val_2], state=0)
            self.__gpio.change_relay_state()
            time.sleep(1.5)
            self.__gpio.set_relays([random_val_1, random_val_2], state=1)
            self.__gpio.change_relay_state()
            time.sleep(3)
        return

    def message_stretch(self):
        print("Deflating head, back, shoulders")
        self.head_deflate()
        self.shoulders_deflate()
        self.back_deflate()
        time.sleep(6)
        print("Inflating head, shoulders, back")
        self.head_inflate()
        self.shoulders_inflate()
        self.back_inflate()
        time.sleep(15)
        print("Deflating head, shoulders, butt, calves, feet")
        self.head_deflate()
        self.shoulders_deflate()
        self.butt_deflate()
        self.calves_deflate()
        self.feet_deflate()
        time.sleep(6)
        print("Inflating head, shoulders, butt, calves, feet")
        self.head_inflate()
        self.shoulders_inflate()
        self.butt_inflate()
        self.calves_inflate()
        self.feet_inflate()
        time.sleep(15)
        print("deflating back")
        self.back_deflate()
        time.sleep(6)
        print("Inflating everything")
        self.inflate_all()
        time.sleep(15)

    def message_wave_two(self):
        print("Message Wave Two")
        offset = 3
        max_val = 20
        for i in range(1, max_val + offset):
            if (i - offset) > 0:
                print("Setting Relay: {}, State: 1".format(i - offset))
                self.__gpio.set_relay(i - offset, state=1)
            if i < 20:
                print("Setting Relay: {}, State: 0".format(i))
                self.__gpio.set_relay(i, state=0)
            else:
                print("Setting Relay: {}, State: 1".format(i - offset))
                self.__gpio.set_relay(i - offset, state=1)
            self.__gpio.change_relay_state()

            if 3 <= i <= 8:
                time.sleep(0.75)
            if 9 <= i <= 11:
                time.sleep(0.5)
            else:
                time.sleep(1)
        return

    def message_feet(self):
        self.feet_deflate()
        time.sleep(15)
        self.feet_inflate()
        time.sleep(30)

    def head_inflate(self):
        self.__gpio.set_relays(self.__composition['head'], state=1)
        self.__gpio.change_relay_state()
        return

    def head_deflate(self):
        self.__gpio.set_relays(self.__composition['head'], state=0)
        self.__gpio.change_relay_state()
        return

    def shoulders_inflate(self):
        self.__gpio.set_relays(self.__composition['shoulders'], state=1)
        self.__gpio.change_relay_state()
        return

    def shoulders_deflate(self):
        self.__gpio.set_relays(self.__composition['shoulders'], state=0)
        self.__gpio.change_relay_state()
        return

    def back_inflate(self):
        self.__gpio.set_relays(self.__composition['back'], state=1)
        self.__gpio.change_relay_state()
        return

    def back_deflate(self):
        self.__gpio.set_relays(self.__composition['back'], state=0)
        self.__gpio.change_relay_state()
        return

    def butt_inflate(self):
        self.__gpio.set_relays(self.__composition['butt'], state=1)
        self.__gpio.change_relay_state()
        return

    def butt_deflate(self):
        self.__gpio.set_relays(self.__composition['butt'], state=0)
        self.__gpio.change_relay_state()
        return

    def calves_inflate(self):
        self.__gpio.set_relays(self.__composition['calves'], state=1)
        self.__gpio.change_relay_state()
        return

    def calves_deflate(self):
        self.__gpio.set_relays(self.__composition['calves'], state=0)
        self.__gpio.change_relay_state()
        return

    def feet_inflate(self):
        self.__gpio.set_relays(self.__composition['feet'], state=1)
        self.__gpio.change_relay_state()
        return

    def feet_deflate(self):
        self.__gpio.set_relays(self.__composition['feet'], state=0)
        self.__gpio.change_relay_state()
        return
