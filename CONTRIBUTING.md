# Contributing Guide

## Branching

- Branch from `main`.
- Use naming:
  - `feature/<name>`
  - `fix/<name>`
  - `docs/<name>`

## Commit Messages

Use imperative style and be specific.

Examples:
- `Implement GS update for PQ buses`
- `Add NR Jacobian J1/J2/J3/J4 assembly`
- `Add IEEE 14-bus validation case`

## Pull Requests

Each PR must include:

- Linked issue number.
- Milestone tag (`M0`, `M1`, `M2`, `M3`, `M4`, `M5`, or `Final`).
- Test/validation evidence.
- Notes on assumptions changed.

## Technical Expectations

- Keep solver methods explicit and reviewable.
- Do not merge code you cannot explain mathematically.
- Document per-unit conventions and bus-type handling.
- For numerical changes, show convergence behavior.

## AI-Assisted Coding Requirement

The course requires AI usage documentation.

When AI contributes to work:
- Add or update an entry in `docs/ai-usage/`.
- Include prompt summary, generated output summary, and verification steps.

Use the template:
- `docs/templates/ai_usage_log_template.md`

## Meetings and Decisions

Use dated files in `docs/meeting-notes/` (e.g., `2026-02-25.md`).
Track decisions, owners, deadlines, and blockers.
