#!/usr/bin/env bash
set -euo pipefail

if [ -x ".venv/bin/python" ]; then
  .venv/bin/python -m src.validation.run_small_case_validation
else
  python3 -m src.validation.run_small_case_validation
fi
