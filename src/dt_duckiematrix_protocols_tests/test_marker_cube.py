import time

from dt_duckiematrix_protocols import Matrix

viewer = Matrix("localhost", auto_commit=True)

time.sleep(1)

cube = viewer.markers.Sphere("/markers/cube_0")

cube.scale.x = 0.2
cube.scale.y = 0.2

time.sleep(1)
