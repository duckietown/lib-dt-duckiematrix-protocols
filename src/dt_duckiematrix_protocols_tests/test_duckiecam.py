import time
from threading import Condition, Thread

import cv2
import numpy as np
import matplotlib.pyplot as plt

from dt_duckiematrix_messages.CameraFrame import CameraFrame
from dt_duckiematrix_protocols import Matrix

matrix = Matrix(
    "localhost",
    auto_commit=True
)

time.sleep(1)

robot = matrix.robots.DC21("map_0/vehicle_0/cameraman_0")

fourcc = cv2.VideoWriter_fourcc("M", "J", "P", "G")
writer = cv2.VideoWriter("out.avi", fourcc, 20, (1920, 1080), True)

new_frame_evt = Condition()
last_frame = None


def on_new_frame(cframe: CameraFrame):
    global last_frame
    jpeg = cframe.frame
    # bytes to uint8 array
    npjpeg = np.frombuffer(jpeg, np.uint8)
    # uint8 array to rgb8
    img_np = cv2.imdecode(npjpeg, cv2.IMREAD_COLOR)
    # write frame
    writer.write(img_np)
    last_frame = img_np
    with new_frame_evt:
        new_frame_evt.notify_all()


def movie():
    window = plt.imshow(np.zeros((1080, 1920, 3)))
    plt.axis("off")
    fig = plt.figure(1)
    plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
    plt.pause(0.01)

    while True:
        with new_frame_evt:
            new_frame_evt.wait()
        # show frame
        window.set_data(cv2.cvtColor(last_frame, cv2.COLOR_BGR2RGB))
        fig.canvas.draw_idle()
        fig.canvas.start_event_loop(0.001)


movieman = Thread(target=movie, daemon=True)
movieman.start()

robot.camera.attach(on_new_frame)

input()

writer.release()
