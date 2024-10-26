from utils import  *
from algorithms import *

if __name__ == '__main__':
    p = (2,3)
    pol = [(0,0), (0,5), (6,3), (5,3), (4,2), (4,3), (3,3), (5,0)]
    op_pol = [pol[len(pol)-idx-1] for idx in range(len(pol))]

    vis_pol = construct_visibility_polygon(p, op_pol)

    print(vis_pol)