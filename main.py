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
from algorithms import construct_visibility_polygon
from matplotlib.backend_bases import MouseEvent

def plot_polygon(pol: Union[Polygon, List[Point]], color: str, line_width: float = 1):
    draw_pol = pol
    draw_pol.append(draw_pol[0])
    x, y = zip(*draw_pol)

    plt.plot(x, y, color=color, linewidth=line_width)

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
    plot_polygon(pol, color='red')
    plot_polygon(vis_pol, 'blue', line_width=0.5)
    plt.plot(p[0], p[1], marker='o', color='black')  # Plot the point

    plt.draw()


# Event handler for mouse click
def on_double_click(event: MouseEvent):
    if event.dblclick and event.inaxes:  # Check if click is inside the plot axes
        new_p = (event.xdata, event.ydata)
        update_plot(new_p)

#Nhập thông tin
if __name__ == '__main__':
    path_import = 'fig'                    #Thư mục chứa ảnh
    # img_name = '2.jpg'
    img_name = '5.png'
    pol = read_image(os.path.join(path_import, img_name), idx_crack=0)

    # p = (307, 200)
    p = (334.18, 311.2)

    # Draw the new point
    fig, ax = plt.subplots()
    vis_pol = construct_visibility_polygon(p, pol)  # Initial visibility polygon
    plot_polygon(pol, color='red')
    plot_polygon(vis_pol, 'blue', line_width=0.5)
    plt.plot(p[0], p[1], marker='o', color='black')
    fig.canvas.mpl_connect('button_press_event', on_double_click)

    plt.show()