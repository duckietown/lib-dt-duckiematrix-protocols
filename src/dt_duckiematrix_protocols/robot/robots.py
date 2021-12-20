from enum import Enum
from typing import Optional, Dict, Set, Union, List

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.commons.ProtocolAbs import ProtocolAbs
from dt_duckiematrix_protocols.robot.RobotProtocols import RobotProtocolAbs
from dt_duckiematrix_protocols.robot.features.sensors import Camera, TimeOfFlight
from dt_duckiematrix_protocols.robot.features.motion import DifferentialDrive, \
    DifferentialDriveWheels
from dt_duckiematrix_protocols.types.geometry import IPose3D
from dt_duckiematrix_protocols.utils.Pose3D import Pose3D


# Robot Configurations:
#
# # Duckiebot
# DB18 = 10
# DB19 = 11
# DB20 = 12
# DB21M = 13
# DB21J = 14
# DB21R = 15
# # Watchtower
# WT18 = 20
# WT19A = 21
# WT19B = 22
# WT21A = 23
# WT21B = 24
# # Traffic Light
# TL18 = 30
# TL19 = 31
# TL21 = 32
# # Green Station
# GS17 = 40
# # Duckietown
# DT20 = 50
# DT21 = 51
# # Duckiedrone
# DD18 = 60
# # Workstation
# WS21A = 70
# WS21B = 71
# WS21C = 72
# # Duckiecam
# DC21 = 80


class RobotFeature(Enum):
    # motion
    FRAME = "frame"
    DIFFERENTIAL_DRIVE = "wheels"
    # cameras
    CAMERA_0 = "camera_0"
    # lights
    LIGHT_0 = "light_0"
    LIGHT_1 = "light_1"
    LIGHT_2 = "light_2"
    LIGHT_3 = "light_3"
    LIGHT_4 = "light_4"
    # encoders
    ENCODER_LEFT = "encoder_left"
    ENCODER_RIGHT = "encoder_right"
    # ToFs
    TOF_FRONT_CENTER = "tof_front_center"
    TOF_FRONT_LEFT = "tof_front_left"
    TOF_FRONT_RIGHT = "tof_front_right"
    TOF_BACK_LEFT = "tof_back_left"
    TOF_BACK_RIGHT = "tof_back_right"
    # IMUs
    IMU_0 = "imu_0"
    # DISPLAYs
    DISPLAY_0 = "display_0"
    # Buttons
    BUTTON_0 = "button_0"


class RobotAbs:

    def __init__(self, robot_proto: RobotProtocolAbs, key: str,
                 features: Set[RobotFeature],
                 layer_proto: Optional[LayerProtocol] = None, **_):
        self._key: str = key
        self._features: Set[RobotFeature] = features
        self._protocols: Dict[str, Union[None, LayerProtocol, RobotProtocolAbs]] = {
            "layer": layer_proto,
            "robot": robot_proto,
        }
        # fields
        # - pose
        self._pose: Optional[IPose3D] = None
        if RobotFeature.FRAME in features:
            self._assert_protocols(RobotFeature.FRAME, ["layer"])
            self._pose = Pose3D(self._protocol("layer"), key)
        # - differential drive
        self._drive: Optional[DifferentialDrive] = None
        if RobotFeature.DIFFERENTIAL_DRIVE in features:
            self._assert_protocols(RobotFeature.DIFFERENTIAL_DRIVE, ["robot"])
            wheels_key = self._resource_key("wheels")
            self._drive = DifferentialDrive(self._protocol("robot"), wheels_key)
        # - camera_0
        self._camera_0: Optional[Camera] = None
        if RobotFeature.CAMERA_0 in features:
            self._assert_protocols(RobotFeature.CAMERA_0, ["robot"])
            camera_0_key = self._resource_key("camera_0")
            self._camera_0 = Camera(self._protocol("robot"), camera_0_key)
        # - wheels
        self._wheels: Optional[DifferentialDriveWheels] = None
        if RobotFeature.DIFFERENTIAL_DRIVE in features:
            encoder_left: bool = RobotFeature.ENCODER_LEFT in features
            encoder_right: bool = RobotFeature.ENCODER_RIGHT in features
            self._wheels = DifferentialDriveWheels(robot_proto, key, encoder_left, encoder_right)

    def session(self) -> ProtocolAbs.SessionProtocolContext:
        return self._protocol("robot").session()

    @property
    def pose(self) -> IPose3D:
        return self._pose

    def time_of_flight(self, name: str) -> Optional[TimeOfFlight]:
        tof_name = f"tof_{name}"
        # make sure the feature exists
        try:
            feature = RobotFeature(tof_name)
        except ValueError:
            raise ValueError(f"Time-of-Flight feature '{name}' not recognized.")
        # make sure the robot has this feature
        if feature not in self._features:
            raise ValueError(f"Robot {type(self).__name__} does not have the feature '{feature}'")
        # return pointer to sensor object
        tof_key = self._resource_key(tof_name)
        return TimeOfFlight(self._protocol("robot"), tof_key)

    def _protocol(self, name: str):
        return self._protocols[name]

    def _resource_key(self, resource: str):
        return f"{self._key}/{resource}".rstrip("/")

    def _assert_protocols(self, feature: RobotFeature, protocols: List[str]):
        for protocol in protocols:
            protocol = self._protocol(protocol)
            if protocol is None:
                raise ValueError(f"Robot {self._key}, model {self.__class__.__name__} has feature "
                                 f"{feature} enabled, which requires the '{protocol}' "
                                 f"protocol, which was not provided.")


class CameraEnabledRobot(RobotAbs):

    @property
    def camera(self) -> Camera:
        return self._camera_0


class WheeledRobot(RobotAbs):

    @property
    def wheels(self) -> DifferentialDriveWheels:
        return self._wheels


class DifferentialDriveRobot(RobotAbs):

    @property
    def drive(self) -> DifferentialDrive:
        return self._drive


# DB - Duckiebots

class DBRobot(CameraEnabledRobot, WheeledRobot, DifferentialDriveRobot):
    pass


class DB2XRobot(DBRobot):
    pass


class DB21M(DB2XRobot):
    pass


class DB21J(DB2XRobot):
    pass


class DB21R(DB2XRobot):
    pass


class DB1XRobot(DBRobot):
    pass


class DB19(DB1XRobot):
    pass


class DB18(DB1XRobot):
    pass


# WT - Watchtowers

class WTRobot(CameraEnabledRobot):
    pass


class WT2XRobot(WTRobot):
    pass


class WT21A(WT2XRobot):
    pass


class WT21B(WT2XRobot):
    pass


class WT1XRobot(WTRobot):
    pass


class WT19A(WT1XRobot):
    pass


class WT19B(WT1XRobot):
    pass


class WT18(WT1XRobot):
    pass


# DC - Duckiecam

class DCRobot(CameraEnabledRobot):
    pass


class DC2XRobot(DCRobot):
    pass


class DC21(DC2XRobot):
    pass


__all__ = [
    "RobotFeature",
    "RobotAbs",
    # Duckiebots
    "DBRobot",
    "DB21M",
    "DB21J",
    "DB21R",
    "DB19",
    "DB18",
    # Watchtowers
    "WTRobot",
    "WT21A",
    "WT21B",
    "WT19A",
    "WT19B",
    "WT18",
    # Duckiecams
    "DCRobot",
    "DC21",
    # Generic Robots
    "CameraEnabledRobot",
    "WheeledRobot",
    "DifferentialDriveWheels"
]
