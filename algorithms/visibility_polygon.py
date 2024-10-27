import math
from typing import List
from utils import *
# from math import

def construct_visibility_polygon(p: Point, pol: List[Point]) -> Polygon:
    """
    Build the visibility polygon of polygon `pol` and point `p`
    _____
    Stage 1: Find the starting point to start adding

    -----
    Stage 2: Construct visibility polygon
    """
    # Stage 1: Find the starting points
    pol = Polygon(pol)
    min_distance = float('inf')
    referenced_ray = Ray(p, (p[0]+1, p[1]))     # Reference ray
    starting_idx, init_point = None, None

    for idx in range(len(pol)-1):
        edge = Segment(pol[idx], pol[idx+1])
        intersection = referenced_ray.compute_intersection(edge)
        # If no intersection
        if intersection is None:            # No intersect
            continue

        # If the edge is on the reference line
        if referenced_ray.check_lie_on(pol[idx]) and referenced_ray.check_lie_on(pol[idx+1]):
            continue

        distance = get_distance(p, intersection)
        if distance < min_distance:
            print(f"Edge: {edge} intersection: {intersection}")
            min_distance = distance
            starting_idx, init_point = idx, intersection

    wise_angle = Segment.get_angle(referenced_ray, Segment(pol[starting_idx], pol[starting_idx + 1]))
    pol.update_by_idx(starting_idx, safe_le(wise_angle, math.pi))

    # Stage 2: Build visibility set
    visibility_polygon = Polygon()
    visibility_polygon.append(init_point)     # append the zero-radian point



    return pol

