import matplotlib.pyplot as plt
import numpy as np

from .polygon import Polygon, VisibilityPolygon
from .point import Point
from .geometry_2d import Segment
from typing import List, Union

def plot_polygon(pol: Union[Polygon, List[Point]], color: str, line_width: float = 1, title=None):
    if isinstance(pol, List):
        pol = Polygon(pol)
        
    draw_pol = np.append(pol, pol[0])
    draw_pol = draw_pol.reshape((pol.shape[0]+1, 2))

    x, y = zip(*draw_pol)

    plt.plot(x, y, color=color, linewidth=line_width, label=title)

def plot_width_of_polygon(p: Point, pol: Polygon, vis_pol: VisibilityPolygon, join_segments: List[Segment], width_of_pol: float):
    plot_polygon(pol, color='red', title="Crack contour")
    plot_polygon(vis_pol, 'blue', line_width=0.5, title="Visibility polygon")
    plt.plot(p[0], p[1], marker='o', markersize=2, color='black', label="p")

    for segment in join_segments:
        x_value = segment[0][0], segment[1][0]
        y_value = segment[0][1], segment[1][1]

        plt.plot(x_value, y_value, color='green', label=f"width = {round(width_of_pol, 4)}")
        
    p = (float(round(p[0], 2)), float(round(p[1], 2)))

    plt.legend(loc='best')
    plt.savefig(f"output/crack_03_{p}.png")
    plt.draw()