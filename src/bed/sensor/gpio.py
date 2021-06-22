import time

import RPi.GPIO as GPIO


class Gpio:
    __rasp_pi_available_gpio = []
    __gpio_pins = {}

    def __init__(self, inflatable_regions):
        GPIO.setmode(GPIO.BCM)

        self.__rasp_pi_available_gpio = [i for i in range(inflatable_regions)]

        for index in range(self.__inflatable_regions):
            self.__gpio_pins[index] = {"gpio_pin": self.__rasp_pi_available_gpio[index], "state": 1}
        GPIO.cleanup()
        for key, value in self.__gpio_pins.items():
            GPIO.setup(value["gpio_pin"], GPIO.OUT)
            GPIO.output(value["gpio_pin"], GPIO.HIGH)
            time.sleep(0.25)
            GPIO.output(value["gpio_pin"], GPIO.LOW)
            time.sleep(0.25)

    def set_relay(self, pin, state):
        # enable all pins
        self.__gpio_pins[pin]["state"] = state

    def change_relay_state(self):
        for key, value in self.__gpio_pins.items():
            if value["state"] == 0:
                # Turn off GPIO
                GPIO.output(value["gpio_pin"], GPIO.HIGH)  # Turn off
            elif value["state"] == 1:
                GPIO.output(value["gpio_pin"], GPIO.LOW)  # Turn on
            else:
                print("Error: GPIO pin could not be set, improper array value %d" % value)

    def get_gpio_pins(self):
        return self.__gpio_pins
