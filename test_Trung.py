from utils import  *
from algorithms import *
from typing import List

import matplotlib.pyplot as plt


if __name__ == '__main__':
    p = (2,2)
    pol = [(0,0), (7,0), (9,1), (7,3), (8,1), (5,1),(7,2), (6,4), (9,2), (11,2), (10,10), (8, 6),
           (10,7), (10,3), (9,3), (7,6), (4,7), (0,7), (2,5)]
    # pol = [(0,0), (4,0), (4,4), (0,4)]

    # p = (7, 4)
    # pol = [(6,4), (5,1), (10,4), (10,7), (7,9), (3,9), (0,7), (3,6), (5,7), (4,7), (5,8)]

    join_segments, width_of_pol, vis_pol = compute_width_of_polygon(p, pol)

    plot_polygon(Polygon(pol), color='red')
    plot_polygon(vis_pol, 'blue', line_width=0.5)
    plt.plot(p[0], p[1], marker='o')

    # print(f"Join_segments: {type(join_segments)} and min_distance: {width_of_pol}")

    for segment in join_segments:
        x_value = segment[0][0], segment[1][0]
        y_value = segment[0][1], segment[1][1]

        plt.plot(x_value, y_value, color='green')

    plt.show()