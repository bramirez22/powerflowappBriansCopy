"""Core data structures for parser and network-model layers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Bus:
    bus_i: int
    bus_type: int
    pd: float
    qd: float
    gs: float
    bs: float
    area: int
    vm: float
    va: float
    base_kv: float
    zone: int
    vmax: float
    vmin: float


@dataclass(frozen=True)
class Generator:
    bus: int
    pg: float
    qg: float
    qmax: float
    qmin: float
    vg: float
    mbase: float
    status: int
    pmax: float
    pmin: float


@dataclass(frozen=True)
class Branch:
    fbus: int
    tbus: int
    r: float
    x: float
    b: float
    ratio: float
    angle: float
    status: int


@dataclass(frozen=True)
class PowerSystemCase:
    base_mva: float
    buses: list[Bus]
    generators: list[Generator]
    branches: list[Branch]
