from src.sensor_data.tactilus import PressureSensor
class Bed:
    #A bed contains the following:
    #   Patient
    #   Sensor
    #   Relays to control the valves
    pressure_sensor = PressureSensor()

    def __init__(self):
        # open GPIO and set output. Do this for all GPIO pins that are used
        return

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