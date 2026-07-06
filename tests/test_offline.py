"""Offline gate.

The library core must import and do useful work without any network access.
CI runs the whole suite a second time under ``pytest --disable-socket`` (see
the offline job in ``.github/workflows/ci.yml``); any module that reached out
to the network at import time would raise ``SocketBlockedError`` there.

This test is the permanent home of that guarantee: as the engine grows, the
offline-safe entry points get exercised here so the socket-blocked run keeps
proving that a fresh install works with no services reachable.
"""

from __future__ import annotations

import importlib


def test_core_imports_without_network() -> None:
    import bike_power_model

    importlib.reload(bike_power_model)
    assert bike_power_model.__version__


def test_cli_imports_without_network() -> None:
    from bike_power_model.cli import cli

    assert callable(cli)
