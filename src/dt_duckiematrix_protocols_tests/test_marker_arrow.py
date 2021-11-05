import time

from dt_duckiematrix_protocols import Matrix
from dt_duckiematrix_protocols.types.markers import MarkerType

viewer = Matrix("localhost", auto_commit=True)

time.sleep(1)

arrow = viewer.markers.Arrow(
    "/markers/arrow_0",
    scale=[0.02, 0.02, 0.585 / 2],
    head=MarkerType.CONE
)

yaw = 0.0
for _ in range(1000):
    time.sleep(1 / 240.0)
    yaw += 0.01
    arrow.pose.yaw = yaw
