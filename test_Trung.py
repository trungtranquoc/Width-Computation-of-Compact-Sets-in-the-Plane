from utils import *

if __name__ == '__main__':
    # segment_A = Segment((2, 1), (6, 1))
    # ray = Ray((2, 4), (3, 3))
    # point = ray.compute_intersection(segment_A)
    segment_A = Segment((0, 0), (100, 100))
    segment_B = Segment((0, 100), (100, 0))
    point = segment_A.compute_intersection(segment_B)
    print(point)