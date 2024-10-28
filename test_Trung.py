from utils import  *
from algorithms import *
from typing import List

import matplotlib.pyplot as plt

def plot_polygon(pol: Polygon, color: str, line_width: float = 1):
    draw_pol = pol
    draw_pol.append(draw_pol[0])
    x, y = zip(*draw_pol)

    plt.plot(x, y, color=color, linewidth=line_width)


if __name__ == '__main__':
    p = (2,2)
    # pol = [(0,0), (0,5), (4,5), (4,7), (6,3), (5,3), (4,2), (4,4), (3,3), (4,1), (9,3), (10,6), (10, 3), (5,0)]
    pol = [(0,0), (7,0), (9,1), (7,3), (8,1), (5,1),(7,2), (6,4), (9,2), (11,2), (10,10), (8, 6),
           (10,7), (10,3), (9,3), (7,6), (4,7), (0,7), (2,5)]
    # pol = [[-2, 1], [0, 1], [0, 3], [3, 3], [3, -2], [0, -2], [0, -1], [-2, -1], [-2, 1]]
    # pol = [tuple((x, y)) for x, y in pol]

    vis_pol = construct_visibility_polygon(p, pol)

    plot_polygon(Polygon(pol), color='red')
    plot_polygon(vis_pol, 'blue', line_width=0.5)
    plt.plot(p[0], p[1], marker='o')

    plt.show()