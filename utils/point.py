from typing import Tuple, List, Annotated, Union
import numpy as np

from .operation import error_delta

# Define basic structure
Point = Tuple[float, float]
Angle = Annotated[float, "range: 0 <= value < 2pi"]

# Operation on points
def check_on_segment(p1: Point, p2: Point, p: Point) -> bool:
    """
    Check if the point p lies in the axis-aligned segment with endpoints p1, p2
    """
    return np.abs(get_distance(p1,p) + get_distance(p2,p) - get_distance(p1,p2)) <= error_delta

def get_distance(p1: Point, p2: Point) -> float:
    """
    Get distance between two points
    """
    return np.linalg.norm(np.subtract(p1, p2))

def check_coincide(p1: Point, p2: Point) -> bool:
    """
    Check whether two points are coincide in given error
    """
    return abs(p1[0]-p2[0]) < error_delta and abs(p1[1]-p2[1]) < error_delta