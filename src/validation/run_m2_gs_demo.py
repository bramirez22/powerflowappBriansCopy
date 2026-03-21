"""Run a Milestone 2 GS convergence demonstration on IEEE-14 sample."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from src.parser import parse_matpower_case
from src.powerflow.gs import solve_gauss_seidel


def run_demo() -> None:
    case_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "ieee14" / "case14_sample.m"
    case = parse_matpower_case(case_path)

    result = solve_gauss_seidel(case, tolerance=1e-6, max_iterations=500)

    print(f"Converged: {result.converged}")
    print(f"Iterations: {result.iterations}")
    if result.history:
        last = result.history[-1]
        print(f"Final max |dV|: {last.max_voltage_change:.6e}")
        print(f"Final max mismatch: {last.max_power_mismatch:.6e}")

    print("Bus voltages (|V|, angle deg) for buses 1-5:")
    for i, v in enumerate(result.voltages[:5], start=1):
        print(f"Bus {i}: {abs(v):.6f}, {np.degrees(np.angle(v)):.6f}")


if __name__ == "__main__":
    run_demo()
