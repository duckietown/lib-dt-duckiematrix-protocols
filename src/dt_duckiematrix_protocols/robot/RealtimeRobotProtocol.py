from dt_duckiematrix_protocols.robot.RobotProtocolAbs import RobotProtocolAbs


class RealtimeRobotProtocol(RobotProtocolAbs):

    def __init__(self, engine_hostname: str, auto_commit: bool = False):
        super(RealtimeRobotProtocol, self).__init__(engine_hostname, auto_commit)
