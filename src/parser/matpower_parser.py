"""Parser for MATPOWER-style plain-text case files used in M1."""

from __future__ import annotations

import re
from pathlib import Path

from src.models import Branch, Bus, Generator, PowerSystemCase


def parse_matpower_case(file_path: str | Path) -> PowerSystemCase:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")

    base_mva = _parse_base_mva(text)
    bus_rows = _extract_matrix_rows(text, "bus")
    gen_rows = _extract_matrix_rows(text, "gen")
    branch_rows = _extract_matrix_rows(text, "branch")

    buses = [_row_to_bus(row, idx) for idx, row in enumerate(bus_rows, start=1)]
    generators = [_row_to_generator(row, idx) for idx, row in enumerate(gen_rows, start=1)]
    branches = [_row_to_branch(row, idx) for idx, row in enumerate(branch_rows, start=1)]

    return PowerSystemCase(
        base_mva=base_mva,
        buses=buses,
        generators=generators,
        branches=branches,
    )


def _parse_base_mva(text: str) -> float:
    match = re.search(r"mpc\.baseMVA\s*=\s*([0-9]*\.?[0-9]+)\s*;", text)
    if not match:
        return 100.0
    return float(match.group(1))


def _extract_matrix_rows(text: str, section: str) -> list[list[float]]:
    pattern = rf"mpc\.{section}\s*=\s*\[(.*?)\];"
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Missing required section: mpc.{section}")

    block = match.group(1)
    rows: list[list[float]] = []
    for line_no, raw_line in enumerate(block.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        line = line.split("%", maxsplit=1)[0].strip()
        if not line:
            continue
        if line.endswith(";"):
            line = line[:-1].strip()
        if not line:
            continue

        try:
            values = [float(token) for token in line.split()]
        except ValueError as exc:
            raise ValueError(
                f"Could not parse numeric row in mpc.{section} at block line {line_no}: {raw_line}"
            ) from exc
        rows.append(values)

    if not rows:
        raise ValueError(f"Section mpc.{section} is empty")
    return rows


def _row_to_bus(row: list[float], idx: int) -> Bus:
    if len(row) < 13:
        raise ValueError(f"Bus row {idx} has {len(row)} columns; expected >= 13")
    return Bus(
        bus_i=int(row[0]),
        bus_type=int(row[1]),
        pd=row[2],
        qd=row[3],
        gs=row[4],
        bs=row[5],
        area=int(row[6]),
        vm=row[7],
        va=row[8],
        base_kv=row[9],
        zone=int(row[10]),
        vmax=row[11],
        vmin=row[12],
    )


def _row_to_generator(row: list[float], idx: int) -> Generator:
    if len(row) < 10:
        raise ValueError(f"Generator row {idx} has {len(row)} columns; expected >= 10")
    return Generator(
        bus=int(row[0]),
        pg=row[1],
        qg=row[2],
        qmax=row[3],
        qmin=row[4],
        vg=row[5],
        mbase=row[6],
        status=int(row[7]),
        pmax=row[8],
        pmin=row[9],
    )


def _row_to_branch(row: list[float], idx: int) -> Branch:
    if len(row) < 13:
        raise ValueError(f"Branch row {idx} has {len(row)} columns; expected >= 13")
    return Branch(
        fbus=int(row[0]),
        tbus=int(row[1]),
        r=row[2],
        x=row[3],
        b=row[4],
        ratio=row[8],
        angle=row[9],
        status=int(row[10]),
    )
