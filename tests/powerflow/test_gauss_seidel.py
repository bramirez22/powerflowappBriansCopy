from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from src.parser import parse_matpower_case
from src.powerflow.gs import solve_gauss_seidel


def test_gs_converges_on_zero_load_case3() -> None:
    case_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "small_cases" / "case3_sample.m"
    case = parse_matpower_case(case_path)

    result = solve_gauss_seidel(case, tolerance=1e-10, max_iterations=30)

    assert result.converged
    assert result.iterations >= 1
    assert len(result.history) == result.iterations

    # Slack bus (bus 1 in this case) should remain at initial value 1.0 + j0.0
    assert np.isclose(result.voltages[0].real, 1.0, atol=1e-12)
    assert np.isclose(result.voltages[0].imag, 0.0, atol=1e-12)


def test_gs_handles_slack_pv_pq_and_converges() -> None:
    case_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "raw"
        / "small_cases"
        / "case3_gs_pv_sample.m"
    )
    case = parse_matpower_case(case_path)

    result = solve_gauss_seidel(case, tolerance=1e-6, max_iterations=200)

    assert result.converged
    assert len(result.history) == result.iterations

    # Bus 2 is PV with specified |V| = 1.02.
    assert np.isclose(abs(result.voltages[1]), 1.02, atol=2e-3)


def test_gs_rejects_invalid_solver_parameters() -> None:
    case_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "small_cases" / "case3_sample.m"
    case = parse_matpower_case(case_path)

    with pytest.raises(ValueError, match="tolerance must be positive"):
        solve_gauss_seidel(case, tolerance=0.0, max_iterations=10)

    with pytest.raises(ValueError, match="max_iterations must be positive"):
        solve_gauss_seidel(case, tolerance=1e-6, max_iterations=0)
