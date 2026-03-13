"""Run a simple M1 validation on a 3-bus sample case."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from src.parser import parse_matpower_case
from src.ybus import build_ybus


def expected_three_bus_ybus() -> np.ndarray:
    y = 1.0 / complex(0.1, 0.2)
    diag = 2.0 * y
    off = -y
    return np.array(
        [
            [diag, off, off],
            [off, diag, off],
            [off, off, diag],
        ],
        dtype=complex,
    )


def run_validation(case_path: Path) -> None:
    case = parse_matpower_case(case_path)
    ybus = build_ybus(case)
    expected = expected_three_bus_ybus()

    if not np.allclose(ybus, expected, atol=1e-10):
        raise SystemExit("Validation failed: computed Y-bus does not match expected 3-bus reference.")

    print("Validation passed for 3-bus sample case.")
    print("Computed Y-bus:")
    print(ybus)


if __name__ == "__main__":
    default_case = Path(__file__).resolve().parents[2] / "data" / "raw" / "small_cases" / "case3_sample.m"
    run_validation(default_case)
