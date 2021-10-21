from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.robot.RobotProtocols import RealtimeRobotProtocol
from dt_duckiematrix_protocols.robot.RobotsManager import RobotsManager
from dt_duckiematrix_protocols.viewer.MarkersManager import MarkersManager


class Matrix:

    def __init__(self, engine_hostname: str, auto_commit: bool = False):
        # create protocols
        self._robot_protocol: RealtimeRobotProtocol = \
            RealtimeRobotProtocol(engine_hostname, auto_commit)
        self._layer_protocol: LayerProtocol = \
            LayerProtocol(engine_hostname, auto_commit)
        # robots manager
        self.robots = RobotsManager(
            engine_hostname,
            auto_commit=auto_commit,
            robot_protocol=self._robot_protocol,
            layer_protocol=self._layer_protocol
        )
        # markers manager
        self.markers = MarkersManager(
            engine_hostname,
            auto_commit=auto_commit,
            layer_protocol=self._layer_protocol
        )

    def commit(self):
        self._robot_protocol.commit()
        self._layer_protocol.commit()
