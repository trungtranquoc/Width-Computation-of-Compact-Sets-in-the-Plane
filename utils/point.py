from typing import Tuple, List, Annotated
import numpy as np

# Define the error
error_delta = 0.0000005

# Define basic structure
Point = Tuple[float, float]
Angle = Annotated[float, "rangee: 0 <= value < 2pi"]

# Operation on points
def check_on_segment(p1: Point, p2: Point, p: Point) -> bool:
    """
    Check if the point p lies in the axis-aligned segment with endpoints p1, p2
    """
    return get_distance(p1,p) + get_distance(p2,p) == get_distance(p1,p2)

def get_angle(p: Point, p1: Point, p2: Point) -> Angle:
    """
    Return the angle between two vector, pp1 and pp2
    """
    p1_distance = get_distance(p1,p)
    p2_distance = get_distance(p2,p)
    if p1_distance == 0 or p2_distance == 0:
        return 0
    return p1[0]

def get_distance(p1: Point, p2: Point) -> float:
    """
    Get distance between two points
    """
    return np.linalg.norm(np.subtract(p1, p2))

def check_concide(p1: Point, p2: Point) -> bool:
    """
    Check whether two points are concide in given error
    """
    return abs(p1[0]-p2[0]) < error_delta and abs(p1[1]-p2[1]) < error_delta