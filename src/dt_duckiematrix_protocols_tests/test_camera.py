import time

import cv2
import matplotlib.pyplot as plt
import numpy as np

from dt_duckiematrix_messages.CameraFrame import CameraFrame
from dt_duckiematrix_protocols import Matrix

# open connection to matrix
matrix = Matrix("localhost")
time.sleep(1)

# create connection to robot
robot = matrix.robots.DB21M("map_0/vehicle_0")

# create matplot window
window = plt.imshow(np.zeros((480, 640, 3)))
plt.axis("off")
fig = plt.figure(1)
plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
plt.pause(0.01)


# new frame callback
def on_new_frame(cframe: CameraFrame):
    # get frame as uint8 array
    jpeg = cframe.as_uint8()
    # uint8 array to bgr8
    rgb = cv2.imdecode(jpeg, cv2.IMREAD_COLOR)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
    # show frame
    window.set_data(bgr)
    fig.canvas.draw_idle()
    fig.canvas.start_event_loop(0.001)


# attach frame callback to camera feed
robot.camera.attach(on_new_frame)
input()
