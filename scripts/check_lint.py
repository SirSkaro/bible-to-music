"""Check lint, complexity, and formatting for all or selected Python files."""

import argparse
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from verification_config import load_verification_settings

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = ("src", "tests", "scripts")


def run_ruff(
    *args: str, capture_output: bool = False
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ruff", *args],
        cwd=ROOT,
        capture_output=capture_output,
        text=True,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths", nargs="*", help="repository-relative directories or files"
    )
    args = parser.parse_args()
    targets = args.paths or DEFAULT_TARGETS
    if any(not (ROOT / target).resolve().is_relative_to(ROOT) for target in targets):
        parser.error("lint targets must be inside the repository")
    try:
        settings = load_verification_settings(ROOT)
    except (KeyError, ValueError) as error:
        parser.error(str(error))

    discovered = run_ruff("check", "--show-files", *targets, capture_output=True)
    if discovered.stderr:
        sys.stderr.write(discovered.stderr)
    if discovered.returncode:
        return discovered.returncode

    by_limit = defaultdict(list)
    for file in discovered.stdout.splitlines():
        path = Path(file).relative_to(ROOT)
        by_limit[settings.complexity_overrides.get(path)].append(path.as_posix())

    status = 0
    for limit, paths in by_limit.items():
        override = (
            []
            if limit is None
            else ["--config", f"lint.mccabe.max-complexity = {limit}"]
        )
        status = max(status, run_ruff("check", *override, *paths).returncode)
    return max(status, run_ruff("format", "--check", *targets).returncode)


if __name__ == "__main__":
    raise SystemExit(main())
