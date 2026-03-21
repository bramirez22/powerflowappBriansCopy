#!/usr/bin/env bash
set -euo pipefail

if [ -x ".venv/bin/python" ]; then
  .venv/bin/python -m src.validation.plot_m2_history "$@"
else
  python3 -m src.validation.plot_m2_history "$@"
fi
