import ast
from importlib.util import resolve_name
from pathlib import Path
from sys import stdlib_module_names

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "src" / "bible_music"
DOMAIN = "bible_music.domain"


def imports_in(path):
    package = ".".join(path.parent.relative_to(PACKAGE.parent).parts)
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            yield from ((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            name = "." * node.level + (node.module or "")
            yield node.lineno, resolve_name(name, package)


def test_domain_imports_only_the_standard_library_and_the_domain():
    paths = [PACKAGE / "__init__.py", *(PACKAGE / "domain").rglob("*.py")]
    forbidden = [
        f"{path.relative_to(ROOT)}:{line} imports {module}"
        for path in paths
        for line, module in imports_in(path)
        if module.split(".")[0] not in stdlib_module_names
        and module != DOMAIN
        and not module.startswith(f"{DOMAIN}.")
    ]
    assert not forbidden, "\n".join(forbidden)
