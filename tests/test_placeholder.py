"""Baseline tests for the pre-release scaffold.

These keep CI green while the engine is still landing. They are replaced by
the real physics and FIT test suites when the engine ships.
"""

from __future__ import annotations

from click.testing import CliRunner

import bike_power_model
from bike_power_model.cli import cli


def test_version_is_exposed() -> None:
    assert isinstance(bike_power_model.__version__, str)
    assert bike_power_model.__version__


def test_cli_reports_version() -> None:
    result = CliRunner().invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert bike_power_model.__version__ in result.output


def test_cli_status_runs() -> None:
    result = CliRunner().invoke(cli, ["status"])
    assert result.exit_code == 0
    assert "bike-power-model" in result.output
