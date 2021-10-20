from typing import Any, Optional

import numpy as np

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.utils.MonitoredObject import MonitoredObject

BUILTIN_TYPES = (
    int,
    float,
    bool,
    str,
    list,
    tuple,
    dict,
    set,
    frozenset,
)


class Pose3D(MonitoredObject):

    EMPTY_DICT = {}
    POSE_ATTRS = ["x", "y", "z", "roll", "pitch", "yaw"]

    def __init__(self, layers: LayerProtocol, key: str, auto_commit: bool = False, **kwargs):
        super(Pose3D, self).__init__(auto_commit)
        self._layers = layers
        self._key = key
        # make frame if it does not exist
        if not self._layers.has("frames", self._key):
            self._layers.update("frames", self._key, {
                "relative_to": None,
                "pose": {k: 0.0 for k in self.POSE_ATTRS}
            })
        # update with given attrs
        if "relative_to" in kwargs:
            self.relative_to = kwargs["relative_to"]
        with self.quiet():
            for k in self.POSE_ATTRS:
                if k in kwargs:
                    self._set_property(k, kwargs[k])

    def _get_property(self, field: str) -> float:
        return self._layers.get("frames", self._key).get("pose").get(field, None)

    def _set_property(self, field: str, value: Any):
        # make sure the value is YAML-serializable
        if value is not None and value.__class__ not in BUILTIN_TYPES:
            # Numpy float values
            if isinstance(value, (np.float32, np.float64)):
                value = float(value)
            # Numpy int values
            elif isinstance(value, (np.int8, np.int16, np.int32, np.int64, np.uint)):
                value = int(value)
            # unknown value
            else:
                self._layers.logger.error(f"You cannot set the property '{field}' to an object "
                                          f"of type '{type(value)}'")
                return
        pose = self._layers.get("frames", self._key)
        pose["pose"][field] = value
        if self._auto_commit:
            self._commit()

    def _commit(self):
        pose = self._layers.get("frames", self._key)
        self._layers.update("frames", self._key, pose)

    @property
    def x(self) -> float:
        return self._get_property("x")

    @x.setter
    def x(self, value):
        self._set_property("x", value)

    @property
    def y(self) -> float:
        return self._get_property("y")

    @y.setter
    def y(self, value):
        self._set_property("y", value)

    @property
    def z(self) -> float:
        return self._get_property("z")

    @z.setter
    def z(self, value):
        self._set_property("z", value)

    @property
    def roll(self) -> float:
        return self._get_property("roll")

    @roll.setter
    def roll(self, value):
        self._set_property("roll", value)

    @property
    def pitch(self) -> float:
        return self._get_property("pitch")

    @pitch.setter
    def pitch(self, value):
        self._set_property("pitch", value)

    @property
    def yaw(self) -> float:
        return self._get_property("yaw")

    @yaw.setter
    def yaw(self, value):
        self._set_property("yaw", value)

    @property
    def relative_to(self) -> Optional[str]:
        return self._layers.get("frames", self._key).get("relative_to")

    @relative_to.setter
    def relative_to(self, value):
        self._layers.get("frames", self._key)["relative_to"] = value

    def __str__(self):
        return str({
            "relative_to": self.relative_to,
            "pose": {k: self._get_property(k) for k in self.POSE_ATTRS}
        })
