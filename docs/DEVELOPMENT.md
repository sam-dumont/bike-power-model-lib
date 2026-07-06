# Development

## Prerequisites

[`uv`](https://docs.astral.sh/uv/) is the only prerequisite. It manages the
Python version, the virtualenv, and the lockfile. Don't use bare `python`.

```bash
git clone https://github.com/sam-dumont/bike-power-model-lib
cd bike-power-model-lib
uv sync --extra dev
```

`uv sync` reads `uv.lock` and builds the venv. The editable install lives inside
that venv, so every command below goes through `uv run`.

## The loop

The `Makefile` wraps the common tasks. `make help` lists them.

```bash
make test      # pytest with coverage
make offline   # pytest with sockets blocked (the offline gate)
make lint      # ruff check
make format    # ruff format (writes)
make build     # sdist + wheel into dist/
make wheel-smoke   # build, then import-test the wheel in an isolated env
make check     # lint + format-check + test + offline, the same set CI runs
make audit     # pip-audit against the locked dependency tree
```

Run `make check` before pushing. If it's green, CI will be too.

### The offline gate

The core must import and run with no network reachable. `make offline` runs the
suite with sockets blocked (`pytest --disable-socket`); a module that reached
out to the network at import time fails there. Optional network features
(weather, elevation) are exercised in their own tests that opt back into
sockets. Keep the gate green: it is a release requirement, not a nicety.

### The wheel smoke

`pytest` reads from `src/`, so it can't catch two packaging bugs: a runtime
dependency that's imported but not declared, and a data file that's read at
runtime but not shipped in the wheel. `make wheel-smoke` builds the wheel,
installs it into a throwaway env with no source tree on `sys.path`, and
exercises the import paths. CI runs the same script.

## Layout

```
src/bike_power_model/   the library (physics engine + FIT tooling + CLI)
  __init__.py           public surface + __version__
  py.typed              PEP 561 marker: this package ships types
  cli.py                the `bpm` command-line entry point
tests/                  the test suite (offline by default)
scripts/wheel_smoke.py  the packaging smoke test CI runs post-build
docs/                   these docs
samples/                small, curated reference files (e.g. format FITs)
```

## Versioning

Versions come from git tags via `hatch-vcs`: the tag `v0.0.1a0` builds
`0.0.1a0`. `src/bike_power_model/_version.py` is generated at build time and is
gitignored, so you never edit a version by hand. See
[`RELEASING.md`](RELEASING.md).

## Type checking

The package ships `py.typed`, so it advertises inline types to downstream users.
Keep public signatures annotated. A type checker (mypy or pyright) can be added
to the loop once the engine lands and the surface is stable.
