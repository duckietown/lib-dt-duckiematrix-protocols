import time

import numpy as np

from dt_duckiematrix_protocols import Matrix

viewer = Matrix("localhost", auto_commit=True)

time.sleep(1)


markers = [
    viewer.markers.Cube,
    viewer.markers.Cylinder,
    viewer.markers.Sphere,
    viewer.markers.Cone,
    viewer.markers.Quad,
]

scale = 0.1

with viewer.markers.atomic():
    for i, Marker in enumerate(markers):
        key = f"/markers/{Marker.__name__}_0".lower()
        marker = Marker(
            key,
            x=scale * 2 * i, y=-0.4, z=scale / 2,
            scale=scale,
            yaw=np.deg2rad(180)
        )

time.sleep(1)
