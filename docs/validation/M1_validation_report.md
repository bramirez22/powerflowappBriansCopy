# M1 Validation Report: Parser + Y-bus

## Scope

This report documents evidence for Milestone 1 objectives:

1. Working parser
2. Correct Y-bus construction
3. Validation using small test systems

## Per-Unit Assumptions

- Input branch parameters (`r`, `x`, `b`) are interpreted in per-unit.
- `mpc.baseMVA` is used when present; default is `100.0` if omitted.
- Bus shunts are stamped as `(Gs + jBs) / baseMVA` on Y-bus diagonal.

## Parser Evidence

Test file: `tests/parser/test_matpower_parser.py`

Validated behaviors:
- Parses valid IEEE-14 and 3-bus MATPOWER-style inputs.
- Raises clear errors for:
  - missing required matrix sections,
  - non-numeric rows,
  - insufficient bus-row columns.

## Y-bus Evidence

Test file: `tests/ybus/test_build_ybus.py`

### Case A: 3-bus symmetric network

Input: `data/raw/small_cases/case3_sample.m`

Expected series admittance per branch:
- `y = 1 / (0.1 + j0.2) = 2 - j4`

Expected matrix:

```text
[[ 4 - j8, -2 + j4, -2 + j4],
 [-2 + j4,  4 - j8, -2 + j4],
 [-2 + j4, -2 + j4,  4 - j8]]
```

### Case B: 2-bus with charging and tap

Input: `data/raw/small_cases/case2_tap_shunt_sample.m`

Parameters:
- `r = 0.1`, `x = 0.2`, `b = 0.04`, `tap = 1.1`, `angle = 0`
- `y_series = 1 / (r + jx) = 2 - j4`
- `y_shunt = j * (b/2) = j0.02`

Stamped values:
- `Y11 = (y_series + y_shunt) / |tap|^2`
- `Y22 = y_series + y_shunt`
- `Y12 = Y21 = -y_series / tap`

This directly validates both line charging and transformer tap handling.

## Test Results

Command:

```bash
.venv/bin/python -m pytest -q
```

Result:
- `11 passed`

Validation script command:

```bash
./scripts/run_m1_validation.sh
```

Result:
- Passes and prints computed 3-bus Y-bus matrix.

## Conclusion

Milestone 1 implementation and validation objectives are satisfied with automated tests and small-system reference cases.
