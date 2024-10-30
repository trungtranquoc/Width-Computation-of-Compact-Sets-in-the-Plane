"""
This code is copyrighted by Institute of Mathematical and Computational Sciences - IMACS,
    Ho Chi Minh City University of Technology (HCMUT).
Contact: Prof. Phan Thanh An thanhan@hcmut.edu.vn
"""
from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
# from lib_imacs_cracks import *
from utils import *
from typing import List, Union, Any
from algorithms import construct_visibility_polygon, compute_width_of_polygon
from matplotlib.backend_bases import MouseEvent

def read_image(img_path: str, idx_crack: int = 0) -> List[Point]:
    original_image = cv2.imread(img_path)
    # k_width = 0.011754334835464791

    # Nhận diện vết nứt S
    model = YOLO("crack_width_YOLOv8.pt")
    cracks = model.predict(source=img_path, conf=0.4)[0]

    crack = cracks.masks.xy[idx_crack]
    crack = np.concatenate((crack, np.array([crack[0]])))
    crack = crack.astype(np.int32)

    return [(float(x), float(y)) for x, y in crack]


def update_plot(p: Point):
    # Reset vis_pol and recompute it with the new point `p`
    vis_pol = construct_visibility_polygon(p, pol)

    # Clear the previous plot
    plt.clf()

    # Redraw the polygons and the new point
    try:
        join_segments, width_of_pol, vis_pol = compute_width_of_polygon(p, pol)
        print(f"Width at {p}: {width_of_pol}")

        plot_width_of_polygon(p, pol, vis_pol, join_segments)
    except Exception as e:
        print(f"Error on point {p}: {e}")
        plot_polygon(pol, color="red")


# Event handler for mouse click
def on_double_click(event: MouseEvent):
    if event.dblclick and event.inaxes:  # Check if click is inside the plot axes
        new_p = (event.xdata, event.ydata)
        update_plot(new_p)

#Nhập thông tin
if __name__ == '__main__':
    path_import = 'fig'                    #Thư mục chứa ảnh
    img_name = '2.jpg'
    pol = read_image(os.path.join(path_import, img_name), idx_crack=0)

    # Draw the new point
    fig, ax = plt.subplots()
    plot_polygon(pol, color="red")
    fig.canvas.mpl_connect('button_press_event', on_double_click)

    plt.show()