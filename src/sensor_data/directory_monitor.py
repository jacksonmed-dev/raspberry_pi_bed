import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.bed.bed import Bed
from src.sensor_data.util.sensor_data_utils import extract_sensor_dataframe


class OnMyWatch:
    # Set the directory on watch
    __observer = Observer()

    def __init__(self, path, bed: Bed):
        self.__watch_directory = path
        self.__bed = bed
        self.__event_handler = Handler(self.__bed, path)

    def run(self):
        self.__observer.schedule(self.__event_handler, self.__watch_directory, recursive=True)
        self.__observer.start()
        # try:
        #     while True:
        #         time.sleep(5)
        # except:
        #     self.observer.stop()
        #     print("Observer Stopped")

        self.__observer.join()

    def stop(self):
        self.__observer.stop()

    def get_observer(self):
        return self.__observer

    def get_watch_directory(self):
        return self.__watch_directory

    def set_watch_directory(self, path):
        self.__watch_directory = path


class Handler(FileSystemEventHandler):
    def __init__(self, bed: Bed, path):
        self.__bed = bed
        self.__file = path + "/data.csv"

    def on_modified(self, event):
        df = pd.read_csv(self.__file, index_col=0)
        temp = extract_sensor_dataframe(df)
        print("Directory Modified - %s" % event.src_path)

    def on_created(self, event):
        df = pd.read_csv(self.__file, index_col=0)
        temp = extract_sensor_dataframe(df)
        print("Directory Created - %s" % event.src_path)
