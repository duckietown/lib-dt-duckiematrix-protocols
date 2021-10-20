from abc import abstractmethod, ABC
from enum import IntEnum
from typing import Any, Union

from dt_duckiematrix_messages import CBorMessage
from dt_duckiematrix_protocols.utils.Color import Color
from dt_duckiematrix_protocols.utils.MonitoredObject import MonitoredObject
from dt_duckiematrix_protocols.utils.Pose3D import Pose3D
from dt_duckiematrix_protocols.utils.Vector3 import Vector3


class MarkerType(IntEnum):
    CUBE = 0
    SPHERE = 1
    CYLINDER = 2
    QUAD = 3
    ARROW = 4
    TEXT = 5
    TRAJECTORY = 6


class MarkerAction(IntEnum):
    ADD_OR_UPDATE = 0
    REMOVE = 1
    HIDE = 2
    SHOW = 3


class MarkerScale(Vector3):

    def _make_layers(self):
        self._layers.set_quiet("markers", self._key, "scale", {})

    def _get_property(self, field: str) -> float:
        return self._layers.get("markers", self._key).get("scale").get(field, None)

    def _set_property(self, field: str, value: Any):
        value = Vector3._sanitize_float(field, value)
        marker = self._layers.get("markers", self._key)
        marker["scale"][field] = value
        if self._auto_commit:
            self._commit()

    def _commit(self):
        marker = self._layers.get("markers", self._key)
        self._layers.update("markers", self._key, marker)


class MarkerColor(Color):

    def _make_layers(self):
        self._layers.set_quiet("markers", self._key, "color", {})

    def _get_property(self, field: str) -> float:
        return self._layers.get("markers", self._key).get("color").get(field, None)

    def _set_property(self, field: str, value: Any):
        value = Color._sanitize_float(field, value)
        marker = self._layers.get("markers", self._key)
        marker["color"][field] = value
        if self._auto_commit:
            self._commit()

    def _commit(self):
        marker = self._layers.get("markers", self._key)
        self._layers.update("markers", self._key, marker)


class MarkerAbs(MonitoredObject, CBorMessage):

    def __init__(self, layers, key: str, auto_commit: bool = False):
        super().__init__(auto_commit)
        self._key = key
        self._layers = layers
        # fields
        self._pose: Pose3D = Pose3D(layers, key,
                                    auto_commit=auto_commit)
        self._scale: Vector3 = MarkerScale(layers, key,
                                           auto_commit=auto_commit,
                                           x=1.0, y=1.0, z=1.0)
        self._color: Color = MarkerColor(layers, key,
                                         auto_commit=auto_commit,
                                         r=1.0, g=1.0, b=1.0, a=1.0)
        self._action: MarkerAction = MarkerAction.ADD_OR_UPDATE
        # ---
        self._layers.set_quiet("markers", self._key, "type", self.type)
        self._layers.set_quiet("markers", self._key, "action", self._action)

    def _commit(self):
        self._layers.update("markers", self._key, self.as_dict())

    @property
    @abstractmethod
    def type(self) -> MarkerType:
        pass

    @property
    def pose(self) -> Pose3D:
        return self._pose

    @pose.setter
    def pose(self, value: Pose3D):
        if isinstance(value, Pose3D):
            with self._pose.atomic():
                self._pose.x = value.x
                self._pose.y = value.y
                self._pose.z = value.z
                self._pose.roll = value.roll
                self._pose.pitch = value.pitch
                self._pose.yaw = value.yaw

    @property
    def scale(self) -> Vector3:
        return self._scale

    @scale.setter
    def scale(self, value: Union[int, float, Vector3]):
        if isinstance(value, (float, int)):
            value = float(value)
            with self._scale.atomic():
                self._scale.x = value
                self._scale.y = value
                self._scale.z = value
        elif isinstance(value, Vector3):
            with self._scale.atomic():
                self._scale.x = value.x
                self._scale.y = value.y
                self._scale.z = value.z

    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, value: Union[int, float, Color]):
        if isinstance(value, (float, int)):
            if isinstance(value, int):
                value = value / 255.0
            with self._color.atomic():
                self._color.r = value
                self._color.g = value
                self._color.b = value
        elif isinstance(value, Color):
            with self._color.atomic():
                self._color.r = value.r
                self._color.g = value.g
                self._color.b = value.b
                self._color.a = value.a

    def show(self):
        self._action = MarkerAction.SHOW
        self._layers.update("markers", self._key, {"action": self._action})

    def hide(self):
        self._action = MarkerAction.HIDE
        self._layers.update("markers", self._key, {"action": self._action})

    def destroy(self):
        self._action = MarkerAction.REMOVE
        self._layers.update("markers", self._key, {"action": self._action})

    def as_dict(self) -> dict:
        return self._layers.get("markers", self._key)


class MarkerSimple(MarkerAbs, ABC):
    pass


class MarkerCube(MarkerSimple):

    @property
    def type(self) -> MarkerType:
        return MarkerType.CUBE


class MarkerSphere(MarkerSimple):

    @property
    def type(self) -> MarkerType:
        return MarkerType.SPHERE


class MarkerCylinder(MarkerSimple):

    @property
    def type(self) -> MarkerType:
        return MarkerType.CYLINDER


class MarkerQuad(MarkerSimple):

    @property
    def type(self) -> MarkerType:
        return MarkerType.QUAD


class MarkerArrowDirection(Vector3):

    def _make_layers(self):
        # TODO: implement this
        pass

    def _commit(self):
        # TODO: implement this
        pass

    def _get_property(self, field: str) -> float:
        return self._layers.get("markers", self._key).get("direction").get(field, None)

    def _set_property(self, field: str, value: Any):
        value = Vector3._sanitize_float(field, value)
        marker = self._layers.get("markers", self._key)
        marker["direction"][field] = value
        self._layers.update("markers", self._key, marker)


class MarkerArrow(MarkerAbs):

    @property
    def type(self) -> MarkerType:
        return MarkerType.ARROW

    def __init__(self, layers, key: str):
        super(MarkerArrow, self).__init__(layers, key)
        self._direction: Vector3 = MarkerArrowDirection(layers, key, x=0.0, y=0.0, z=1.0)

    @property
    def direction(self) -> Vector3:
        return self._direction


class MarkerText(MarkerAbs):

    @property
    def type(self) -> MarkerType:
        return MarkerType.TEXT

    def __init__(self, layers, key: str):
        super(MarkerText, self).__init__(layers, key)
        self._text: str = "text"

    @property
    def text(self) -> str:
        return self._text


class MarkerTrajectory(MarkerAbs):

    @property
    def type(self) -> MarkerType:
        return MarkerType.TRAJECTORY

    def __init__(self, layers, key: str):
        super(MarkerTrajectory, self).__init__(layers, key)
        # TODO
        # self._points: List[Vector3] = None

    # @property
    # def points(self) -> List[Vector3]:
    #     return self._points


__all__ = [
    MarkerCube,
    MarkerSphere,
    MarkerCylinder,
    MarkerQuad,
    MarkerArrow,
    MarkerText,
    MarkerTrajectory,
]
