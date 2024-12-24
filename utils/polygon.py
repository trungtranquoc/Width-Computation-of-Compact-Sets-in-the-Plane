from shapely.lib import points

from .geometry_2d import Segment, Ray, LinearElement
from .point import *
from typing import Union

referenced_ray = Ray((0,0), (1,0))

class Polygon:
    def __init__(self, points: List[Point] = None):
        if points is None:
            self.points = []
        else:
            self.points = points

    def get_points(self) -> List[Point]:
        return self.points

    def append(self, p: Point):
        """
        Add the to the end of the list if the added point is not coincide with the last point
        """
        last_points = self.top()

        # Check for coincide with the last point in visibility set
        if (last_points is not None) and check_coincide(p, last_points):
            return

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

    def second(self) -> Union[Point, None]:
        """
        Return the second last point of the set
        """
        if len(self.points) < 2:
            return None
        return self.points[len(self.points) - 2]

    def top_edge(self) -> Union[Segment, None]:
        """
        Return the last edge of the set
        """
        if len(self.points) < 2:
            return None
        return Segment(self.second(), self.top())

    def copy(self):
        """
        Return a copy of the polygon
        """
        return Polygon(self.points)

    def is_empty(self):
        return self.points == []
    
    @property
    def shape(self):
        return [len(self.points), 2]

    def __len__(self):
        return len(self.points)

    def __getitem__(self, item):
        item = item % len(self.points)
        return self.points[item]

    def __iter__(self):
        return iter(self.points)

    def __str__(self):
        return f"Polygon with length {len(self.points)} and points: {self.points}"

class VisibilityPolygon(Polygon):
    def __init__(self, p: Point):
        super().__init__([])
        self.p = p
        self.list_windows = []
        self.max_angle = 0

    def append(self, current: Point):
        """
        Add the to the end of the list if the added point is not coincide with the last point
        """
        last = self.top()

        if last is not None:
            # Check for coincide with the last point in visibility set
            if check_coincide(current, last):
                return

            # Check if the last, second, current and p are on the straight line
            max_ray = Ray(self.p, self.top())

            if max_ray.check_lie_on(current):
                # Check for straight line with the two last point
                if len(self.points) >= 2:
                    second = self.points[len(self.points) - 2]
                    if max_ray.check_lie_on(second):
                        self.pop()

                # Add window
                self.list_windows = [(self.__len__(), Segment(current, self.top()))] + self.list_windows
            else:
                # If no window, then update the max_angle
                self.max_angle += LinearElement.get_angle(Ray(self.p, last), Ray(self.p, current))

        self.points.append(current)

    def pop(self):
        first_ray = Ray(self.p, self.top())
        self.points.pop()
        second_ray = Ray(self.p, self.top())

        # Update the max_angle
        self.max_angle -= LinearElement.get_angle(second_ray, first_ray)

        last_window = self.last_window()
        # If we pop the last window, then pop it from the window
        if last_window is not None and last_window[0] == self.__len__():
            self.list_windows = self.list_windows[1:]

    def last_window(self):
        if self.list_windows:
            return self.list_windows[0]
        return None

    def check_last_edge_is_window(self):
        if not self.list_windows or len(self.points) < 2:
            return False
        else:
            return self.last_window()[0] == len(self.points)