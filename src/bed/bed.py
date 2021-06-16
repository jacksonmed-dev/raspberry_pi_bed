from src.sensor_data.tactilus import PressureSensor
from src.body.body import Patient


class Bed:
    # A bed contains the following:
    #   Patient
    #   Sensor
    #   Relays to control the valves
    __pressure_sensor = PressureSensor()
    __relay_count = 1

    def __init__(self, patient: Patient):
        self.__patient = patient
        return

    def get_pressure_sensor(self):
        return self.__pressure_sensor

    def get_relay_count(self):
        return self.__relay_count

    def get_patient(self):
        return self.__patient

    def set_pressure_sensor(self, pressure_sensor: PressureSensor):
        self.__pressure_sensor = pressure_sensor

    def set_relay_count(self, relay_count):
        self.__relay_count = relay_count

    def set_patient(self, patient: Patient):
        self.__patient = patient

    def enable_relays(self, pins):
        # enable all pins
        for pin in pins:
            # enable the pin to turn on relay
            dummy = 5

    def disable_relays(self, pins):
        for pin in pins:
            # disable the pin to turn on relay
            dummy = 5

    # Getters/Setters
