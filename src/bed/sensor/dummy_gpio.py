class Gpio:
    __rasp_pi_available_gpio = []
    __gpio_pins = {}

    def __init__(self, inflatable_regions):
        self.__rasp_pi_available_gpio = [i for i in range(inflatable_regions)]
        for index in range(inflatable_regions):
            self.__gpio_pins[index] = {"gpio_pin": self.__rasp_pi_available_gpio[index], "state": 1}

    def set_relay(self, pin, state):
        # enable all pins
        self.__gpio_pins[pin]["state"] = state

    def change_relay_state(self):
        return

    def get_gpio_pins(self):
        return self.__gpio_pins
