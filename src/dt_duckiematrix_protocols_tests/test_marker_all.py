import uuid

import numpy as np

from dt_duckiematrix_protocols import Matrix

viewer = Matrix("localhost", auto_commit=True)
markers = []


markers_to_place = [
    viewer.markers.Cube,
    viewer.markers.Cylinder,
    viewer.markers.Sphere,
    viewer.markers.Cone,
    viewer.markers.Quad,
]

scale = 0.1

with viewer.markers.atomic():
    for i, Marker in enumerate(markers_to_place):
        key = f"/markers/{str(uuid.uuid4())}"
        marker = Marker(
            key,
            x=scale * 2 * i, y=-0.4, z=scale / 2,
            scale=scale,
            yaw=np.deg2rad(180)
        )
        markers.append(marker)

print("Markers placed, press ENTER to clean up and exit.")
input()

with viewer.markers.atomic():
    for marker in markers:
        marker.destroy()
