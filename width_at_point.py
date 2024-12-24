from utils import  *
from algorithms import *
from typing import List, Tuple
import sys
import ast

import matplotlib.pyplot as plt


if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
        with open(f"input/{input_file}", 'r') as file:
            data = file.readlines()
            p: Tuple[int, int] = ast.literal_eval(data[0])
            pol: List[Tuple[int, int]] = ast.literal_eval(data[1])
    except Exception as e:
        print(f"Error {e} when reading file, use default input instead")
        p = (4,3)
        pol = [(0, 0), (7, 0), (9, 1), (7, 3), (8, 1), (5, 1), (7, 2), (6, 4), (9, 2), (11, 2), (10, 10), (8, 6), (10, 7),
    (10, 3), (9, 3), (7, 6), (4, 7), (0, 7), (2, 5)]

    join_segments, width_of_pol, vis_pol = compute_width_of_polygon(p, pol)

    plot_polygon(Polygon(pol), color='red', title="Input polygon")
    plot_polygon(vis_pol, 'blue', line_width=0.5, title=f"Visibility polygon at {p}")
    plt.plot(p[0], p[1], marker='o', label="p")
    
    for idx, segment in enumerate(join_segments):
        x_value = segment[0][0], segment[1][0]
        y_value = segment[0][1], segment[1][1]
    
        plt.plot(x_value, y_value, color='green', label=f"Minimum joint segment {idx+1}")
    
    plt.legend(loc="upper left")
    plt.savefig("output/polygon_1_width")
    # plt.savefig("input/polygon_1")
    plt.show()