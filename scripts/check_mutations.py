"""Gate each module's confirmed kills in a fresh Cosmic Ray session."""

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path("src/bible_music")
# Cosmic Ray 8.9.0 generates no mutants for these forwarding and lookup modules.
MAY_HAVE_NO_MUTANTS = frozenset(
    {PACKAGE / "app/review_take.py", PACKAGE / "adapters/in_memory_scripture.py"}
)
MINIMUM_KILL_PERCENT = 95
PYTEST_STATUS = "PYTEST_EXIT="
BEHAVIOR_TESTS = ("tests/domain", "tests/app")
PYTEST_ARGS = ["-qx", "-p", "no:cacheprovider", *BEHAVIOR_TESTS]


def pytest_status(result):
    if result is None:
        return "incomplete"
    if result["worker_outcome"] in {"no-test", "skipped"}:
        return "untested"
    if result["worker_outcome"] != "normal":
        return "incomplete"

    lines = (result["output"] or "").splitlines()
    marker = lines[-1] if lines else ""
    match (result["test_outcome"], marker):
        case ("killed", code) if code == f"{PYTEST_STATUS}1":
            return "killed"
        case ("survived", code) if code == f"{PYTEST_STATUS}0":
            return "survived"
        case (_, code) if code == f"{PYTEST_STATUS}5":
            return "untested"
        case _:
            return "incomplete"


def score_report(report, expected_modules, may_have_no_mutants=frozenset()):
    counts = defaultdict(Counter)
    for line in report.splitlines():
        job, result = json.loads(line)
        (mutation,) = job["mutations"]
        module = Path(mutation["module_path"])
        status = pytest_status(result)
        counts[module][status] += 1
        if status != "killed":
            print(
                f"{module}:{mutation['start_pos'][0]} {mutation['operator_name']} {status}"
            )

    absent = expected_modules - counts.keys()
    for module in sorted(absent & may_have_no_mutants):
        print(f"{module}: no mutants generated")
    missing = absent - may_have_no_mutants
    for module in sorted(missing):
        print(f"{module}: no mutation results")

    passed = not missing
    for module, outcomes in sorted(counts.items()):
        total = outcomes.total()
        killed = outcomes["killed"]
        print(f"{module}: {killed}/{total} confirmed kills ({killed / total:.1%})")
        if outcomes["incomplete"] or 100 * killed < MINIMUM_KILL_PERCENT * total:
            passed = False
    return passed


def run_mutations(scope, expected_modules, workspace):
    shutil.copytree(
        ROOT / "src", workspace / "src", ignore=shutil.ignore_patterns("__pycache__")
    )
    for tests in BEHAVIOR_TESTS:
        shutil.copytree(
            ROOT / tests,
            workspace / tests,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
    shutil.copy2(ROOT / "pyproject.toml", workspace)
    env = {
        **os.environ,
        "PYTHONPATH": str(workspace / "src"),
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
    }
    subprocess.run(
        [sys.executable, "-m", "pytest", *PYTEST_ARGS],
        cwd=workspace,
        env=env,
        check=True,
    )

    # Cosmic Ray calls any nonzero status or timeout a kill. Record pytest's actual verdict.
    test_code = (
        f"import pytest; status = pytest.main({PYTEST_ARGS!r}); "
        f"print({PYTEST_STATUS!r} + str(int(status))); raise SystemExit(status)"
    )
    test_command = shlex.join((sys.executable, "-c", test_code))
    config = workspace / "mutation.toml"
    config.write_text(
        "[cosmic-ray]\n"
        f"module-path = {json.dumps(scope.as_posix())}\n"
        f"test-command = {json.dumps(test_command, ensure_ascii=False)}\n"
        "timeout = 10.0\n"
        "[cosmic-ray.distributor]\n"
        'name = "local"\n',
        encoding="utf-8",
    )
    session = "session.sqlite"
    cosmic_ray = shutil.which("cosmic-ray", path=str(Path(sys.executable).parent))
    if cosmic_ray is None:
        raise RuntimeError(
            "Install the project's dev dependencies in the active Python environment."
        )
    for action in ("init", "exec"):
        subprocess.run(
            [cosmic_ray, action, config.name, session],
            cwd=workspace,
            env=env,
            check=True,
        )
    report = subprocess.check_output(
        [cosmic_ray, "dump", session], cwd=workspace, env=env, text=True
    )
    return score_report(report, expected_modules, MAY_HAVE_NO_MUTANTS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modules = {
        path.stem: path.relative_to(ROOT)
        for path in (ROOT / PACKAGE).rglob("*.py")
        if path.stem != "__init__"
    }
    parser.add_argument("module", nargs="?", choices=sorted(modules))
    args = parser.parse_args()
    scope = modules[args.module] if args.module else PACKAGE
    expected_modules = {scope} if args.module else set(modules.values())
    with TemporaryDirectory(prefix="bible-music-mutations-") as directory:
        return 0 if run_mutations(scope, expected_modules, Path(directory)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
