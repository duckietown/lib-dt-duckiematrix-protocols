import time

from dt_duckiematrix_protocols import Matrix

matrix = Matrix(
    "localhost",
    auto_commit=True
)

time.sleep(1)

robot = matrix.robots.DB21M("map_0/vehicle_0", raw_pose=True)

speed = 1.0
drive_for_num_steps = 0

for _ in range(drive_for_num_steps):
    print(_)
    speed += 0.0
    with robot.session():
        robot.drive(-speed, speed)
    time.sleep(1 / 60.0)



# matrix._robot_protocol.commit()
