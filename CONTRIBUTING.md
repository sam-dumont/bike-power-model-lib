# Contributing

Thanks for considering a contribution. This is a personal research tool first
and an open-source library second, so the bar is "does it make the prediction
better or the code cleaner", not "is it a feature the README mentions".

The library is in pre-release: the physics engine is still landing. If you want
to help, the highest-value thing right now is trying the build, reading the
docs, and flagging anything that reads wrong or fails on your machine.

## Setup

Python through [`uv`](https://docs.astral.sh/uv/) only. Don't use bare `python`
or `PYTHONPATH=src python`: a stale global editable install on some machines
resolves to the wrong tree and gives silently wrong results.

```bash
git clone https://github.com/sam-dumont/bike-power-model-lib
cd bike-power-model-lib
uv sync --extra dev
uv run pytest
bpm --help
```

See [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md) for the full loop (the offline
gate, the wheel smoke, `make check`).

## Pre-commit hooks

The repo ships `.pre-commit-config.yaml`. Install it once:

```bash
uv run pre-commit install
```

They run on every commit and block it if anything fails:

- `ruff` (lint + format), through the project's own uv venv so the version
  matches CI
- `pytest -x`, fast-fail on the first failing test
- `gitleaks`, secret scan on staged changes

Don't bypass with `--no-verify`. If a hook fails, fix the underlying issue:
re-stage after ruff auto-fixes, or run the failing test locally.

## What's welcome

- Bug fixes with a regression test in `tests/`.
- New Garmin FIT message decodes, with a round-trip test.
- Per-sector surface Crr refinements with a citation (a race organiser road
  book, public ride telemetry, a lab measurement).
- Per-rider power-duration wiring against APIs you own the key for
  (intervals.icu, Strava, Wahoo).
- Performance improvements with a before/after benchmark in the PR.

## What needs a discussion first

Open an issue before you write the code for any of these:

- New external dependencies. The supply-chain posture is deliberate: pinned,
  audited, added one at a time with a reason. "Latest is better" is not a
  reason.
- Architectural shifts: a new public entry point, a new constructor, a change
  to a public signature.
- Anything that changes the model's numbers. Predictions are validated per
  rider and per terrain type; a change that improves one case and quietly
  breaks another is a regression, not a win.

## Code style

- ruff-format defaults, type hints on public APIs.
- Docstrings explain the *why*: the calling convention, the failure mode, the
  observation that motivated the design. The code already says the *what*.
- Tests: integration over unit. Validate behaviour, not implementation.

## License

Contributions are accepted under MIT (matching the repo). By opening a PR you
agree your contribution is licensed under MIT.
