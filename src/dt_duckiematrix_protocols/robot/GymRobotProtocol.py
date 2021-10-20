from dt_duckiematrix_protocols.robot.RobotProtocolAbs import RobotProtocolAbs


class GymRobotProtocol(RobotProtocolAbs):

    def __init__(self, engine_hostname: str, auto_commit: bool = False):
        super(GymRobotProtocol, self).__init__(engine_hostname, auto_commit)
