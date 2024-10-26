from utils import *
import numpy as np
from typing import  Union, List, Tuple

def get_endpoints_intersection(p: Point, edge_1: Segment, edge_2: Segment) -> Union[List[Segment], None]:
    """
    Get the list of valid connected paths from each end-points
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

def shortest_path_edge_pair(p: Point, edge_1: Segment, edge_2: Segment) -> Union[Tuple[float,Segment], None]:
    """
    Compute the shortest segment connecting 2 edges and its length.
    Return None if no path found.
    """
    endpoint_intersected = get_endpoints_intersection(p, edge_1, edge_2)
    if len(endpoint_intersected) == 0:  # No path joined 2 edges
        return None

    u_point_line, v_point_line = None, None
    if edge_1.is_parallel(edge_2): # case 2 edges parallel
        u_point_line = edge_1.get_projection(p)
        v_point_line = edge_2.get_projection(p)

    line_1 = Line.from_segment(edge_1)
    line_2 = Line.from_segment(edge_2)
    o_p = line_1.compute_intersection(line_2)
    theta = edge_1.get_angle(edge_2)
    p_a = edge_1.get_point_parallel(p, edge_2)
    p_b = edge_2.get_point_parallel(p, edge_1)
    l_1 = get_distance(p_a, o_p)
    l_2 = get_distance(p_b, o_p)

    t = solve_3rd_equations(1, -l_2* np.cos(theta), l_1 * l_2 * np.cos(theta), -)


    return None