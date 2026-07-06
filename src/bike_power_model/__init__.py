"""bike-power-model: a cycling physics engine for power, speed, and race time.

This is a pre-release. The physics solver, FIT tooling, and full command-line
interface land in a later release; this alpha reserves the package name and
exercises the build-and-publish pipeline end to end.

Status and roadmap: https://github.com/sam-dumont/bike-power-model-lib
"""

from __future__ import annotations

try:
    from ._version import __version__
except ImportError:  # pragma: no cover - source checkout without a build
    # _version.py is written by hatch-vcs at build time from the git tag.
    # A plain source checkout (no build, no tag) has no version to report.
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
