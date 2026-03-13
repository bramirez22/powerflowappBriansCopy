"""Y-bus matrix formation for the parsed power-system case."""

from __future__ import annotations

import numpy as np

from src.models import PowerSystemCase
from src.ybus.admittance_utils import series_admittance, tap_complex


def build_ybus(case: PowerSystemCase) -> np.ndarray:
    bus_numbers = [bus.bus_i for bus in case.buses]
    bus_index = {bus_i: idx for idx, bus_i in enumerate(bus_numbers)}
    nbus = len(case.buses)
    ybus = np.zeros((nbus, nbus), dtype=complex)

    for bus in case.buses:
        i = bus_index[bus.bus_i]
        ybus[i, i] += complex(bus.gs, bus.bs) / case.base_mva

    for branch in case.branches:
        if branch.status == 0:
            continue

        if branch.fbus not in bus_index or branch.tbus not in bus_index:
            raise ValueError(f"Branch references unknown bus: {branch.fbus} -> {branch.tbus}")

        i = bus_index[branch.fbus]
        j = bus_index[branch.tbus]

        y_series = series_admittance(branch.r, branch.x)
        y_shunt = 1j * (branch.b / 2.0)
        tap = tap_complex(branch.ratio, branch.angle)

        ybus[i, i] += (y_series + y_shunt) / (tap * tap.conjugate())
        ybus[j, j] += y_series + y_shunt
        ybus[i, j] -= y_series / tap.conjugate()
        ybus[j, i] -= y_series / tap

    return ybus
