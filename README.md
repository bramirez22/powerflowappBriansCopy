<<<<<<< HEAD
# powerflowapp
Power Flow Analysis App
=======
# EE 4310 Power Systems Analysis - Group Project (Spring 2026)

Collaborative repository for the EE 4310 project deliverables, code, analysis, and documentation.

## Quick Start

1. Clone:
   ```bash
   git clone https://github.com/<org-or-user>/<repo-name>.git
   cd <repo-name>
   ```
2. Create a branch:
   ```bash
   git checkout -b feature/<short-task-name>
   ```
3. Work, commit, push, and open a Pull Request.

## Team Workflow

- `main` is protected and always reviewable/runnable.
- Work happens in short-lived branches: `feature/*`, `fix/*`, `docs/*`.
- All merges go through PR review.
- Keep PRs small (target <300 lines changed when possible).

## Suggested 7-Week Plan

1. Week 1: Finalize requirements, assign owners, set baseline model assumptions.
2. Week 2: Build core data model and initial power-flow solver pipeline.
3. Week 3: Validate against small benchmark cases and write test harness.
4. Week 4: Add UI/reporting outputs and improve numerical robustness.
5. Week 5: Scenario analysis and sensitivity studies.
6. Week 6: Draft final report/presentation and polish visuals.
7. Week 7: Final verification, rehearsal, packaging, and submission.

## Repository Layout

```text
.github/                 # CI and PR/Issue templates
/docs/
  spec/                  # Project specification PDFs and requirement notes
  meeting-notes/         # Team meeting logs
  reports/               # Report drafts and final submission artifacts
/src/                    # Main implementation
/tests/                  # Unit/integration tests
/data/
  raw/                   # Input datasets (immutable)
  processed/             # Derived data artifacts
/notebooks/              # Exploratory analyses
/scripts/                # Utility scripts (setup, checks, exports)
```

## Definition of Done

- Code merged via PR + at least 1 reviewer.
- Tests relevant to change pass.
- README/docs updated if behavior or assumptions changed.
- Reproducible steps included for new analyses.

## Project Spec

Place the course project specification in `docs/spec/` (or keep the original in root and reference it there).
>>>>>>> Initial project scaffold for EE 4310 group collaboration
