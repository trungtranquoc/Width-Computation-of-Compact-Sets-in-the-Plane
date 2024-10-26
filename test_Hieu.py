from utils import *

if __name__ == '__main__':
    p = (3,2)
    segment_A = Segment((1,1),(5,1))
    segment_B = Segment((0,0), (2,2))
    line_A = Line.from_segment(segment_A)
    print("Point p2 in A such that pp2 || B:", segment_A.get_point_parallel(p, segment_B))