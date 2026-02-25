# Contributing Guide

## Branching

- Branch from `main`.
- Naming:
  - `feature/<name>` for new functionality
  - `fix/<name>` for bug fixes
  - `docs/<name>` for documentation-only changes

## Commits

Use clear, imperative commit messages.

Examples:
- `Add Newton-Raphson mismatch calculation`
- `Fix slack bus voltage initialization`
- `Document test case assumptions`

## Pull Requests

- Keep scope focused.
- Include what changed, why, and how it was tested.
- Link related issue(s).

## Code Quality

- Prefer small, testable functions.
- Avoid hard-coded constants; document assumptions.
- Add/update tests for solver behavior changes.

## Meetings and Decisions

Record major decisions in `docs/meeting-notes/` with date-stamped files.
