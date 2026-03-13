# M1 Parser + Y-bus Checklist (Week 8, 10%)

- [x] Plain-text parser supports bus/branch/generator data.
- [x] Per-unit normalization rules documented.
- [x] Y-bus includes line charging susceptance.
- [x] Y-bus includes transformer tap ratios.
- [x] Small-system validation case added with expected result.

## Evidence Links

- Parser: `src/parser/matpower_parser.py`
- Y-bus: `src/ybus/build_ybus.py`
- Tests: `tests/parser/test_matpower_parser.py`, `tests/ybus/test_build_ybus.py`
- Validation report: `docs/validation/M1_validation_report.md`
- Sample inputs: `data/raw/small_cases/`
