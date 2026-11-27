#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

python -m pytest
ruff check src tests scripts/check_mutations.py
ruff format --check src tests scripts/check_mutations.py
lint-imports --no-cache
python scripts/check_mutations.py
