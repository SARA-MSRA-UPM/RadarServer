# external imports
from math import (
    cos, sin, pi
)

# internal imports
from .point import Point


class EightPoint(Point):

    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.cx = self.x
        self.cy = self.y
        self.angle = 0
        self.update()

    def update(self):
        # Move x and y in a figure-eight pattern
        self.angle = (self.angle + .1) % (2 * pi)
        self.x = self.cx + sin(self.angle) * 20
        self.y = self.cy + sin(self.angle) * cos(self.angle) * 20
