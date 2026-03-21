"""Gauss-Seidel power-flow solver for Milestone 2."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.models import PowerSystemCase
from src.ybus import build_ybus

BUS_TYPE_PQ = 1
BUS_TYPE_PV = 2
BUS_TYPE_SLACK = 3


@dataclass(frozen=True)
class GSIterationRecord:
    iteration: int
    max_voltage_change: float
    max_power_mismatch: float


@dataclass(frozen=True)
class GSResult:
    voltages: np.ndarray
    converged: bool
    iterations: int
    history: list[GSIterationRecord]


def solve_gauss_seidel(
    case: PowerSystemCase,
    tolerance: float = 1e-6,
    max_iterations: int = 200,
) -> GSResult:
    """Solve power flow using complex-form Gauss-Seidel iteration."""
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")

    ybus = build_ybus(case)
    nbus = len(case.buses)
    p_spec, q_spec = _build_specified_power_injections(case)

    v = np.array(
        [
            bus.vm * np.exp(1j * np.radians(bus.va))
            for bus in case.buses
        ],
        dtype=complex,
    )
    v_target_mag = np.array([bus.vm for bus in case.buses], dtype=float)
    bus_types = np.array([bus.bus_type for bus in case.buses], dtype=int)

    history: list[GSIterationRecord] = []

    for it in range(1, max_iterations + 1):
        v_prev = v.copy()

        for i in range(nbus):
            btype = bus_types[i]
            if btype == BUS_TYPE_SLACK:
                continue

            yii = ybus[i, i]
            if abs(yii) < 1e-14:
                raise ValueError(f"Ybus diagonal entry is zero at bus index {i}")

            yv_sum = ybus[i, :] @ v
            sum_except_i = yv_sum - yii * v[i]

            if btype == BUS_TYPE_PV:
                s_calc = v[i] * np.conj(yv_sum)
                q_est = float(s_calc.imag)
                v_temp = ((p_spec[i] - 1j * q_est) / np.conj(v[i]) - sum_except_i) / yii
                v[i] = v_target_mag[i] * np.exp(1j * np.angle(v_temp))
            elif btype == BUS_TYPE_PQ:
                v[i] = ((p_spec[i] - 1j * q_spec[i]) / np.conj(v[i]) - sum_except_i) / yii
            else:
                raise ValueError(f"Unsupported bus type {btype} at bus index {i}")

        max_dv = float(np.max(np.abs(v - v_prev)))
        max_mismatch = _compute_max_power_mismatch(ybus, v, p_spec, q_spec, bus_types)

        history.append(
            GSIterationRecord(
                iteration=it,
                max_voltage_change=max_dv,
                max_power_mismatch=max_mismatch,
            )
        )

        if max(max_dv, max_mismatch) < tolerance:
            return GSResult(
                voltages=v,
                converged=True,
                iterations=it,
                history=history,
            )

    return GSResult(
        voltages=v,
        converged=False,
        iterations=max_iterations,
        history=history,
    )


def _build_specified_power_injections(case: PowerSystemCase) -> tuple[np.ndarray, np.ndarray]:
    """Return net specified P and Q injections in per-unit (generation - load)."""
    bus_to_idx = {bus.bus_i: idx for idx, bus in enumerate(case.buses)}
    nbus = len(case.buses)

    p = np.zeros(nbus, dtype=float)
    q = np.zeros(nbus, dtype=float)

    for bus in case.buses:
        idx = bus_to_idx[bus.bus_i]
        p[idx] -= bus.pd / case.base_mva
        q[idx] -= bus.qd / case.base_mva

    for gen in case.generators:
        if gen.status == 0:
            continue
        if gen.bus not in bus_to_idx:
            raise ValueError(f"Generator references unknown bus {gen.bus}")
        idx = bus_to_idx[gen.bus]
        p[idx] += gen.pg / case.base_mva
        q[idx] += gen.qg / case.base_mva

    return p, q


def _compute_max_power_mismatch(
    ybus: np.ndarray,
    v: np.ndarray,
    p_spec: np.ndarray,
    q_spec: np.ndarray,
    bus_types: np.ndarray,
) -> float:
    """Compute max mismatch for GS reporting (P for PV/PQ, Q for PQ)."""
    s_calc = v * np.conj(ybus @ v)
    p_calc = s_calc.real
    q_calc = s_calc.imag

    residuals: list[float] = []
    for i, btype in enumerate(bus_types):
        if btype in (BUS_TYPE_PQ, BUS_TYPE_PV):
            residuals.append(abs(p_spec[i] - p_calc[i]))
        if btype == BUS_TYPE_PQ:
            residuals.append(abs(q_spec[i] - q_calc[i]))

    if not residuals:
        return 0.0
    return float(max(residuals))
