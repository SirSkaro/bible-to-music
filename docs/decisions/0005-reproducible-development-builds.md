# ADR 0005 · Lock the development and build environment

**Decision.** Pin the direct development tools and the setuptools build backend in `pyproject.toml`. Commit the resolved dependencies and their SHA-256 artifact hashes in `requirements-build.lock` and `requirements-dev.lock`. The lock targets CPython 3.13 on macOS and glibc Linux for ARM64 and x86-64. The Python compatibility declaration describes the application separately.

**Reason.** Ruff, Import Linter, pytest, and Cosmic Ray all affect what the offline gate reports. Exact transitive versions and artifact hashes let another workspace run the same checks with the same toolchain. The lock starts from the previously verified dependency versions.

**Build setup.** Install the hashed build lock first, then install the hashed development lock with build isolation disabled. Yattag 1.16.1 is distributed as a source archive and builds using the locked setuptools version. Install the project in editable mode with build isolation disabled and index access turned off so the installed versions must satisfy the project's exact requirements. The same setup can use a local directory of locked artifacts with pip's `--no-index --find-links` options. [Setup commands](../../README.md#offline-verification)

**Update procedure.**

1. Update the direct pins in `pyproject.toml` as needed. In a fresh CPython 3.13 environment, install the proposed build backend and resolve the `dev` extra. Use `pip download` with `--no-build-isolation --only-binary=:all: --no-binary=yattag` to gather the resolved project dependencies. Include the exact build backend package in the download.
2. Record each exact version in the appropriate lock. Gather its compatible wheels for the supported targets and compute SHA-256 hashes with `python -m pip hash`. Hash the Yattag source archive. Refresh the source exception if the new versions have different distribution formats.
3. Install from both locks into a fresh environment, install the project using the documented command, run `python -m pip check`, and run the full offline gate. Review the lock and pin changes together.

**Change trigger.** Add lock artifacts and verify the install and offline gate on a new Python or platform target when it becomes part of development.
