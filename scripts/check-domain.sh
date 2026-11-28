#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

python -m pytest
python scripts/check_lint.py
lint-imports --no-cache
python scripts/check_mutations.py
