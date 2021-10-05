import dataclasses

from dt_duckiematrix_protocols import CBorMessage


@dataclasses.dataclass
class EmptyMessage(CBorMessage):
    __empty__: str = ""
