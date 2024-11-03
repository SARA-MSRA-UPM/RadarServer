# external imports
from math import (
    cos, sin, pi
)

# internal imports
from .point import Point


class CircularPoint(Point):

    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x, y)
        self.cx = self.x
        self.cy = self.y
        self.radius = radius
        self.angle = 0
        self.update()

    # Circular motion
    def update(self):
        # Keep angle in [0, 2π] range
        self.angle = (self.angle + .1) % (2 * pi)
        self.x = self.cx + cos(self.angle) * self.radius
        self.y = self.cy + sin(self.angle) * self.radius
