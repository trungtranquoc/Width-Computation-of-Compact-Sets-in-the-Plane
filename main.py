"""
This code is copyrighted by Institute of Mathematical and Computational Sciences - IMACS,
    Ho Chi Minh City University of Technology (HCMUT).
Contact: Prof. Phan Thanh An thanhan@hcmut.edu.vn
"""

"""
This file is used for compute the width of the crack. Arguments to run this file:
python main.py <img_name> <crack_index>

Where:
    + <img_name> is the name of the image to be cracked in the directory fig
    + <crack_index> is the index of the crack in the image
"""
import sys

from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from utils import *
from algorithms import *

def read_image(img_path: str, idx_crack: int = 0) -> np.ndarray:
    # Nhận diện vết nứt S
    model = YOLO("crack_width_YOLOv8.pt")
    cracks = model.predict(source=img_path, conf=0.4)[0]

    crack = cracks.masks.xy[idx_crack]
    crack = np.concatenate((crack, np.array([crack[0]])))
    crack = crack.astype(np.int32)

    return crack

# Main function
if __name__ == '__main__':
    if len(sys.argv) >= 3:
        img_name, idx_crack = sys.argv[1], int(sys.argv[2])
    elif len(sys.argv) == 2:
        img_name, idx_crack = sys.argv[1], 0
    else:
        img_name, idx_crack = '1.jpg', 0
    path_import = "fig"

    print(f"Read image {os.path.join(path_import, img_name)}, crack index: {idx_crack}")

    # Original image
    img_path = os.path.join(path_import, img_name)
    original_image = cv2.imread(img_path)
    crack = read_image(img_path=img_path, idx_crack=idx_crack)

    skeleton_set = hh_skeletonize(original_image, crack)
    # Number of skip point
    skip_step = 8

    compute_set = [(float(p[0]), float(p[1])) for idx, p in enumerate(skeleton_set) if idx % skip_step == 0]
    pol = [(float(x), float(y)) for x, y in crack]

    # Set up max width
    max_width = 0
    max_p, max_segments = None, []

    for p in compute_set:
        # print(f"Process on point {p}")
        try:
            # Take the upper bound
            w_n = float('inf')
            try:
                w_n = hh_width_point_approx(p, crack, N=3).width
            except:
                pass

            if w_n < max_width:
                continue            # Skip this point

            join_segments, width_of_pol, _ = compute_width_of_polygon(p, pol)

            # Draw point
            plt.plot(p[0], p[1], markersize=2, marker='o', color='black')

            for segment in join_segments:
                x_value = segment[0][0], segment[1][0]
                y_value = segment[0][1], segment[1][1]

                plt.plot(x_value, y_value, color='palegreen', linewidth=0.5)

            if width_of_pol > max_width:
                max_p, max_segments = p, join_segments
                max_width = width_of_pol

        except Exception as e:
            print(f"Error in point {p}: {e}")
            pass

    # Draw the new point
    plt.plot(max_p[0], max_p[1], marker='o', label="max_p")
    plot_polygon(pol, color="red", title="Crack contour")
    plt.scatter(skeleton_set[:, 0], skeleton_set[:, 1], s=1, color='yellow', label="skeleton")

    for segment in max_segments:
        x_value = segment[0][0], segment[1][0]
        y_value = segment[0][1], segment[1][1]

        plt.plot(x_value, y_value, color='blue', linewidth=1, label=f"width = {round(max_width, 4)}")

    plt.legend(loc='best')

    plt.imshow(original_image)
    plt.show()