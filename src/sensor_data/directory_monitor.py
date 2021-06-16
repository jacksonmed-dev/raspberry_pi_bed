import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class OnMyWatch:
    # Set the directory on watch

    def __init__(self, path):
        self.observer = Observer()
        self.watchDirectory = path

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        # try:
        #     while True:
        #         time.sleep(5)
        # except:
        #     self.observer.stop()
        #     print("Observer Stopped")

        self.observer.join()
    def stop(self):
        self.observer.stop()


class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        print("Directory Modified - %s" % event.src_path)

    def on_created(self, event):
        print("Directory Created - %s" % event.src_path)