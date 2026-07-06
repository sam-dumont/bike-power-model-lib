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

The repo ships `.pre-commit-config.yaml`. Install it once, including the
commit-message stage:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

They run on every commit and block it if anything fails:

- `ruff` (lint + format), through the project's own uv venv so the version
  matches CI
- `pytest -x`, fast-fail on the first failing test
- `gitleaks`, secret scan on staged changes
- a commit-msg hook that strips any `Co-authored-by` trailer (contribution is
  credited outside the commit trail)

Don't bypass with `--no-verify`. If a hook fails, fix the underlying issue:
re-stage after ruff auto-fixes, or run the failing test locally.

## Contributing changes

Obvious bug fixes are always welcome: fix it, add a regression test in
`tests/`, open the PR. If it's genuinely a bug and the fix is small and clear,
you don't need to ask first.

Everything else, open an issue or a discussion before you write the code: new
features, new dependencies, anything that changes the model's numbers, any
structural change. It's a small project with firm opinions about scope, so a
quick conversation up front saves you from a PR that doesn't fit.

New dependencies get extra scrutiny: the supply-chain posture is deliberate
(pinned, audited, added one at a time with a reason). "Latest is better" isn't
a reason.

## LLM-assisted contributions

Welcome. This project is built with Claude, heavily, so a PR written with an
LLM's help is not a problem. The one requirement: you understand your own
change and can reason about it. Explain the *why* in the PR, be ready to defend
the approach in review, and don't send code you can't stand behind. Pasted
output you can't explain will get closed.

## Code style

- ruff-format defaults, type hints on public APIs.
- Docstrings explain the *why*: the calling convention, the failure mode, the
  observation that motivated the design. The code already says the *what*.
- Tests: integration over unit. Validate behaviour, not implementation.

## Code of conduct

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Contributions are accepted under MIT (matching the repo). By opening a PR you
agree your contribution is licensed under MIT.
