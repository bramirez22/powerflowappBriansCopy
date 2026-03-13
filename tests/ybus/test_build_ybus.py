from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

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


def test_build_ybus_tap_and_line_charging_case2() -> None:
    case_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "raw"
        / "small_cases"
        / "case2_tap_shunt_sample.m"
    )
    case = parse_matpower_case(case_path)
    ybus = build_ybus(case)

    y_series = 1.0 / complex(0.1, 0.2)  # 2 - j4
    y_shunt = 1j * (0.04 / 2.0)  # j0.02 at each end
    tap = 1.1

    expected = np.array(
        [
            [(y_series + y_shunt) / (tap * tap), -y_series / tap],
            [-y_series / tap, y_series + y_shunt],
        ],
        dtype=complex,
    )

    assert ybus.shape == (2, 2)
    assert np.allclose(ybus, expected, atol=1e-10)


def test_build_ybus_ieee14_shape() -> None:
    case_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "ieee14" / "case14_sample.m"
    case = parse_matpower_case(case_path)
    ybus = build_ybus(case)

    assert ybus.shape == (14, 14)


def test_build_ybus_raises_for_unknown_bus_reference() -> None:
    case_path = Path(__file__).resolve().parents[1] / "fixtures" / "invalid_unknown_bus_reference.m"
    case = parse_matpower_case(case_path)

    with pytest.raises(ValueError, match=r"Branch references unknown bus"):
        build_ybus(case)
