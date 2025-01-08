from bsb import Simulation, config, types

from .cell import NestCell
from .connection import NestConnection
from .device import NestDevice


@config.node
class NestSimulation(Simulation):
    """
    Interface between the scaffold model and the NEST simulator.
    """

    modules = config.list(type=str)
    """List of NEST modules to load at the beginning of the simulation"""
    threads = config.attr(type=types.int(min=1), default=1)
    """Number of threads to use during simulation"""
    resolution = config.attr(type=types.float(min=0.0), required=True)
    """Simulation time step size in milliseconds"""
    verbosity = config.attr(type=str, default="M_ERROR")
    """NEST verbosity level"""
    seed = config.attr(type=int, default=None)
    """Random seed for the simulations"""

    cell_models = config.dict(type=NestCell, required=True)
    connection_models = config.dict(type=NestConnection, required=True)
    devices = config.dict(type=NestDevice, required=True)
