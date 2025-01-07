"""
This module has functionality to support running in
a distributeed context
"""

import os
import socket
import logging
from typing import Any

from pydantic import BaseModel


logger = logging.getLogger(__name__)


class ComputeProcess(BaseModel):
    """
    This represents a process on a compute device, such as a GPU or CPU
    """

    local_rank: int = 0
    device_name: str = "cpu"
    handle: Any | None = None


class NetworkAttributes(BaseModel):

    hostname: str = ""
    ip_address: str = ""


def read_network_attributes() -> NetworkAttributes:
    hostname = socket.gethostname()
    return NetworkAttributes(
        hostname=hostname, ip_address=socket.gethostbyname(hostname)
    )


class RuntimeContext(BaseModel):
    """
    This holds runtime information for the session, which is mostly
    useful in a distributed setting.
    """

    process: ComputeProcess
    network: NetworkAttributes
    node_id: int = 0
    num_nodes: int = 1
    gpus_per_node: int = 1

    @property
    def is_multigpu(self) -> bool:
        return self.gpus_per_node > 1

    @property
    def world_size(self) -> int:
        return self.gpus_per_node * self.num_nodes

    @property
    def global_rank(self) -> int:
        return self.node_id * self.gpus_per_node + self.process.local_rank

    @property
    def is_master_process(self) -> bool:
        """
        Return true if this process has zero global rank
        """
        return self.global_rank == 0


def load() -> RuntimeContext:
    return RuntimeContext(process=ComputeProcess(), network=read_network_attributes())


def get_slurm_info():
    return {
        "SLURM_LAUNCH_NODE_IPADDR": os.environ.get("SLURM_LAUNCH_NODE_IPADDR", ""),
        "SLURM_NPROCS": os.environ.get("SLURM_NPROCS", ""),  # world size
        "SLURM_PROCID": os.environ.get("SLURM_PROCID", ""),  # my rank
    }
