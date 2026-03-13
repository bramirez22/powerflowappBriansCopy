from __future__ import annotations

from pathlib import Path

import numpy as np

from src.validation.run_small_case_validation import expected_three_bus_ybus


def test_expected_three_bus_ybus_matrix_values() -> None:
    y = expected_three_bus_ybus()
    assert y.shape == (3, 3)

    reference = 1.0 / complex(0.1, 0.2)
    assert np.isclose(y[0, 0], 2 * reference)
    assert np.isclose(y[0, 1], -reference)
    assert np.isclose(y[1, 2], -reference)


def test_small_case_file_exists() -> None:
    case_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "small_cases" / "case3_sample.m"
    assert case_path.exists()
