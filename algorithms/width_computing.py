from utils import *
import numpy as np
from typing import  Union, List

def check_visible(p: Point, edge_1: Segment, edge_2: Segment) -> Union[List[Segment], None]:
    """
    Check whether the pair of edge is visible through p
    """
    intersected_pairs = []
    for point in edge_1:
        point_symmetric = np.subtract(p*2, point)
        ray = Ray(p, point_symmetric)
        intersected_point = ray.compute_intersection(edge_2)

        if intersected_point is not None:
            intersected_pairs.append(Segment(point, intersected_point))

    if len(intersected_pairs) == 0:
        return None

    return intersected_pairs