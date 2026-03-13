from __future__ import annotations

from pathlib import Path

import numpy as np

from src.parser import parse_matpower_case
from src.ybus import build_ybus


def test_build_ybus_for_case3_matches_reference() -> None:
    case_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "small_cases" / "case3_sample.m"
    case = parse_matpower_case(case_path)
    ybus = build_ybus(case)

    y = 1.0 / complex(0.1, 0.2)
    expected = np.array(
        [
            [2 * y, -y, -y],
            [-y, 2 * y, -y],
            [-y, -y, 2 * y],
        ],
        dtype=complex,
    )

    assert ybus.shape == (3, 3)
    assert np.allclose(ybus, expected, atol=1e-10)


def test_build_ybus_ieee14_shape() -> None:
    case_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "ieee14" / "case14_sample.m"
    case = parse_matpower_case(case_path)
    ybus = build_ybus(case)

    assert ybus.shape == (14, 14)
