from __future__ import annotations

from pathlib import Path

from src.validation.run_m2_gs_demo import run_demo, write_iteration_history_csv
from src.powerflow.gs import GSIterationRecord


def test_write_iteration_history_csv_writes_header_and_rows(tmp_path: Path) -> None:
    output = tmp_path / "history.csv"
    rows = [
        GSIterationRecord(iteration=1, max_voltage_change=1.2e-2, max_power_mismatch=3.4e-2),
        GSIterationRecord(iteration=2, max_voltage_change=5.6e-3, max_power_mismatch=7.8e-3),
    ]

    write_iteration_history_csv(rows, output)

    text = output.read_text(encoding="utf-8").strip().splitlines()
    assert text[0] == "iteration,max_voltage_change,max_power_mismatch"
    assert text[1].startswith("1,")
    assert text[2].startswith("2,")


def test_run_demo_creates_csv(tmp_path: Path) -> None:
    case_path = Path(__file__).resolve().parents[2] / "data" / "raw" / "small_cases" / "case3_sample.m"
    output = tmp_path / "m2_demo_history.csv"

    result = run_demo(
        tolerance=1e-10,
        max_iterations=50,
        case_path=case_path,
        output_path=output,
    )

    assert output.exists()
    line_count = len(output.read_text(encoding="utf-8").strip().splitlines())
    assert line_count == result.iterations + 1
