"""Plot GS iteration-history CSV into a convergence PNG figure."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def load_history(csv_path: Path) -> tuple[list[int], list[float], list[float]]:
    iterations: list[int] = []
    max_dv: list[float] = []
    max_mismatch: list[float] = []

    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        expected = {"iteration", "max_voltage_change", "max_power_mismatch"}
        if reader.fieldnames is None or set(reader.fieldnames) != expected:
            raise ValueError(
                "Unexpected CSV columns. Expected: iteration,max_voltage_change,max_power_mismatch"
            )

        for row in reader:
            iterations.append(int(row["iteration"]))
            max_dv.append(float(row["max_voltage_change"]))
            max_mismatch.append(float(row["max_power_mismatch"]))

    if not iterations:
        raise ValueError("CSV has no iteration rows")

    return iterations, max_dv, max_mismatch


def plot_history(csv_path: Path, output_path: Path, title: str = "M2 GS Convergence") -> Path:
    iterations, max_dv, max_mismatch = load_history(csv_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.semilogy(iterations, max_dv, marker="o", label="max |dV|")
    plt.semilogy(iterations, max_mismatch, marker="s", label="max mismatch")
    plt.xlabel("Iteration")
    plt.ylabel("Magnitude (log scale)")
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()

    return output_path


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plot M2 GS iteration history CSV")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("docs/validation/m2_gs_iteration_history.csv"),
        help="Path to iteration-history CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/validation/m2_gs_convergence.png"),
        help="Path to output PNG",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="M2 GS Convergence",
        help="Figure title",
    )
    return parser


if __name__ == "__main__":
    args = _build_arg_parser().parse_args()
    png_path = plot_history(args.input, args.output, title=args.title)
    print(f"Convergence plot written: {png_path}")
