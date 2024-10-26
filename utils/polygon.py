from .point import *

class Polygon:
    def __init__(self, points: List[Point] = []):
        self.points = points

    def append(self, p: Point):
        """
        Add the to the end of the list if the added point is not coincide with the last point
        """
        last_points = self.points[len(self.points) - 1]

        if not check_coincide(p, last_points):
            self.points.append(p)

    def pop(self) -> Point:
        """
        Pop and return the last point of the list
        """
        point = self.points.pop()

        return point

    def update_by_idx(self, starting_idx: int, wise: bool):
        size = len(self.points)
        if wise:
            new_points = [self.points[(starting_idx+i) % size] for i in range(size)]
        else:
            new_points = [self.points[(starting_idx-i) % size] for i in range(size)]

        self.points = new_points

    def __len__(self):
        return len(self.points)

    def __getitem__(self, item):
        item = item % len(self.points)
        return self.points[item]

    def __iter__(self):
        if self.points == []:
            return iter(self.points)

        return iter(self.points + [self.points[0]])

    def __str__(self):
        return f"Polygon with length: {len(self.points)} and points: {self.points}"