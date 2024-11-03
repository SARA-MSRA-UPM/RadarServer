# external imports
from threading import Thread, Event
from time import sleep
# internal imports


class Point(Thread):
    def __init__(self, x: float, y: float):
        super().__init__()
        self.x = x
        self.y = y
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            self.update()
            sleep(1/10)  # 10 FPS

    def update(self):
        pass
