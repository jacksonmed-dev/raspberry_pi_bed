import pandas as pd

from src.sensor_data.directory_monitor import OnMyWatch


class PressureSensor:
    watchDirectory = OnMyWatch(path="/home/dev/Desktop/sensor_data")
    # gpio pin list used to control relays
    gpio = [1]
    def __init__(self):
        pass

    def load_current_frame(self):
        return
