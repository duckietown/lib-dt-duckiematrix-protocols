from typing import Optional, Dict

from dt_duckiematrix_protocols.commons.LayerProtocol import LayerProtocol
from dt_duckiematrix_protocols.commons.ProtocolAbs import ProtocolAbs
from dt_duckiematrix_protocols.viewer.MarkersManager import MarkersManager
from dt_duckiematrix_protocols.viewer.markers import MarkerAbs


class ViewerProtocol(LayerProtocol):

    # TODO: make the LayerProtocol object, do not inherit from it so that you don't expose those APIs

    def __init__(self, engine_hostname: str, auto_commit: bool = True):
        super(ViewerProtocol, self).__init__(engine_hostname, auto_commit)
        self.markers = MarkersManager(self, auto_commit)
