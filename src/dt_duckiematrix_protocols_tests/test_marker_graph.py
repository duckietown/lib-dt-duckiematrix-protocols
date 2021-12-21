import uuid

import numpy as np

from dt_duckiematrix_protocols import Matrix

from dt_maps import Map

map_dir = "/home/afdaniele/code/duckietown/distro/ente/dt-duckiematrix/assets/embedded_maps/demo"
map = Map.from_disk("demo", map_dir)

viewer = Matrix("localhost", auto_commit=True)

G = map.graph(2)
markers = []

with viewer.markers.atomic():

    for node_id, node_data in G.nodes(data=True):
        x, y, z = node_data["position"]
        # cyl = viewer.markers.Cylinder(
        #     f"markers/{node_id}",
        #     x=x, y=y, z=z,
        #     scale=[0.03, 0.03, 0.01],
        #     color=[1.0, 1.0, 1.0, 0.2]
        # )

    for node_u_id, node_v_id in G.edges():
        node_u = G.nodes[node_u_id]
        node_v = G.nodes[node_v_id]
        ux, uy, uz = node_u["position"]
        vx, vy, vz = node_v["position"]

        d = np.linalg.norm([ux-vx, uy-vy, uz-vz]) / 2
        yaw = np.arctan2(vy-uy, vx-ux)

        arrow = viewer.markers.Arrow(
            f"markers/{str(uuid.uuid4())}",
            x=ux, y=uy, z=0.0,
            scale=[0.02, 0.02, d * 0.95],
            yaw=yaw,
            color=[1.0, 1.0, 1.0, 0.2]
        )
        markers.append(arrow)

print("Markers placed, press ENTER to clean up and exit.")
input()

with viewer.markers.atomic():
    for marker in markers:
        marker.destroy()
