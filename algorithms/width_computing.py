from utils import *
import numpy as np
from typing import  Union, List, Tuple

def _get_endpoints_intersection(p: Point, edge_1: Segment, edge_2: Segment) -> Union[List[Segment], None]:
    """
    Get the list of valid connected paths from each end-points
    """
    intersected_pairs = []
    for point in edge_1:
        point_symmetric = 2*p[0] - point[0], 2*p[1] - point[1]
        ray = Ray(p, point_symmetric)
        intersected_point = ray.compute_intersection(edge_2)

        if intersected_point is not None:
            intersected_pairs.append(Segment(point, intersected_point))

    for point in edge_2:
        point_symmetric = 2*p[0] - point[0], 2*p[1] - point[1]
        ray = Ray(p, point_symmetric)
        intersected_point = ray.compute_intersection(edge_1)

        if intersected_point is not None:
            intersected_pairs.append(Segment(point, intersected_point))

    if len(intersected_pairs) == 0:
        return None

    return intersected_pairs

def shortest_path_edge_pair(p: Point, edge_1: Segment, edge_2: Segment) -> Union[Tuple[float,Segment], Tuple[None, None]]:
    """
    Compute the shortest segment connecting 2 edges and its length.
    Return None if no path found.
    """
    endpoint_intersected = _get_endpoints_intersection(p, edge_1, edge_2)
    if len(endpoint_intersected) == 0:  # No path joined 2 edges
        return None, None

    u_point_line, v_point_line = None, None
    line_1 = Line.from_segment(edge_1)
    line_2 = Line.from_segment(edge_2)
    o_p = line_1.compute_intersection(line_2)

    if o_p is None: # case 2 edges parallel
        u_point_line = edge_1.get_projection(p)
        v_point_line = edge_2.get_projection(p)

    else:
        p_a = edge_1.get_point_parallel(p, edge_2)
        p_b = edge_2.get_point_parallel(p, edge_1)
        theta = Segment.get_angle(Segment(o_p, p_a), Segment(o_p, p_b))

        l_1 = get_distance(p_a, o_p)
        l_2 = get_distance(p_b, o_p)

        solutions = solve_3rd_equations(1, -l_2* np.cos(theta), l_1 * l_2 * np.cos(theta), -l_1 * l_2 ** 2)
        t = None
        for idx in range(0, 3): # get real positive solution
            if solutions[idx].imag == 0 and solutions[idx].real > 0:
                t = solutions[idx].real
                break

        scale = (l_1 + t) / get_distance(o_p, p_a)
        u_point_line = o_p[0] + scale * (p_a[0] - o_p[0]), o_p[1] + scale * (p_a[1] - o_p[1])
        v_point_line = line_2.compute_intersection(Line(u_point_line, p))

    if edge_1.check_lie_on(u_point_line) and edge_2.check_lie_on(v_point_line):
        return get_distance(u_point_line, v_point_line), Segment(u_point_line, v_point_line)

    min_segment = min(endpoint_intersected, key= lambda x: x.compute_length())

    return min_segment.compute_length(), min_segment