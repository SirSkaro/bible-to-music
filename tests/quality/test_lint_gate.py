import shutil
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def lint_gate(tmp_path: Path) -> Path:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    project_scripts = Path(__file__).resolve().parents[2] / "scripts"
    for filename in ("check_lint.py", "verification_config.py"):
        shutil.copy2(project_scripts / filename, scripts)
    (tmp_path / "pyproject.toml").write_text(
        """\
[tool.ruff]
extend-exclude = ["scripts"]
[tool.ruff.lint]
select = ["C901", "F"]
[tool.ruff.lint.mccabe]
max-complexity = 1
[tool.bible-music.verification]
minimum-kill-percent = 95
[tool.bible-music.verification.complexity-overrides]
"src/override.py" = 2
""",
        encoding="utf-8",
    )
    (tmp_path / "tests").mkdir()
    source = tmp_path / "src"
    source.mkdir()
    for filename in ("default.py", "override.py"):
        (source / filename).write_text(
            "def explain(condition):\n    if condition:\n        return 1\n    return 2\n",
            encoding="utf-8",
        )
    return tmp_path


def run_lint(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(root / "scripts/check_lint.py"), *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


def test_full_and_focused_lint_apply_the_same_module_complexity_cap(
    lint_gate: Path,
) -> None:
    full = run_lint(lint_gate)
    assert full.returncode == 1, (full.stdout, full.stderr)
    assert "C901" in full.stdout
    assert "src/default.py" in full.stdout
    assert "src/override.py" not in full.stdout

    focused = run_lint(lint_gate, "src/override.py")
    assert focused.returncode == 0, (focused.stdout, focused.stderr)


def test_a_complexity_override_still_applies_the_other_lint_rules(
    lint_gate: Path,
) -> None:
    module = lint_gate / "src/override.py"
    contents = module.read_text(encoding="utf-8")
    module.write_text("import sys\n\n\n" + contents, encoding="utf-8")

    result = run_lint(lint_gate, "src/override.py")

    assert result.returncode == 1, (result.stdout, result.stderr)
    assert "F401" in result.stdout
    assert "C901" not in result.stdout


def test_a_typo_in_an_override_path_fails_verification(lint_gate: Path) -> None:
    config = lint_gate / "pyproject.toml"
    contents = config.read_text(encoding="utf-8")
    config.write_text(
        contents.replace("src/override.py", "src/ovverride.py"), encoding="utf-8"
    )

    result = run_lint(lint_gate)

    assert result.returncode == 2
    assert "src/ovverride.py" in result.stderr
