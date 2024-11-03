# external imports
from threading import Condition
# internal imports
# from ..actors.radar import Radar

class Monitor:
    def __init__(self):
        # Data structure
        # (radar name, distance, facing angle)
        self._detections:list[tuple[any, float, float]] = []
        # Lock for controlling access
        self._lock_condition = Condition()

    def add_data(self, radar, distance: float, facing_angle: float):
        with self._lock_condition:
            self._detections.append((radar.name, distance, facing_angle))
            self._lock_condition.notify_all()

    def take_first_detection(self) -> tuple[any, float, float]:
        with self._lock_condition:
            while not self._detections:
                self._lock_condition.wait()
            return self._detections.pop(0)