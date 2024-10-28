from . import Segment
from .point import *
from typing import Union

class Polygon:
    def __init__(self, points: List[Point] = []):
        self.points = points

    def append(self, p: Point):
        """
        Add the to the end of the list if the added point is not coincide with the last point
        """
        last_points = self.top()

        if (last_points is None) or not check_coincide(p, last_points):
            self.points.append(p)

    def pop(self):
        """
        Pop and return the last point of the list
        """
        self.points.pop()

    def update_by_idx(self, starting_idx: int, wise: bool):
        size = len(self.points)
        if wise:
            new_points = [self.points[(starting_idx+i+1) % size] for i in range(size)]
        else:
            new_points = [self.points[(starting_idx-i) % size] for i in range(size)]

        self.points = new_points

    def top(self) -> Union[Point, None]:
        """
        Return the last point of the set
        """
        if len(self.points) == 0:
            return None
        return self.points[len(self.points) - 1]

    def top_edge(self) -> Union[Segment, None]:
        """
        Return the last edge of the set
        """
        if (len(self.points) == 0) or (len(self.points) == 1):
            return None
        return Segment(self.points[len(self.points) - 2], self.points[len(self.points) - 1])

    def is_empty(self):
        return self.points == []

    def __len__(self):
        return len(self.points)

    def __getitem__(self, item):
        item = item % len(self.points)
        return self.points[item]

    def __iter__(self):
        return iter(self.points)

    def __str__(self):
        return f"Polygon with length {len(self.points)} and points: {self.points}"