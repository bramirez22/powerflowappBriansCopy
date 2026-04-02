"""Newton-Raphson power-flow solver scaffold."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from src.models import PowerSystemCase
from src.ybus import build_ybus

BUS_TYPE_PQ = 1
BUS_TYPE_PV = 2
BUS_TYPE_SLACK = 3


@dataclass(frozen=True)
class NRIterationRecord:
    iteration: int
    max_voltage_change: float
    max_power_mismatch: float


@dataclass(frozen=True)
class NRResult:
    voltages: np.ndarray
    converged: bool
    iterations: int
    history: list[NRIterationRecord]


def solve_newton_raphson(
    case: PowerSystemCase,
    tolerance: float = 1e-6,
    max_iterations: int = 50,
) -> NRResult:
    """Solve power flow using a Newton-Raphson method with slack, PV, and PQ buses."""
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")

    ybus = build_ybus(case)
    p_spec, q_spec = _build_specified_power_injections(case)
    v = _build_initial_voltages(case)
    bus_types = _build_bus_type_array(case)
    angle_state_buses, pq_state_buses = _get_state_bus_indices(bus_types)
    v_target_mag = np.abs(v).astype(float)

    history: list[NRIterationRecord] = []

    for it in range(1, max_iterations + 1):
        v_prev = v.copy()
        mismatch = _build_power_mismatch(ybus, v, p_spec, q_spec, bus_types)

        if mismatch.size == 0:
            return NRResult(
                voltages=v,
                converged=True,
                iterations=0,
                history=history,
            )

        max_mismatch = _compute_max_power_mismatch(ybus, v, p_spec, q_spec, bus_types)
        if max_mismatch < tolerance:
            history.append(
                NRIterationRecord(
                    iteration=it,
                    max_voltage_change=0.0,
                    max_power_mismatch=max_mismatch,
                )
            )
            return NRResult(
                voltages=v,
                converged=True,
                iterations=it,
                history=history,
            )

        if len(angle_state_buses) + len(pq_state_buses) == 0:
            return NRResult(
                voltages=v,
                converged=False,
                iterations=0,
                history=history,
            )

        jacobian = _build_jacobian(
            ybus,
            v,
            bus_types,
            angle_state_buses,
            pq_state_buses,
        )

        try:
            delta_x = np.linalg.solve(jacobian, mismatch)
        except np.linalg.LinAlgError as exc:
            raise ValueError(
                "Jacobian is singular; Newton-Raphson cannot proceed"
            ) from exc

        v = _apply_state_update(v, delta_x, bus_types, v_target_mag)
        max_dv = _compute_max_voltage_change(v, v_prev)
        max_mismatch = _compute_max_power_mismatch(ybus, v, p_spec, q_spec, bus_types)

        history.append(
            NRIterationRecord(
                iteration=it,
                max_voltage_change=max_dv,
                max_power_mismatch=max_mismatch,
            )
        )

        if max_mismatch < tolerance:
            return NRResult(
                voltages=v,
                converged=True,
                iterations=it,
                history=history,
            )

    return NRResult(
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


def _build_initial_voltages(case: PowerSystemCase) -> np.ndarray:
    """Build the initial complex voltage vector from bus magnitudes and angles."""
    return np.array(
        [
            bus.vm * np.exp(1j * np.radians(bus.va))
            for bus in case.buses
        ],
        dtype=complex,
    )


def _build_bus_type_array(case: PowerSystemCase) -> np.ndarray:
    """Return bus types as an integer array for slack, PV, and PQ handling."""
    return np.array([bus.bus_type for bus in case.buses], dtype=int)


def _get_state_bus_indices(bus_types: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return angle-state bus indices and magnitude-state bus indices."""
    angle_state_buses = np.array(
        [
            idx
            for idx, btype in enumerate(bus_types)
            if btype in (BUS_TYPE_PQ, BUS_TYPE_PV)
        ],
        dtype=int,
    )
    pq_state_buses = np.array(
        [
            idx
            for idx, btype in enumerate(bus_types)
            if btype == BUS_TYPE_PQ
        ],
        dtype=int,
    )
    return angle_state_buses, pq_state_buses


def _compute_power_injections(ybus: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Compute active and reactive power injections implied by the current voltages."""
    s_calc = v * np.conj(ybus @ v)
    p_calc = np.array(s_calc.real, dtype=float)
    q_calc = np.array(s_calc.imag, dtype=float)
    return p_calc, q_calc


def _build_power_mismatch(
    ybus: np.ndarray,
    v: np.ndarray,
    p_spec: np.ndarray,
    q_spec: np.ndarray,
    bus_types: np.ndarray,
) -> np.ndarray:
    """Build the Newton-Raphson mismatch vector for PV and PQ buses."""
    p_calc, q_calc = _compute_power_injections(ybus, v)

    residuals: list[float] = []
    for i, btype in enumerate(bus_types):
        if btype in (BUS_TYPE_PQ, BUS_TYPE_PV):
            residuals.append(p_spec[i] - p_calc[i])
    for i, btype in enumerate(bus_types):
        if btype == BUS_TYPE_PQ:
            residuals.append(q_spec[i] - q_calc[i])

    return np.array(residuals, dtype=float)


def _build_jacobian(
    ybus: np.ndarray,
    v: np.ndarray,
    bus_types: np.ndarray,
    angle_state_buses: np.ndarray,
    pq_state_buses: np.ndarray,
) -> np.ndarray:
    """Build the reduced Newton-Raphson Jacobian for the current operating point."""
    del bus_types

    vm = np.abs(v)
    va = np.angle(v)
    p_calc, q_calc = _compute_power_injections(ybus, v)

    n_angle = len(angle_state_buses)
    n_pq = len(pq_state_buses)

    h = np.zeros((n_angle, n_angle), dtype=float)
    n = np.zeros((n_angle, n_pq), dtype=float)
    m = np.zeros((n_pq, n_angle), dtype=float)
    l = np.zeros((n_pq, n_pq), dtype=float)

    for row, i in enumerate(angle_state_buses):
        vi = vm[i]
        for col, k in enumerate(angle_state_buses):
            if i == k:
                h[row, col] = -q_calc[i] - ybus[i, i].imag * vi * vi
            else:
                vk = vm[k]
                theta_ik = va[i] - va[k]
                gik = ybus[i, k].real
                bik = ybus[i, k].imag
                h[row, col] = vi * vk * (
                    gik * np.sin(theta_ik) - bik * np.cos(theta_ik)
                )

        for col, k in enumerate(pq_state_buses):
            if i == k:
                n[row, col] = p_calc[i] / vi + ybus[i, i].real * vi
            else:
                theta_ik = va[i] - va[k]
                gik = ybus[i, k].real
                bik = ybus[i, k].imag
                n[row, col] = vi * (
                    gik * np.cos(theta_ik) + bik * np.sin(theta_ik)
                )

    for row, i in enumerate(pq_state_buses):
        vi = vm[i]
        for col, k in enumerate(angle_state_buses):
            if i == k:
                m[row, col] = p_calc[i] - ybus[i, i].real * vi * vi
            else:
                vk = vm[k]
                theta_ik = va[i] - va[k]
                gik = ybus[i, k].real
                bik = ybus[i, k].imag
                m[row, col] = -vi * vk * (
                    gik * np.cos(theta_ik) + bik * np.sin(theta_ik)
                )

        for col, k in enumerate(pq_state_buses):
            if i == k:
                l[row, col] = q_calc[i] / vi - ybus[i, i].imag * vi
            else:
                theta_ik = va[i] - va[k]
                gik = ybus[i, k].real
                bik = ybus[i, k].imag
                l[row, col] = vi * (
                    gik * np.sin(theta_ik) - bik * np.cos(theta_ik)
                )

    top = np.hstack((h, n))
    bottom = np.hstack((m, l))
    return np.vstack((top, bottom))


def _apply_state_update(
    v: np.ndarray,
    delta_x: np.ndarray,
    bus_types: np.ndarray,
    v_target_mag: np.ndarray,
) -> np.ndarray:
    """Apply a Newton-Raphson state update to bus angles and PQ-bus magnitudes."""
    angle_state_buses, pq_state_buses = _get_state_bus_indices(bus_types)

    n_angle = len(angle_state_buses)
    angle_updates = delta_x[:n_angle]
    magnitude_updates = delta_x[n_angle:]

    vm = np.abs(v).astype(float)
    va = np.angle(v).astype(float)

    for idx, bus_idx in enumerate(angle_state_buses):
        va[bus_idx] += angle_updates[idx]

    for idx, bus_idx in enumerate(pq_state_buses):
        vm[bus_idx] += magnitude_updates[idx]

    for i, btype in enumerate(bus_types):
        if btype == BUS_TYPE_PV:
            vm[i] = v_target_mag[i]
        elif btype == BUS_TYPE_SLACK:
            vm[i] = abs(v[i])
            va[i] = np.angle(v[i])

    return vm * np.exp(1j * va)


def _compute_max_voltage_change(v: np.ndarray, v_prev: np.ndarray) -> float:
    """Compute the maximum complex voltage change between successive iterations."""
    return float(np.max(np.abs(v - v_prev)))


def _compute_max_power_mismatch(
    ybus: np.ndarray,
    v: np.ndarray,
    p_spec: np.ndarray,
    q_spec: np.ndarray,
    bus_types: np.ndarray,
) -> float:
    """Compute max mismatch for NR reporting (P for PV/PQ, Q for PQ)."""
    mismatch = _build_power_mismatch(ybus, v, p_spec, q_spec, bus_types)
    if mismatch.size == 0:
        return 0.0
    return float(np.max(np.abs(mismatch)))