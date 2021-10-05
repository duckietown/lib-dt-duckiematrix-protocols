import dataclasses

from dt_duckiematrix_protocols import CBorMessage


@dataclasses.dataclass
class CameraFrame(CBorMessage):
    __empty__: str = ""
