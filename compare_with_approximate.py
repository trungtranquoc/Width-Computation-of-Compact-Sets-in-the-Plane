"""
This code is copyrighted by Institute of Mathematical and Computational Sciences - IMACS,
    Ho Chi Minh City University of Technology (HCMUT).
Contact: Prof. Phan Thanh An thanhan@hcmut.edu.vn
"""
import matplotlib.pyplot as plt
from algorithms import compute_width_of_polygon, hh_width_point_approx
from utils import plot_polygon

#Nhập thông tin
if __name__ == '__main__':
    pol = [(0,0), (7,0), (9,1), (7,3), (8,1), (5,1),(7,2), (6,4), (9,2), (11,2), (10,10), (8, 6),
           (10,7), (10,3), (9,3), (7,6), (4,7), (0,7), (2,5)]

    # Draw the new point
    points = [(2,2), (2,4), (2,6), (3,4), (3,5), (4,2), (6,2), (9,7)]

    for p in points:
        try:
            join_segments, width_of_pol, vis_pol = compute_width_of_polygon(p, pol)
            appr_width_3 = hh_width_point_approx(p, pol, N=3).width
            appr_width_4 = hh_width_point_approx(p, pol, N=4).width

            print(f"{p} {round(width_of_pol, 2)} {round(appr_width_3, 2)} {round(appr_width_4, 2)}")

            plt.plot(p[0], p[1], marker='o', color='blue', markersize=2)
        except:
            pass

    plot_polygon(pol, color='red')

    plt.show()