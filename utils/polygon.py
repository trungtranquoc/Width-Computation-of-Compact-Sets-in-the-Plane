from .point import *

class Polygon:
    def __init__(self, points: List[Point] = []):
        self.points = points

    def append(self, p: Point):
        length = len(self.points)
        if 