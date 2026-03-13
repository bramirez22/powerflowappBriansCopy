# Milestone 1 Coding Best Practices

This guide defines how we write code for:

1. Working parser
2. Correct Y-bus construction
3. Validation with a small test system

## Core Principles

- Keep it simple: prefer clear logic over clever shortcuts.
- Avoid redundancy: one source of truth for each rule/calculation.
- Keep a consistent directory structure and naming style.
- Write testable functions with clear inputs/outputs.
- Separate data parsing, math logic, and reporting/output concerns.

## Recommended Directory Layout

```text
src/
  parser/
    matpower_parser.py
  models/
    schemas.py
  ybus/
    build_ybus.py
    admittance_utils.py
  validation/
    run_small_case_validation.py
tests/
  parser/
  ybus/
  validation/
data/
  raw/
    ieee14/
    small_cases/
```

## Simplicity Rules

- Use small functions that do one thing.
- Use explicit variable names (`from_bus`, `to_bus`, `tap_ratio`, `b_shunt`).
- Prefer straightforward loops/matrix operations over dense one-liners.
- Minimize hidden state; pass required values explicitly.

## No-Redundancy Rules

- Do not duplicate parser logic across files.
- Centralize per-unit conversion rules in one module.
- Centralize Y-bus element contribution formulas in one utility location.
- If code is copied twice, refactor it into a shared function.

## Parser Best Practices (M1 Objective i)

- Validate input early with clear error messages (line number + reason).
- Parse into typed/internal models before any network calculations.
- Handle missing/invalid fields explicitly; do not silently guess.
- Keep parser output deterministic and documented.

## Y-bus Best Practices (M1 Objective ii)

- Implement one canonical function to stamp each branch into Y-bus.
- Include:
  - Series admittance
  - Line charging susceptance
  - Transformer tap ratio effects
- Enforce matrix symmetry checks when applicable.
- Add assertions for shape and indexing correctness.

## Validation Best Practices (M1 Objective iii)

- Start with a very small hand-checkable system (e.g., 3-bus).
- Keep expected values in version-controlled fixtures.
- Compare computed vs expected with numeric tolerances.
- Add at least one negative test (bad input should fail cleanly).

## Code Review Checklist for M1

- [ ] Logic is clear and minimal.
- [ ] No duplicated parsing or admittance logic.
- [ ] Directory/module placement follows agreed layout.
- [ ] Parser errors are specific and actionable.
- [ ] Y-bus includes line charging and tap ratios.
- [ ] Small-system validation test passes.
- [ ] New behavior is covered by tests.
