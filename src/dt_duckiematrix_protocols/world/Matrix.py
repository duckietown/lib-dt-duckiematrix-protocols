from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.robot.RealtimeRobotProtocol import RealtimeRobotProtocol
from dt_duckiematrix_protocols.robot.RobotProtocolAbs import RobotProtocolAbs
from dt_duckiematrix_protocols.robot.RobotsManager import RobotsManager


class Matrix:

    def __init__(self, engine_hostname: str, auto_commit: bool = True):
        self._robot_protocol: RobotProtocolAbs = RealtimeRobotProtocol(engine_hostname, auto_commit)
        self._layer_protocol: LayerProtocol = LayerProtocol(engine_hostname, auto_commit)
        self.robots = RobotsManager(self._robot_protocol, self._layer_protocol)

    def commit(self):
        self._robot_protocol.commit()
        self._layer_protocol.commit()
