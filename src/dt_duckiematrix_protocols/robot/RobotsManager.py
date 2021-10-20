from threading import Semaphore
from typing import Dict, Type, TypeVar, Optional, Set

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.robot.RobotProtocolAbs import RobotProtocolAbs
from dt_duckiematrix_protocols.robot.robots import RobotAbs, DB21M, RobotFeature
from dt_duckiematrix_protocols.utils.Pose3D import Pose3D

T = TypeVar("T")


class RobotsManager:

    def __init__(self, robot_protocol: RobotProtocolAbs,
                 layer_protocol: Optional[LayerProtocol] = None):
        self._robots: Dict[str, RobotAbs] = {}
        self._robot_protocol = robot_protocol
        self._layer_protocol = layer_protocol
        self._lock = Semaphore(1)

    def _add(self, key: str, robot: RobotAbs):
        # add new robot
        with self._lock:
            self._robots[key] = robot

    def _make_pose(self, key: str, **kwargs) -> Pose3D:
        return Pose3D(self._layer_protocol, key, **kwargs)

    def _make_robot(self, key: str, factory: Type[T], features: Set[RobotFeature],
                    raw_pose: bool = False, **kwargs) -> T:
        # expose raw 'frames' layer
        if raw_pose:
            features.add(RobotFeature.FRAME)
        robot = factory(self._robot_protocol, key, features, self._layer_protocol, **kwargs)
        # add robot
        self._add(key, robot)
        # ---
        return robot

    def DB21M(self, key: str, **kwargs) -> DB21M:
        features: Set[RobotFeature] = {
            RobotFeature.DIFFERENTIAL_DRIVE,
            RobotFeature.CAMERA_0,
            RobotFeature.ENCODER_LEFT,
            RobotFeature.ENCODER_RIGHT,
        }
        return self._make_robot(key, DB21M, features, **kwargs)
