import logging
from abc import ABC, abstractmethod
from threading import Semaphore

import socket
from typing import Optional, Dict

from dt_duckiematrix_messages.NetworkEndpoint import NetworkEndpoint, NetworkEndpointType
from dt_duckiematrix_messages.NetworkJoin import NetworkJoin
from dt_duckiematrix_messages.NetworkJoined import NetworkJoined
from dt_duckiematrix_protocols.commons.socket import \
    DuckieMatrixEngineDataSocket, \
    DuckieMatrixEngineControlSocket
from dt_duckiematrix_types import NetworkRole, EngineMode
from dt_duckiematrix_protocols.utils.communication import compile_topic, parse_topic


class ProtocolAbs(ABC):

    class ProtocolContext:

        def __init__(self, protocol: 'ProtocolAbs'):
            self._protocol = protocol
            self._counter = 0
            self._lock = Semaphore()

        def __enter__(self):
            with self._lock:
                self._counter += 1

        def __exit__(self, exc_type, exc_val, exc_tb):
            with self._lock:
                self._counter -= 1
                commit = self._counter == 0
            if commit:
                self._protocol.commit()

    def __init__(self, engine_hostname: str, group: str):
        self._logger = logging.getLogger(f"Protocol[{group}]")
        self._ctl_socket = DuckieMatrixEngineControlSocket(engine_hostname)
        self._group = group
        # join network
        endpoints = self._join_network()
        if endpoints is None:
            return
        # find data endpoints
        data_in_epoint = endpoints.get(NetworkEndpointType.DATA_IN.value, None)
        data_out_epoint = endpoints.get(NetworkEndpointType.DATA_OUT.value, None)
        data_in_uri = data_in_epoint.to_uri(engine_hostname) if data_in_epoint else None
        data_out_uri = data_out_epoint.to_uri(engine_hostname) if data_out_epoint else None
        # create underlying socket
        self._socket = DuckieMatrixEngineDataSocket(
            group,
            data_in_uri,
            data_out_uri
        )
        self._socket.start()
        # ---
        self._context = ProtocolAbs.ProtocolContext(self)

    def _join_network(self) -> Optional[Dict[str, NetworkEndpoint]]:
        topic, data = self._ctl_socket.request(
            compile_topic("network", "join"),
            NetworkJoin(
                role=NetworkRole.CLIENT,
                key=None,
                location=socket.gethostname(),
                group=self._group
            )
        )
        protocol, answer = parse_topic(topic)
        if protocol == "network":
            if answer == "joined":
                network_desc = NetworkJoined.from_bytes(data)
                # validate engine mode
                if not self.validate_engine_mode(network_desc.mode):
                    self._logger.error("The Engine you connected to is running in "
                                       f"{network_desc.mode.name} mode, but the protocol you "
                                       f"instantiated does not support it. You need to use "
                                       f"the correct protocol.")
                    return None
                # ---
                return network_desc.endpoints
            else:
                self._logger.error(f"The engine replied to 'network/join' with '{topic}'.")
        return None

    def session(self) -> ProtocolContext:
        return self._context

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def validate_engine_mode(self, mode: EngineMode) -> bool:
        pass
