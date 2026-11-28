# ADR 0009 · Enforce Python lint rules

**Decision.** Run pinned Ruff against Python 3.13 source, tests, and verification scripts in the offline gate. Select rules that protect public contracts, expose runtime mistakes, or make test evidence more reliable. Use Ruff's formatter for layout. [Rule configuration](../../pyproject.toml) · [Dependency lock policy](0005-reproducible-development-builds.md) · [Offline software gate](0003-replay-and-live-evaluation.md)

**Reason.** The next aggregate, adapter, or verification script should be safe to change in isolation. Private member checks protect implementation details. Specific exception tests make it harder for setup failures to hide a broken rule. Explicit timezone and decimal inputs preserve the meaning of timestamps and amounts across machines and runs.

| Protects | Rules | What they enforce |
| --- | --- | --- |
| Public contracts | `ANN`, `SLF001`, `RUF013` | Require function parameter and return hints. Flag access to another class's private members and require an explicitly optional type when a parameter defaults to `None`. [Type-hint policy](0006-python-type-hints.md) |
| Domain values and views | `RUF008`, `RUF009`, `RUF012`, `PIE794`, `PIE796` | Flag mutable and call-based defaults, duplicate class fields, and accidental enum aliases. |
| Test evidence | `PT010`, `PT011`, `PT012`, `PT014`, `PT015`, `PT017`, `PT028`, `RUF043` | Require an expected exception, narrow broad exception checks, and keep `pytest.raises` focused on one operation. Flag duplicate parametrized cases, always-false assertions, assertions in exception handlers, defaulted test parameters, and ambiguous exception-message patterns. |
| Runtime correctness | `B`, `F`, `PLE`, `S101`, `W605`, `ISC004` | Flag common Python mistakes such as mutable function defaults, undefined names, malformed special methods, invalid escapes, and strings merged by a missing comma. Runtime validation uses explicit errors so Python optimization cannot disable it. |
| Timestamps and decimal amounts | `DTZ001`, `DTZ002`, `DTZ003`, `DTZ004`, `DTZ005`, `DTZ006`, `DTZ007`, `DTZ901`, `RUF032` | Require timezone-aware `datetime` construction, parsing, and bounds. Flag `Decimal` construction from float literals. |
| Verification tools | `T100`, `PLW1510` | Flag leftover debugger calls and require `subprocess.run` callers to choose explicitly how to handle a failed command. |
| Imports and Python idioms | `E4`, `E7`, `E9`, `I`, `UP` | Check import placement and ordering, selected statement and syntax issues, and idioms supported by the target Python version. |
| Visible lint exceptions | `PGH004`, `RUF100`, `RUF101`, `RUF102` | Require specific codes in `noqa` comments and flag unused, redirected, or invalid codes. |
| Complexity | `C901` | Cap McCabe complexity at 10 per function by default. |
| Formatting | `ruff format --check` | Check layout with Ruff's defaults, including an 88-character target width. |

**Scope and exceptions.** Tests under `tests/**` may use `assert` for pytest's assertion reporting. Keep the `UP045` exception in `domain/take_review.py` while the pinned Cosmic Ray version mutates module-level return-type unions as binary operations. Record the reason beside each exception in `pyproject.toml`.

**Verification.** Run `python scripts/check_lint.py` for the full lint scope or pass repository-relative Python paths for a focused check. Both apply the same rules and per-file complexity limits, followed by a format check. Configure justified limits under `tool.bible-music.verification.complexity-overrides` by repository-relative Python file path and record the reason with the override. Keep the README and AGENTS.md in sync when changing the default.
