import time

from dt_duckiematrix_protocols import Matrix

matrix = Matrix(
    "localhost",
    auto_commit=True
)

time.sleep(1)

robot = matrix.robots.DB21M("vautobot00", raw_pose=True)

speed = 1.0
drive_for_num_steps = 0

for _ in range(drive_for_num_steps):
    print(_)
    speed += 0.0
    with robot.session():
        robot.drive(-speed, speed)
    time.sleep(1 / 60.0)
