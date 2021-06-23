import os
from datetime import timedelta
import pandas as pd
from bed.sensor.tactilus import PressureSensor

if os.uname()[4][:3] == 'arm':
    from bed.sensor.gpio import Gpio
else:
    from bed.sensor.dummy_gpio import Gpio


class Message:
    # Same value for inflatable_regions and relay count. There may be a situation where there are more relays than
    # inflatable regions. For now, the variable serves no purpose
    __inflatable_regions = 20
    __relay_count = 20
    __pressure_sensor = PressureSensor(__inflatable_regions)
    __bed_gpio = Gpio(inflatable_regions=__inflatable_regions)
    __body_stats_df = pd.DataFrame(0, index=['head', 'shoulders', 'back', 'butt', 'calves', 'feet'],
                                   columns=['time', 'max_pressure'])
    __composition = __pressure_sensor.get_sensor_body_composition()

    def __init__(self):
        self.__body_stats_df['time'] = timedelta(0)
        return

    def message(self):
        composition = self.__pressure_sensor.get_sensor_body_composition()
        while True:
            self.message_wave()
        return

    def message_wave(self):
        return

    def head_inflate(self):
        self.__bed_gpio.set_relays(self.__composition['head'], state=1)
        self.__bed_gpio.change_relay_state()
        return

    def head_deflate(self):
        self.__bed_gpio.set_relays(self.__composition['head'], state=0)
        self.__bed_gpio.change_relay_state()
        return

    def shoulders_inflate(self):
        self.__bed_gpio.set_relays(self.__composition['shoulders'], state=1)
        self.__bed_gpio.change_relay_state()
        return

    def shoulders_deflate(self):
        self.__bed_gpio.set_relays(self.__composition['shoulders'], state=0)
        self.__bed_gpio.change_relay_state()
        return

    def back_infalte(self):
        self.__bed_gpio.set_relays(self.__composition['back'], state=1)
        self.__bed_gpio.change_relay_state()
        return

    def back_deflate(self):
        self.__bed_gpio.set_relays(self.__composition['back'], state=0)
        self.__bed_gpio.change_relay_state()
        return

    def butt_inflate(self):
        self.__bed_gpio.set_relays(self.__composition['butt'], state=1)
        self.__bed_gpio.change_relay_state()
        return

    def butt_deflate(self):
        self.__bed_gpio.set_relays(self.__composition['butt'], state=0)
        self.__bed_gpio.change_relay_state()
        return

    def calves_inflate(self):
        self.__bed_gpio.set_relays(self.__composition['calves'], state=1)
        self.__bed_gpio.change_relay_state()
        return

    def calves_deflate(self):
        self.__bed_gpio.set_relays(self.__composition['calves'], state=0)
        self.__bed_gpio.change_relay_state()
        return

    def feet_inflate(self):
        self.__bed_gpio.set_relays(self.__composition['feet'], state=1)
        self.__bed_gpio.change_relay_state()
        return

    def feet_deflate(self):
        self.__bed_gpio.set_relays(self.__composition['feet'], state=0)
        self.__bed_gpio.change_relay_state()
        return
