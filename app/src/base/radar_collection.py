# external imports
from pydantic import BaseModel


class RadarCollection:
    def __init__(self):
        self.radars = []


class PositionData(BaseModel):
    name: str
    position_x: int
    position_y: int
    detection_range: int
    orientation_initial: int
    increment: int
