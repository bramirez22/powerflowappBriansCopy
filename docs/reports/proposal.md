# EE 4310 Project Proposal (M0 Draft)

## Team

- Member 1: TBD (project lead / integration)
- Member 2: TBD (solver implementation)
- Member 3: TBD (UI + reporting)

## Technology Stack Choice

- Chosen stack:
  - Backend/solver engine: Python (`numpy`, `scipy`)
  - UI: Web UI in Python (Streamlit for M4 target)
  - Export: CSV/TXT from Python
- Why this stack is appropriate:
  - Fastest path for numerical methods (GS, NR, fault analysis) in a 7-week schedule.
  - Lowest integration overhead across team members and platforms.
  - Browser-based UI is naturally cross-platform (macOS/Windows/Linux).

### Option Considered but Deferred

- Python backend + C++ desktop UI is technically valid, but not recommended for first pass.
- Reason: higher integration complexity (IPC/API bridge, packaging, debugging across languages).
- Decision: ship full requirements first with Python + web UI, then consider C++ UI as stretch work.

## Architecture Plan

- Parser layer:
  - Parse plain-text bus/branch/generator input into typed internal models.
- Network model layer:
  - Per-unit normalization, bus classification (Slack/PV/PQ), branch/tap/charging handling.
- Solvers (GS/NR):
  - `GS`: complex-form iterative updates with convergence history.
  - `NR`: mismatch vector + Jacobian update each iteration.
- Fault analysis module:
  - Three-phase fault and symmetrical component sequence-network calculations.
- UI module:
  - Upload/select input file, choose method/settings, run analysis, view/export results.

## Cross-Platform Plan

- Runtime target: Python 3.11+ on macOS, Windows, Linux.
- Access pattern: local web app (`localhost`) in browser.
- Reproducibility:
  - Pinned dependencies
  - Standard startup script
  - Optional container later if needed

## Development Plan by Milestone

- M0:
  - Finalize team roles, lock stack, publish architecture and risk plan.
- M1:
  - Parser + Y-bus formation with small-case validation.
- M2:
  - GS solver with tolerance/max-iter controls and iteration reporting.
- M3:
  - NR solver with Jacobian and GS/NR comparison metrics.
- M4:
  - UI integration, line flow/loss reporting, CSV/TXT export.
- M5:
  - Three-phase + symmetrical-component short-circuit module and UI display.
- Final:
  - IEEE 14-bus validation package, report (6-10 pages), AI usage log, demo prep.

## Risks and Mitigation

- Risk: Numerical instability or non-convergence in early solver versions.
- Mitigation: early small-case tests + IEEE 14-bus baseline checks each week.

- Risk: UI integration delays.
- Mitigation: keep UI thin; backend-first API/function contracts.

- Risk: Team schedule mismatch.
- Mitigation: weekly checkpoint notes + issue ownership + milestone checklists.
