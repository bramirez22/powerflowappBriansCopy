from __future__ import annotations

from pathlib import Path

import pytest

from src.parser import parse_matpower_case


def test_parse_case3_counts() -> None:
    case_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "small_cases" / "case3_sample.m"
    case = parse_matpower_case(case_path)

    assert len(case.buses) == 3
    assert len(case.generators) == 1
    assert len(case.branches) == 3


def test_parse_ieee14_counts() -> None:
    case_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "ieee14" / "case14_sample.m"
    case = parse_matpower_case(case_path)

    assert len(case.buses) == 14
    assert len(case.generators) == 5
    assert len(case.branches) == 20


def test_parse_missing_branch_section_raises() -> None:
    case_path = Path(__file__).resolve().parents[1] / "fixtures" / "invalid_missing_branch.m"
    with pytest.raises(ValueError, match=r"Missing required section: mpc\.branch"):
        parse_matpower_case(case_path)


def test_parse_bad_numeric_row_raises() -> None:
    case_path = Path(__file__).resolve().parents[1] / "fixtures" / "invalid_bad_numeric.m"
    with pytest.raises(ValueError, match=r"Could not parse numeric row in mpc\.bus"):
        parse_matpower_case(case_path)


def test_parse_short_bus_row_raises() -> None:
    case_path = Path(__file__).resolve().parents[1] / "fixtures" / "invalid_short_bus_row.m"
    with pytest.raises(ValueError, match=r"Bus row 1 has 10 columns; expected >= 13"):
        parse_matpower_case(case_path)
