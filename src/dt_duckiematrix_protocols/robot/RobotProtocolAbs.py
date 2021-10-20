from dt_duckiematrix_protocols.commons.CBORProtocol import CBORProtocol


class RobotProtocolAbs(CBORProtocol):

    def __init__(self, engine_hostname: str, auto_commit: bool = False):
        super(RobotProtocolAbs, self).__init__(engine_hostname, "robot", auto_commit)
