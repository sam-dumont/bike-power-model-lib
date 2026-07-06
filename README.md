# bike-power-model

A cycling physics engine for power, speed, and race-time prediction, plus a
generator for Garmin Power Guide FIT files (messages 352/353).

> **Pre-release.** This alpha reserves the package name and wires up the build
> and publish pipeline. The physics solver, FIT tooling, and the full `bpm`
> command set land in a later release. Install it now if you want to track
> progress; the API is not stable yet.

## What it does

Give it a route (GPX or FIT), a rider (weight, FTP, CdA), and conditions
(wind, temperature, surface), and it predicts the power you would hold and the
speed and time that follow from it. The direction matters: it solves logic to
power to physics to speed, never the other way around. It does not read a speed
profile off a file and back out the power.

The same engine writes Garmin Power Guide FIT files, so the plan you compute
can be sideloaded onto a head unit and followed on the road.

It is calibrated and checked against real race telemetry, per rider and per
terrain type (climbs, flats, descents, cobbles, gravel), not against a single
averaged error number that hides where the model is wrong.

## Install

```bash
pip install --pre bike-power-model
```

The `--pre` flag is required while the package is in alpha.

```bash
bpm --version
bpm status
```

The planning, decoding, and FIT-generation commands arrive with the engine.
`bpm status` tells you what the current install can do.

## Requirements

Python 3.11, 3.12, or 3.13. No system libraries for the core install.

## Documentation

- [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md): local setup, tests, the offline gate
- [`docs/RELEASING.md`](docs/RELEASING.md): how a (pre-)release is cut and published
- [`CONTRIBUTING.md`](CONTRIBUTING.md): what is welcome and how to set up
- [`CHANGELOG.md`](CHANGELOG.md): what changed, per version

Reference docs for the physics, the FIT format, and the validation method ship
with the engine.

## License

MIT. See [`LICENSE`](LICENSE).
