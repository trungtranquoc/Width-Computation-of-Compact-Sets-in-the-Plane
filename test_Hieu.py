from typing import Tuple, List, Annotated
import numpy as np

# Define the error
error_delta = 0.0000005

# Define basic structure
Point = Tuple[float, float]
Angle = Annotated[float, "range: 0 <= value < 2pi"] | None

def get_angle(p: Point, p1: Point, p2: Point) -> Angle:
    """
    Return the angle between two vector, pp1 and pp2
    """
    pp1_vector = p1[0] - p[0], p1[1] - p[1]
    pp2_vector = p2[0] - p[0], p2[1] - p[1]

    pp1_distance = np.linalg.norm(pp1_vector)
    pp2_distance = np.linalg.norm(pp2_vector)

    if np.abs(pp1_distance) <= error_delta or np.abs(pp2_distance) <= error_delta:
        return None

    theta = np.arccos(np.dot(pp1_vector, pp2_vector) / (pp1_distance * pp2_distance))
    cross_product = pp1_vector[0]*pp2_vector[1] - pp1_vector[1]*pp2_vector[0]

    if cross_product < 0:
        return 2 * np.pi - theta

    return theta