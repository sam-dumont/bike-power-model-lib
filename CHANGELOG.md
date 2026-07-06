# Changelog

All notable changes are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[PEP 440](https://peps.python.org/pep-0440/) (so `0.0.1a0` is an alpha).

## [Unreleased]

- The physics engine, FIT tooling, and full `bpm` command set.

## [0.0.1a0]

Initial pre-release. Reserves the package name and stands up the build and
publish pipeline.

- Package scaffold: `bike_power_model` with a version and `py.typed` marker.
- `bpm` command-line shell (`--version`, `status`).
- CI: lint, test on Python 3.11/3.12/3.13, an offline gate (suite run with
  sockets blocked), a dependency CVE audit, a secret scan, and a wheel-install
  smoke test.
- Tag-driven release to PyPI via trusted publishing.
