from __future__ import annotations

from pathlib import Path

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
