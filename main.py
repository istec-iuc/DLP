import time
from watchdog.observers import Observer
import ctypes, sys
import Scanner
import os

WatcherPath = os.path.join(os.path.join(os.environ['USERPROFILE']))

class Watcher:
    def __init__(self, path):
        self.observer = Observer()
        self.path = path

    def run(self):
        event_handler = Scanner.Handler()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    Scanner.Handler()
    if is_admin():

        w = Watcher(WatcherPath)

        w.run()


    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
