import math

from algorithms import construct_visibility_polygon
from utils import *
import numpy as np
from typing import  Union, List, Tuple

def _get_endpoints_intersection(p: Point, edge_1: Segment, edge_2: Segment) -> List[Segment]:
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
    # if len(intersected_pairs) == 0:
    #     return None

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

    # print(f"Edge_1: {edge_1} and Edge_2: {edge_2} and min_segment: {min_segment}")

    return min_segment.compute_length(), min_segment

def compute_width_of_polygon(p: Point, pol: List[Point]) -> Union[Tuple[List[Segment], float, Polygon], None]:
    vis_pol = construct_visibility_polygon(p, pol)

    if not len(vis_pol):
        return [Segment(p, p)], 0, vis_pol

    # Filter those edge that are not windows
    pair_edges = []

    for idx in range(len(vis_pol)):
        if not Ray(p, vis_pol[idx]).check_lie_on(vis_pol[idx+1]):
            pair_edges.append(Segment(vis_pol[idx], vis_pol[idx+1]))
        # Check if p lie on any edge
        if Segment(vis_pol[idx], vis_pol[idx+1]).check_lie_on(p):
            return [Segment(p, p)], 0.0, VisibilityPolygon(p)

    # Get angle of rotation ray
    def reference_angle(edge: Segment) -> Tuple[Angle, Angle]:
        ray_1 = Ray(p, edge[0])
        ray_2 = Ray(p, edge[1])

        angle_1 = LinearElement.get_angle(referenced_ray, ray_1)
        angle_2 = angle_1 + LinearElement.get_angle(ray_1, ray_2)

        return angle_1, angle_2

    # Get starting point for j
    i, j, size = 0, 0, len(pair_edges)
    while safe_le(reference_angle(pair_edges[j])[1], math.pi):
        j += 1

    size = len(pair_edges)
    min_distance, join_segments = float('inf'), []
    pair_edges.append(pair_edges[0])

    def compute_and_compare(i: int, j: int):
        nonlocal min_distance, join_segments

        distance, join_segment = shortest_path_edge_pair(p, pair_edges[i], pair_edges[j])
        if safe_eq(distance, min_distance) and not (check_coincide(join_segment[0], join_segments[0][0]) or check_coincide(join_segment[0], join_segments[0][1])):
            join_segments.append(join_segment)
        elif distance < min_distance:
            min_distance, join_segments = distance, []
            join_segments.append(join_segment)

    # Main iteration
    while safe_le(reference_angle(pair_edges[i])[0], math.pi) and j < size:
        compute_and_compare(i, j)

        # Move to the next iteration
        new_angle_i = reference_angle(pair_edges[i])[1]
        new_angle_j = reference_angle(pair_edges[j])[1]

        if safe_eq(new_angle_i + math.pi, new_angle_j):
            # Take action for edge i+1 and edge j
            compute_and_compare(i+1, j)

            # Take action for edge i and edge j+1
            compute_and_compare(i, j+1)

            # Update i, j for the next iteration
            i, j = i+1, j+1
        elif new_angle_i + math.pi < new_angle_j:
            i += 1
        else:
            j += 1
    
    return join_segments, min_distance, vis_pol