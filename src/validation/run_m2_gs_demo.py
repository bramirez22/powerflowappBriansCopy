"""Run a Milestone 2 GS convergence demonstration on IEEE-14 sample."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from src.parser import parse_matpower_case
from src.powerflow.gs import GSIterationRecord, GSResult, solve_gauss_seidel


def write_iteration_history_csv(history: list[GSIterationRecord], output_path: Path) -> None:
    """Write GS iteration history to CSV for plotting/reporting."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["iteration", "max_voltage_change", "max_power_mismatch"])
        for row in history:
            writer.writerow([
                row.iteration,
                f"{row.max_voltage_change:.12e}",
                f"{row.max_power_mismatch:.12e}",
            ])


def run_demo(
    tolerance: float = 1e-6,
    max_iterations: int = 500,
    case_path: Path | None = None,
    output_path: Path | None = None,
) -> GSResult:
    case_file = case_path or (Path(__file__).resolve().parents[2] / "data" / "raw" / "ieee14" / "case14_sample.m")
    output_file = output_path or (Path(__file__).resolve().parents[2] / "docs" / "validation" / "m2_gs_iteration_history.csv")

    case = parse_matpower_case(case_file)
    result = solve_gauss_seidel(case, tolerance=tolerance, max_iterations=max_iterations)

    print(f"Converged: {result.converged}")
    print(f"Iterations: {result.iterations}")
    if result.history:
        last = result.history[-1]
        print(f"Final max |dV|: {last.max_voltage_change:.6e}")
        print(f"Final max mismatch: {last.max_power_mismatch:.6e}")

    print("Bus voltages (|V|, angle deg) for buses 1-5:")
    for i, v in enumerate(result.voltages[:5], start=1):
        print(f"Bus {i}: {abs(v):.6f}, {np.degrees(np.angle(v)):.6f}")

    write_iteration_history_csv(result.history, output_file)
    print(f"Iteration history CSV written: {output_file}")

    return result


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run GS demo and export iteration history CSV")
    parser.add_argument("--tolerance", type=float, default=1e-6)
    parser.add_argument("--max-iterations", type=int, default=500)
    parser.add_argument("--case", type=Path, default=None, help="Path to MATPOWER-style case file")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Path to write iteration-history CSV",
    )
    return parser


if __name__ == "__main__":
    args = _build_arg_parser().parse_args()
    run_demo(
        tolerance=args.tolerance,
        max_iterations=args.max_iterations,
        case_path=args.case,
        output_path=args.output,
    )
