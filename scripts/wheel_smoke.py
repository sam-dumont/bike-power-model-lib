#!/usr/bin/env python3
"""Smoke test that runs against the *installed wheel*, not the source tree.

Run in an isolated environment where ``src/`` is not on ``sys.path``, so it
catches the class of packaging bug the source-tree test suite cannot see:

  - a runtime dependency imported but not declared in ``[project.dependencies]``
  - a data file read at runtime but not shipped inside the wheel

Both slip past ``pytest`` (which reads from ``src/``) and past ``uv build``
(which runs no code after the build). This exercises the wheel-installed
module in a fresh env instead.

Usage (locally / in CI):
    uv build --wheel --quiet
    uv run --isolated --no-project \
        --with dist/bike_power_model-*.whl python scripts/wheel_smoke.py

Exit 0 on success, 1 on any failure.
"""

from __future__ import annotations

import sys
from collections.abc import Callable


def _check(label: str, fn: Callable[[], object]) -> None:
    try:
        fn()
    except Exception as e:  # noqa: BLE001 - report any failure and stop
        print(f"FAIL  {label}: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"ok    {label}")


def _import_package() -> None:
    import bike_power_model

    assert bike_power_model.__version__, "empty __version__"


def _import_cli() -> None:
    from bike_power_model.cli import cli

    assert callable(cli)


def main() -> int:
    _check("import bike_power_model", _import_package)
    _check("import bpm CLI entry point", _import_cli)
    print("\nwheel smoke OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
