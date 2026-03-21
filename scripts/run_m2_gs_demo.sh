#!/usr/bin/env bash
set -euo pipefail

if [ -x ".venv/bin/python" ]; then
  .venv/bin/python -m src.validation.run_m2_gs_demo "$@"
else
  python3 -m src.validation.run_m2_gs_demo "$@"
fi
