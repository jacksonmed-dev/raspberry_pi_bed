import os
import time
from datetime import timedelta

if os.uname()[4][:3] == 'arm':
    from bed.sensor.gpio import Gpio
else:
    from bed.sensor.dummy_gpio import Gpio


class Message:
    # Same value for inflatable_regions and relay count. There may be a situation where there are more relays than
    # inflatable regions. For now, the variable serves no purpose
    __inflatable_regions = 20
    __relay_count = 20
    # __pressure_sensor = PressureSensor(__inflatable_regions)
    __gpio = Gpio(inflatable_regions=__inflatable_regions)
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

    def __init__(self):
        print("Starting Message \n\n\n")
        # self.inflate_all()
        return

    def message(self):
        while True:
            self.message_wave_two()
        return

    def inflate_all(self):
        self.head_inflate()
        self.shoulders_inflate()
        self.back_inflate()
        self.butt_inflate()
        self.calves_inflate()
        self.feet_inflate()

    def message_wave_one(self):
        self.head_deflate()
        time.sleep(1)
        self.shoulders_deflate()
        time.sleep(1)
        self.back_deflate()
        time.sleep(1)
        self.butt_deflate()
        time.sleep(1)
        self.head_inflate()
        self.calves_deflate()
        time.sleep(1)
        self.shoulders_inflate()
        self.feet_inflate()
        time.sleep(1)
        self.back_inflate()
        time.sleep(1)
        self.butt_inflate()
        time.sleep(1)
        self.calves_inflate()
        time.sleep(1)
        self.feet_inflate(1)
        time.sleep(10)
        return

    def message_wave_two(self):
        print("Message Wave Two")
        offset = 5
        max_val = 20
        for i in range(1, max_val + offset):
            if (i - 5) > 0:
                print("Setting Relay: {}, State: 1".format(i - offset))
                self.__gpio.set_relay(i - offset, state=1)
            if i < 20:
                print("Setting Relay: {}, State: 0".format(i))
                self.__gpio.set_relay(i, state=0)
            else:
                print("Setting Relay: {}, State: 1".format(i - offset))
                self.__gpio.set_relay(i - offset, state=1)
            self.__gpio.change_relay_state()
            time.sleep(1)
        time.sleep(10)
        return

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
