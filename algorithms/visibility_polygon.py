import math
from typing import List
from utils import *

def construct_visibility_polygon(p: Point, pol: List[Point]) -> Polygon:
    """
    Build the visibility polygon of polygon `pol` and point `p`
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
            min_distance = distance
            starting_idx, init_point = idx, intersection

    wise_angle = LinearElement.get_angle(referenced_ray, Segment(pol[starting_idx], pol[starting_idx + 1]))
    pol.update_by_idx(starting_idx, safe_le(wise_angle, math.pi))
    # print(f"polygon after stage 1: {pol}")

    # Stage 2: Build visibility set
    # Define reference_angle function
    def reference_angle(p1: Point) -> Angle:
        return LinearElement.get_angle(referenced_ray, Ray(p, p1))

    visibility_polygon = Polygon()
    visibility_polygon.append(init_point)     # append the zero-radian point
    idx = 0

    # Control variables
    visible_window = None
    max_angle = 0

    while idx < len(pol):
        last = visibility_polygon.top()
        current = pol[idx]
        # print(f"Loop {idx}: {current}, max_angle = {max_angle} and visibility polygon: {visibility_polygon}")

        # last and current coincide => skip
        if check_coincide(last, current):
            idx += 1
            continue

        if visible_window is None:
            angle_diff = LinearElement.get_angle(Ray(p, last), Ray(p, current))
            current_angle = reference_angle(current)
            current_edge = Segment(last, current)
            current_ray = Ray(p, current)

            # Case 1.1: The considering edge is counterclockwise
            if safe_le(angle_diff, math.pi):
                # Case 1.1.1
                if safe_le(max_angle, current_angle) or safe_eq(current_angle, 0):
                    max_angle += angle_diff
                    visibility_polygon.append(current)
                # Case 1.1.2
                else:
                    intersection = referenced_ray.compute_intersection(Segment(last, current))
                    if intersection is None:
                        raise TypeError("The intersection in case 1.1.2 return None")

                    max_angle = 2*math.pi
                    visibility_polygon.append(intersection)
                    visible_window = Segment(p, intersection)               # set is_visible to True

            # Case 1.2: The considering edge is clockwise
            else:
                vis_len = len(visibility_polygon)

                # Case 1.2.1
                if vis_len < 2 or LinearElement.get_angle(visibility_polygon.top_edge(), current_edge) > math.pi:
                    visible_window = Ray(p, last)                           # set is_visible to True

                # Case 1.2.2
                else:
                    is_cutting_window = False
                    removed_edge = None

                    while max_angle > current_angle and not is_cutting_window:
                        removed_edge = visibility_polygon.top_edge()
                        first_ray = Ray(p, visibility_polygon.top())
                        visibility_polygon.pop()

                        is_cutting_window = current_edge.compute_intersection(visibility_polygon.top_edge()) is not None
                        max_angle -= LinearElement.get_angle(Ray(p, visibility_polygon.top()), first_ray)

                    # Case 1.2.2.1
                    if not is_cutting_window:
                        intersection =  current_ray.compute_intersection(removed_edge)
                        max_angle += LinearElement.get_angle(Ray(p, visibility_polygon.top()), Ray(p, current))

                        visibility_polygon.append(intersection)
                        visibility_polygon.append(current)

                    # Case 1.2.2.2
                    else:
                        cutting_window = visibility_polygon.top_edge()
                        visibility_polygon.pop()
                        # Case 1.2.2.2.a
                        if cutting_window.check_lie_on(current):
                            while check_coincide(current, pol[idx]):
                                idx += 1

                            next_edge_angle = LinearElement.get_angle(current_edge, Segment(pol[idx], current))
                            visible_angle = LinearElement.get_angle(current_edge, cutting_window)

                            if safe_le(next_edge_angle, visible_angle):
                                visibility_polygon.append(current)
                            else:
                                visible_window = Segment(visibility_polygon.top(), current)
                        # Case 1.2.2.2.b
                        else:
                            intersection = current_edge.compute_intersection(cutting_window)
                            visible_window = Segment(visibility_polygon.top(), intersection)


        # Case 2: is_visible = False
        else:
            prev = pol[idx-1]
            intersection = visible_window.compute_intersection(Segment(prev, current))
            if intersection is not None:
                visibility_polygon.append(intersection)
                visible_window = None                                       # set is_visible to False
                idx -= 1                            # No increase idx

        # Move to the next iteration
        idx += 1

    # If the last point is coincide with the first point, then remove
    if check_coincide(visibility_polygon.top(), visibility_polygon[0]):
        visibility_polygon.pop()

    return visibility_polygon

