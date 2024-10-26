from .point import *
from typing import Tuple, Union
from .operation import error_delta
from abc import abstractmethod

class Shape2D:
    def __init__(self, point_1: Point, point_2: Point):
        self.point_1 = point_1
        self.point_2 = point_2

    @abstractmethod
    def check_lie_on(self, point: Point):
        """
        Check whether a point lies in the shape or not
        """
        pass

    @abstractmethod
    def __str__(self):
        pass

    def get_angle(self, other: "Shape2D"):
        """
        Get the angle between two shape 2D
        """
        v1 = self._vector()
        v2 = other._vector()

        v1_distance, v2_distance = np.linalg.norm(v1), np.linalg.norm(v2)

        if np.abs(v1_distance) <= error_delta or np.abs(v2_distance) <= error_delta:
            return None

        theta = np.arccos(np.dot(v1, v2) / (v1_distance * v2_distance))
        cross_product = v1[0]*v2[1] - v1[1]*v2[0]

        if cross_product < 0:
            return 2 * np.pi - theta

        return theta

    def __getitem__(self, item):
        if item == 0:
            return self.point_1
        elif item == 1:
            return self.point_2
        else:
            raise IndexError("Expected index in {0, 1}")

    def _vector(self):
        return self.point_1[0] - self.point_2[0], self.point_1[1] - self.point_2[1]

class Line(Shape2D):
    def compute_intersection(self, other: "Line") -> Union[Point, None]:
        """
        Return intersection point of 2 lines and None if they are parallel or coincide
        """
        (x1, y1), (x2, y2) = self.point_1, self.point_2
        (x3, y3), (x4, y4) = other.point_1, other.point_2

        # compute the denominator of the parametric equations
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if np.abs(denom) <= error_delta:
            return None

        # compute the numerators for the parametric equation
        t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        u_num = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)

        t = t_num / denom
        u = - u_num / denom

        # Calculate the intersection point
        intersect_x = x1 + t * (x2 - x1)
        intersect_y = y1 + t * (y2 - y1)
        return intersect_x, intersect_y

    def __str__(self):
        return f"Line: ({self.point_1}, {self.point_2})"

    def check_lie_on(self, point: Point):

        vector_1 = point[0] - self.point_1[0], point[1] - self.point_1[1]
        vector_2 = point[0] - self.point_2[0], point[1] - self.point_2[1]

        return np.abs(vector_1[0] * vector_2[1] - vector_1[1] * vector_2[0]) <= error_delta

class Segment(Shape2D):
    def check_lie_on(self, point: Point):
        return check_on_segment(self.point_1, self.point_2, point)

    def compute_intersection(self, other: "Segment") -> Union[Point, None]:
        """
        Return intersection point of 2 lines and None if they are not intersected
        """
        (x1, y1), (x2, y2) = self.point_1, self.point_2
        (x3, y3), (x4, y4) = other.point_1, other.point_2

        # compute the denominator of the parametric equations
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if np.abs(denom) <= error_delta:
            return None

        # compute the numerators for the parametric equation
        t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        u_num = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)

        t = t_num / denom
        u = u_num / denom

        # Calculate the intersection point
        # check if the intersection placed on segments or not
        if 0 <= t <= 1 and 0 <= u <= 1:
            intersect_x = x1 + t * (x2 - x1)
            intersect_y = y1 + t * (y2 - y1)
            return intersect_x, intersect_y
        return None

    def __str__(self):
        return f"Segment: ({self.point_1}, {self.point_2})"

class Ray(Shape2D):
    def compute_intersection(self, other: "Ray") -> Union[Point, None]:
        """
        Return intersection point of 2 rays and None if they are not intersected
        """
        (x1, y1), (x2, y2) = self.point_1, self.point_2
        (x3, y3), (x4, y4) = other.point_1, other.point_2

        # compute the denominator of the parametric equations
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if np.abs(denom) <= error_delta:
            return None

        # compute the numerators for the parametric equation
        t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        u_num = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)

        t = t_num / denom
        u = u_num / denom

        # Calculate the intersection point
        # check if the intersection placed on rays or not
        if 0 <= t and 0 <= u:
            intersect_x = x1 + t * (x2 - x1)
            intersect_y = y1 + t * (y2 - y1)
            return intersect_x, intersect_y
        return None

    def compute_intersection(self, other: Segment) -> Union[Point, None]:
        """
        Return intersection point of a ray and a segment, None if they are not intersected
        """
        (x1, y1), (x2, y2) = self.point_1, self.point_2
        (x3, y3), (x4, y4) = other.point_1, other.point_2

        # compute the denominator of the parametric equations
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if np.abs(denom) <= error_delta:
            return None

        # compute the numerators for the parametric equation
        t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        u_num = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)

        t = t_num / denom
        u = u_num / denom

        # Calculate the intersection point
        # check if the intersection placed on rays or not
        if 0 <= t and 0 <= u <= 1:
            intersect_x = x1 + t * (x2 - x1)
            intersect_y = y1 + t * (y2 - y1)
            intersect_x_2 = x3 + u * (x4 - x3)
            intersect_y_2 = y3 + u * (y4 - y3)
            return intersect_x, intersect_y
        return None

    def __str__(self):
        return f"Ray: ({self.point_1}, {self.point_2})"

    def check_lie_on(self, point: Point) -> bool:
        vector_1 = point[0] -self.point_1[0], point[1] -self.point_1[1]
        vector_2 = self.point_2[0] - self.point_1[0], self.point_2[1] - self.point_1[1]

        if abs(vector_1[0] * vector_2[1] - vector_1[1] * vector_2[0]) <= error_delta:
            return False

        return vector_1[0] * vector_2[0] >= 0

if __name__ == "__main__":
    segment_A = Segment((2,1),(6,1))
    ray = Ray((2,4),(3,3))
    point = ray.compute_intersection(segment_A)
    print(point)