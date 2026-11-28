"""Read the thresholds shared by the offline verification commands."""

import tomllib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

SOURCE_PACKAGE = Path("src/bible_music")


@dataclass(frozen=True)
class VerificationSettings:
    minimum_kill_percent: int
    mutation_overrides: dict[Path, int]
    complexity_overrides: dict[Path, int]

    def mutation_floor_for(self, module: Path) -> int:
        return self.mutation_overrides.get(module, self.minimum_kill_percent)


def mutation_modules(root: Path) -> set[Path]:
    return {
        path.relative_to(root)
        for path in (root / SOURCE_PACKAGE).rglob("*.py")
        if path.name != "__init__.py"
    }


def load_verification_settings(root: Path) -> VerificationSettings:
    text = (root / "pyproject.toml").read_text(encoding="utf-8")
    config = tomllib.loads(text)["tool"]["bible-music"]["verification"]
    known_keys = {"minimum-kill-percent", "mutation-overrides", "complexity-overrides"}
    if unknown_keys := config.keys() - known_keys:
        raise ValueError(
            f"Unknown verification settings: {', '.join(sorted(unknown_keys))}"
        )
    floor = _threshold(
        config.get("minimum-kill-percent"), "minimum-kill-percent", 0, 100
    )
    mutation = _overrides(root, config, "mutation-overrides", 0, 100)
    complexity = _overrides(root, config, "complexity-overrides", 1)
    if unknown_modules := mutation.keys() - mutation_modules(root):
        paths = ", ".join(str(module) for module in sorted(unknown_modules))
        raise ValueError(f"Mutation overrides require a covered source module: {paths}")
    return VerificationSettings(floor, mutation, complexity)


def _overrides(
    root: Path,
    config: Mapping[str, object],
    name: str,
    minimum: int,
    maximum: int | None = None,
) -> dict[Path, int]:
    table = config.get(name, {})
    if not isinstance(table, dict):
        raise ValueError(f"{name} must be a table of module paths and thresholds")
    overrides = {}
    for key, value in table.items():
        module = Path(key)
        path = root / module
        if (
            key != module.as_posix()
            or module.is_absolute()
            or ".." in module.parts
            or module.suffix != ".py"
            or not path.is_file()
            or not path.resolve().is_relative_to(root)
        ):
            raise ValueError(
                f"{name} requires a repository-relative Python file: {key!r}"
            )
        overrides[module] = _threshold(value, f"{name}[{key!r}]", minimum, maximum)
    return overrides


def _threshold(
    value: object, name: str, minimum: int, maximum: int | None = None
) -> int:
    if (
        type(value) is not int
        or value < minimum
        or (maximum is not None and value > maximum)
    ):
        bounds = (
            f"{minimum}–{maximum}" if maximum is not None else f"at least {minimum}"
        )
        raise ValueError(f"{name} must be an integer {bounds}")
    return value
