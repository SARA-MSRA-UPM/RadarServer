# external imports
from math import cos, sin, radians

# internal imports
from ..actors.points.point import Point
# from ..actors.radar import Radar


def radar_detection_to_point(
        detection: tuple[any, float, float]) -> Point:
    radar, distance, facing = detection
    point_angle = radians(radar.orientation_initial + facing)
    return Point(
        x=radar.x + distance * cos(point_angle),
        y=radar.y + distance * sin(point_angle),
    )


def rotate(p: tuple, angle: float) -> tuple:
    """
    Rotate a point around the origin by a given angle in degrees.
    """
    x, y = p
    angle = radians(angle)
    x_new = x * cos(angle) - y * sin(angle)
    y_new = x * sin(angle) + y * cos(angle)
    return x_new, y_new


def rotate_figure(points: list[tuple], angle: float, center: tuple) -> list[tuple]:
    """
    Rotate a figure around a center point by a given angle in degrees.
    """
    return [translate(rotate(p, angle), center[0], center[1]) for p in translate_figure(points, (-center[0], -center[1]))]


def translate_figure(points: list[tuple], center: tuple) -> list[tuple]:
    """
    Translate a figure by a given center point.
    """
    return [translate(p, center[0], center[1]) for p in points]


def translate(p: tuple, dx: float, dy: float) -> tuple:
    """
    Translate a point by dx and dy.
    """
    return p[0] + dx, p[1] + dy
