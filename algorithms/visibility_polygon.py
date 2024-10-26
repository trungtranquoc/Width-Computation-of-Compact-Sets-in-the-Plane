from typing import List
from utils import *

def construct_visibility_polygon(p: Point, pol: List[Point]) -> Polygon:
    """
    Build the visibility polygon of polygon `pol` and point `p`
    _____
    Stage 1: Find the starting point to start adding
    - Strategy: Find the nearest point by the Oy ray from the point p
    """
    # Stage 1: Find the starting points
    pol = Polygon(pol)
    min_distance = float('inf')
    referenced_ray = Ray(p, (p[0], p[1]+1))     # Reference ray
    starting_idx = None

    for idx in range(len(pol)-1):
        edge = Segment(pol[idx], pol[idx+1])
        intersection = referenced_ray.compute_intersect(edge)
        if intersection is None:            # No intersect
            continue

        distance = get_distance(p, intersection)
        if distance < min_distance:
            min_distance = distance
            starting_idx = idx

    # Stage 2: Build visibility set
    visibility_polygon = Polygon()

    return visibility_polygon