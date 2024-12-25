"""
This code is copyrighted by Institute of Mathematical and Computational Sciences - IMACS,
    Ho Chi Minh City University of Technology (HCMUT).
Contact: Prof. Phan Thanh An thanhan@hcmut.edu.vn
"""
import sys

from ultralytics import YOLO
import os
import numpy as np
import matplotlib.pyplot as plt
from utils import *
from typing import List, Union, Any
from algorithms import construct_visibility_polygon, compute_width_of_polygon
from matplotlib.backend_bases import MouseEvent
from threading import Lock

lock = Lock()

def read_image(img_path: str, idx_crack: int = 0) -> List[Point]:
    # Nhận diện vết nứt S
    model = YOLO("crack_width_YOLOv8.pt")
    cracks = model.predict(source=img_path, conf=0.4)[0]

    crack = cracks.masks.xy[idx_crack]
    crack = np.concatenate((crack, np.array([crack[0]])))
    crack = crack.astype(np.int32)

    return [(float(x), float(y)) for x, y in crack]


def update_plot(p: Point):
    # Clear the previous plot
    plt.clf()

    # Redraw the polygons and the new point
    try:
        join_segments, width_of_pol, vis_pol = compute_width_of_polygon(p, pol)
        print(f"Width at {p}: {width_of_pol}")

        plot_width_of_polygon(p, pol, vis_pol, join_segments, width_of_pol)
    except Exception as e:
        print(f"Error on point {p}: {e}")
        plot_polygon(pol, color="red")


# Event handler for mouse click
def on_double_click(event: MouseEvent):
    with lock:
        if event.dblclick and event.inaxes:  # Check if click is inside the plot axes
            if event.xdata is None or event.ydata is None:
                print("[ERROR] Can not capture coordiate of Mouse event !")
            else:
                x, y = round(event.xdata, 2), round(event.ydata, 2)
                new_p = (x, y)
                update_plot(new_p)

#Nhập thông tin
if __name__ == '__main__':
    if len(sys.argv) >= 3:
        img_name, idx_crack = sys.argv[1], int(sys.argv[2])
    elif len(sys.argv) == 2:
        img_name, idx_crack = sys.argv[1], 0
    else:
        img_name, idx_crack = '1.jpg', 0

    path_import = 'fig'                    #Thư mục chứa ảnh
    pol = read_image(os.path.join(path_import, img_name), idx_crack=idx_crack)

    # Draw the new point
    fig, ax = plt.subplots()
    plot_polygon(pol, color="red")
    fig.canvas.mpl_connect('button_press_event', on_double_click)

    plt.show()