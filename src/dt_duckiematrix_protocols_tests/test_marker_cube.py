import time

from dt_duckiematrix_protocols import ViewerProtocol

viewer = ViewerProtocol(
    "localhost",
    auto_commit=True
)

time.sleep(1)

cube = viewer.markers.Sphere("/markers/cube_0")








# print(cube.pose)
# print(cube.scale)
# print(cube.color)

cube.scale.x = 0.2
cube.scale.y = 0.2

# print(cube.as_dict())
# print(cube.to_bytes())

# viewer.commit()
#
time.sleep(1)
