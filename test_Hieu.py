from algorithms import *
from utils import *
import cv2
import matplotlib.pyplot as plt

if __name__ == '__main__':
    p = (4,2)
    segment_A = Segment((1,3),(3,3))
    segment_B = Segment((1,0), (7,0))
    shortest_path, pair = shortest_path_edge_pair(p, segment_A, segment_B)

    plt.plot(segment_A[:, 0], segment_A[:, 1])
    plt.plot(segment_B[:, 0], segment_B[:, 1])
    plt.plot(pair[:, 0], pair[:, 1], marker='o')
    plt.plot(p[0], p[1], marker='o')
    plt.show()