import math
from typing import List
from utils import *
from typing import *
import matplotlib.pyplot as plt

def plot_polygon(pol: Union[Polygon, List[Point]], color: str, line_width: float = 1):
    draw_pol = pol
    # draw_pol.append(draw_pol[0])
    x, y = zip(*draw_pol)

    plt.plot(x, y, color=color, linewidth=line_width)

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

    visibility_polygon = VisibilityPolygon(p)
    visibility_polygon.append(init_point)     # append the zero-radian point
    idx = 0

    # Control variables
    visible_window = None

    # Variable to back tracking in case 1.2.1
    list_of_window = None

    while idx < len(pol):
        last = visibility_polygon.top()
        current = pol[idx]

        # last and current coincide => skip
        if check_coincide(last, current):
            idx += 1
            continue

        # Assign the current value
        current_angle = reference_angle(current)
        current_edge = Segment(last, current)
        current_ray = Ray(p, current)

        if visible_window is None:
            angle_diff = LinearElement.get_angle(Ray(p, last), Ray(p, current))

            # Case 1.1: The considering edge is counterclockwise
            if safe_le(angle_diff, math.pi):
                # Case 1.1.1
                if safe_le(visibility_polygon.max_angle, current_angle) or safe_eq(current_angle, 0):
                    visibility_polygon.append(current)
                # Case 1.1.2
                else:
                    intersection = referenced_ray.compute_intersection(Segment(last, current))
                    if intersection is None:
                        raise TypeError("The intersection in case 1.1.2 return None")

                    visibility_polygon.append(intersection)
                    visible_window = Segment(p, intersection)               # set is_visible to True

            # Case 1.2: The considering edge is clockwise
            else:
                vis_len = len(visibility_polygon)

                # Case 1.2.1
                if vis_len < 2 or LinearElement.get_angle(visibility_polygon.top_edge(), current_edge) > math.pi:
                    visible_window = Ray(p, last)                               # set is_visible to True
                    list_of_window = visibility_polygon.list_windows

                    if list_of_window:
                        _, last_window = list_of_window[0]
                        intersection = last_window.compute_intersection(Segment(last, current))
                        while safe_le(reference_angle(current), reference_angle(list_of_window[0][1][0])) and intersection is None:
                            list_of_window = list_of_window[1:]  # pop the first window
                            if not list_of_window:
                                break
                            intersection = list_of_window[0][1].compute_intersection(Segment(last, current))

                        if intersection is not None:
                            lw_idx, last_window = list_of_window[0]
                            while len(visibility_polygon) > lw_idx:
                                visibility_polygon.pop()

                            visibility_polygon.append(intersection)
                            visible_window, list_of_window = None, None
                            idx -= 1

                    # print(f"lw_idx: {lw_idx} and last_window: {last_window} and current: {current}")

                # Case 1.2.2
                else:
                    is_cutting_window = False
                    removed_edge = None

                    while visibility_polygon.max_angle > current_angle and not is_cutting_window:
                        removed_edge = visibility_polygon.top_edge()
                        visibility_polygon.pop()
                        # Check whether the current_edge cut the window
                        is_cutting_window = current_edge.compute_intersection(visibility_polygon.top_edge()) is not None

                    # Case 1.2.2.1
                    if not is_cutting_window:
                        intersection =  current_ray.compute_intersection(removed_edge)

                        if intersection is None:
                            raise TypeError(f"The intersection of ray {current_ray} and edge {removed_edge} is None")

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
                visible_window, list_of_window = None, None            # set is_visible to False
                idx -= 1

            if list_of_window:
                intersection = list_of_window[0][1].compute_intersection(Segment(prev, current))
                while (safe_le(reference_angle(current), reference_angle(list_of_window[0][1][0]))
                       and intersection is None):
                    list_of_window = list_of_window[1:]             # pop the first window
                    if not list_of_window:
                        break
                    intersection = list_of_window[0][1].compute_intersection(Segment(prev, current))

                if intersection is not None:
                    lw_idx, last_window = list_of_window[0]
                    while len(visibility_polygon) > lw_idx:
                        visibility_polygon.pop()

                    visibility_polygon.append(intersection)
                    visible_window, list_of_window = None, None
                    idx -= 1

        # Mock test for drawing
        # if idx % 1 == 0 and idx > 225:
        #     plot_polygon(pol, color='red')
        #     plot_polygon(visibility_polygon, 'blue', line_width=0.5)
        #     plt.plot(p[0], p[1], marker='o')
        #     plt.plot(current[0], current[1], marker='o', color='black')
        #
        #     plt.title(f"Iterative {idx}")
        #
        #     plt.show()

        # Move to the next iteration
        idx += 1

    # If the last point is coincide with the first point, then remove
    if check_coincide(visibility_polygon.top(), visibility_polygon[0]):
        visibility_polygon.pop()

    return visibility_polygon

