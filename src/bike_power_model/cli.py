"""Command-line entry point for bike-power-model.

Registered as the ``bpm`` console script. In this pre-release the CLI only
reports version and status; the planning, decoding, and FIT-generation
commands ship with the engine in a later release.
"""

from __future__ import annotations

import click

from . import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="bpm")
def cli() -> None:
    """bike-power-model command-line interface."""


@cli.command()
def status() -> None:
    """Report the version and readiness of this install."""
    click.echo(f"bike-power-model {__version__}")
    click.echo(
        "Pre-release: the physics engine and full command set ship in a later release."
    )


if __name__ == "__main__":
    cli()
