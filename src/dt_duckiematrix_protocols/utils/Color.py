import abc
from typing import Any

import numpy as np

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.utils.MonitoredObject import MonitoredObject


class Color(MonitoredObject):

    EMPTY_DICT = {}
    COLOR_ATTRS = ["r", "g", "b", "a"]

    def __init__(self, layers: LayerProtocol, key: str, auto_commit: bool = False, **kwargs):
        super().__init__(auto_commit)
        self._layers = layers
        self._key = key
        # ensure the layer struct is there
        self._make_layers()
        # update with given attrs
        with self.quiet():
            for k in self.COLOR_ATTRS:
                if k in kwargs:
                    self._set_property(k, kwargs[k])

    @abc.abstractmethod
    def _make_layers(self):
        pass

    @abc.abstractmethod
    def _get_property(self, field: str) -> float:
        pass

    @abc.abstractmethod
    def _set_property(self, field: str, value: Any):
        pass

    @property
    def r(self) -> float:
        return self._get_property("r")

    @r.setter
    def r(self, value):
        self._set_property("r", value)

    @property
    def g(self) -> float:
        return self._get_property("g")

    @g.setter
    def g(self, value):
        self._set_property("g", value)

    @property
    def b(self) -> float:
        return self._get_property("b")

    @b.setter
    def b(self, value):
        self._set_property("b", value)

    @property
    def a(self) -> float:
        return self._get_property("a")

    @a.setter
    def a(self, value):
        self._set_property("a", value)

    @staticmethod
    def _sanitize_float(field: str, value: Any) -> float:
        # make sure the value is YAML-serializable
        if value is not None:
            # float values
            if isinstance(value, float):
                pass
            # Numpy float values
            elif isinstance(value, (np.float32, np.float64)):
                value = float(value)
            # Numpy int values
            elif isinstance(value, (np.int8, np.int16, np.int32, np.int64, np.uint, int)):
                value = float(value) / 255.0
            # unknown value
            else:
                raise ValueError(f"You cannot set the property '{field}' to an object "
                                 f"of type '{type(value)}'")
        return value

    def __str__(self):
        return str({k: self._get_property(k) for k in self.COLOR_ATTRS})
