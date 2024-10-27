import numpy as np

from .point import *
from typing import Tuple, Union
from .operation import error_delta
from abc import abstractmethod

class LinearElement:
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

    # def is_parallel(self, other: "LinearElement") -> bool:
    #     """
    #     Check whether two linear element is parallel
    #     """
    #     vector_1 = self._vector()
    #     vector_2 = other._vector()
    #
    #     return np.abs(vector_1[0]*vector_2[1] - vector_1[1]*vector_2[0]) <= error_delta

    def get_projection(self, p: Point) -> Point:
        """
        Get the projection of point p onto this
        """
        vector_1 = self._vector()
        vector_2 = p[0] - self.point_1[0], p[1] - self.point_1[1]

        if vector_1[0] == 0 and vector_1[1] == 0:
            raise TypeError("Can not get projection onto a point")

        v1 = vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1]
        v2 = vector_1[0] * vector_1[0] + vector_1[1] * vector_1[1]

        vector_projection = v1/v2 * vector_1[0], v1/v2 * vector_1[1]

        return vector_projection[0] + self.point_1[0], vector_projection[1] + self.point_1[1]

    def get_point_parallel(self, p: Point, other_line: "LinearElement") -> Point:
        """
        Get point p2 in this line such that line segment (p,p2) is parallel with other_line
        """
        v_1 = self._vector()
        v_2 = other_line._vector()

        # Need to solve equation: p + v_2 * t = self.point_1 + v_1 * m => solving system of equations
        A = np.array([[v_2[0], -v_1[0]], [v_2[1], -v_1[1]]])
        b = np.array([self.point_1[0] - p[0], self.point_1[1] - p[1]])

        solution = np.linalg.solve(A, b)
        t = solution[0].astype(float)

        return p[0] + v_2[0] * t, p[1] + v_2[1] * t

    @staticmethod
    def get_angle(segment_1: "LinearElement", segment_2: "LinearElement") -> Union[Angle, None]:
        """
        Get the angle between two shape 2D
        """
        v1 = segment_1._vector()
        v2 = segment_2._vector()

        v1_distance, v2_distance = np.linalg.norm(v1), np.linalg.norm(v2)

        if np.abs(v1_distance) <= error_delta or np.abs(v2_distance) <= error_delta:
            return None

        theta = np.arccos(np.dot(v1, v2) / (v1_distance * v2_distance))
        cross_product = v1[0] * v2[1] - v1[1] * v2[0]

        if cross_product < 0:
            return 2 * np.pi - theta

        return theta

    # def get_angle(self, other: "LinearElement") -> Union[Angle, None]:
    #     """
    #     Get the angle between two shape 2D
    #     """
        # v1 = self._vector()
        # v2 = other._vector()
        #
        # v1_distance, v2_distance = np.linalg.norm(v1), np.linalg.norm(v2)
        #
        # if np.abs(v1_distance) <= error_delta or np.abs(v2_distance) <= error_delta:
        #     return None
        #
        # theta = np.arccos(np.dot(v1, v2) / (v1_distance * v2_distance))
        # cross_product = v1[0]*v2[1] - v1[1]*v2[0]
        #
        # if cross_product < 0:
        #     return 2 * np.pi - theta
        #
        # return theta

    def __getitem__(self, item: Union[int, Tuple[slice, int]]):
        if isinstance(item, int):
            if item == 0:
                return self.point_1
            elif item == 1:
                return self.point_2
            else:
                raise IndexError("Expected index in {0, 1}")
        else:
            if isinstance(item[0], slice):
                coord_idx = item[1]
                if coord_idx in (0,1):
                    return np.array([self.point_1[coord_idx], self.point_2[coord_idx]])
                else:
                    raise IndexError("Expected index in {0, 1}")

    def _vector(self):
        return self.point_2[0] - self.point_1[0], self.point_2[1] - self.point_1[1]

class Segment(LinearElement):
    def compute_length(self) -> float:
        return np.linalg.norm(np.subtract(self.point_1, self.point_2))

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

    def check_lie_on(self, point: Point):
        return check_on_segment(self.point_1, self.point_2, point)

    def __str__(self):
        return f"Segment: ({self.point_1}, {self.point_2})"

class Ray(LinearElement):
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
        vector_1 = self._vector()
        vector_2 = point[0] - self.point_1[0], point[1] - self.point_1[1]

        if np.abs(vector_2[0] * vector_1[1] - vector_2[1] * vector_1[0]) > error_delta:
            return False

        return vector_1[0] * vector_2[0] >= 0

class Line(LinearElement):
    @classmethod
    def from_segment(cls, s: Segment) -> "Line":
        return cls(s.point_1, s.point_2)

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