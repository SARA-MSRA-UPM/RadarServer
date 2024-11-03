# external imports
import math
from threading import Thread, Event
from time import sleep

# internal imports
from ..actors.points.point import Point
from ..base.monitor import Monitor
from ..helpers.helpers import translate_figure, rotate_figure

TRIANGLE = [(0, 0.5), (0, -0.5), (1, 0)]

class Radar(Thread):
    def __init__(self,
                 name: str,
                 position: tuple[float, float],
                 detection_range: float,
                 orientation_initial: float,
                 increment: float,
                 revolutions_per_second: int,
                 detectable_points: list[Point],
                 monitor: Monitor):
        super().__init__()
        # Radar properties
        self.name = name
        self.x, self.y = position
        self.detection_range = detection_range
        self.detection = self.detection_range
        self.orientation_initial = orientation_initial
        self.facing = 0
        self._revolutions_per_second = revolutions_per_second
        self._increment = increment
        self.detectable_points = detectable_points

        self.triangle = translate_figure(TRIANGLE, (self.x+1, self.y))
        self.triangle = rotate_figure(self.triangle, self.orientation_initial, (self.x, self.y))

        self._monitor = monitor
        # Threads properties
        self._stop_event = Event()

    # Thread methods
    def run(self):
        while not self._stop_event.is_set():
            self._update()
            self.detect(self.detectable_points)
            sleep(self._increment/(360.0*self._revolutions_per_second))

    def stop(self):
        self._stop_event.set()

    # Private Radar methods
    def _update(self):
        self.facing = (self.facing + self._increment) % 360
        self.detection = self.detection_range

    def _in_sector(self, point: Point, sector: float) -> bool:
        angle = self._angle(point)
        return abs(sector - angle) < self._increment/2

    def _angle(self, point: Point):
        return (math.degrees(
            math.atan2(point.y - self.y, point.x - self.x)) + 360) % 360

    def _distance(self, point: Point) -> float:
        return math.hypot(point.x - self.x, point.y - self.y)

    def detect(self, points: list[Point]):
        # determine sector
        sector = (self.orientation_initial + self.facing) % 360
        for point in points:
            if self._in_sector(point, sector):
                distance = self._distance(point)
                if distance < self.detection:
                    self.detection = distance

        if self.detection != self.detection_range:
            self._monitor.add_data(
                radar=self,
                distance=self.detection,
                facing_angle=self.facing
            )

    # Public Radar methods
    ## Methods for visualization
    def facing_point(self):
        """
        Return two points making a line where the radar is facing (counting the
        orientation)
        """
        orientation_rad = math.radians(self.orientation_initial + self.facing)
        l = 3
        p1 = (self.x, self.y)
        p2 = (self.x + l * math.cos(orientation_rad), self.y + l * math.sin(orientation_rad))

        return [p1, p2]

    def detection_line(self):
        orientation_rad = math.radians(self.orientation_initial+self.facing)
        l = self.detection
        p1 = (self.x, self.y)
        p2 = (self.x + l * math.cos(orientation_rad), self.y + l * math.sin(orientation_rad))
        return [p1, p2]

    def detection_area(self):
        orientation_rad = math.radians(self.orientation_initial+self.facing)
        half_increment = math.radians(self._increment/2)
        p1 = (self.x + self.detection_range * math.cos(orientation_rad + half_increment), self.y + self.detection_range * math.sin(orientation_rad + half_increment))
        p2 = (self.x + self.detection_range * math.cos(orientation_rad - half_increment), self.y + self.detection_range * math.sin(orientation_rad - half_increment))
        return [p1, p2, (self.x, self.y)]

