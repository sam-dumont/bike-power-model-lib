# Releasing

Releases are tag-driven. You push a PEP 440 tag; GitHub Actions builds that
exact version and publishes it to PyPI with trusted publishing (no API token
stored anywhere).

## One-time setup: PyPI trusted publisher

Do this once, before the first release, or the publish job will fail.

1. On [pypi.org](https://pypi.org), while the project does not exist yet, add a
   **pending publisher** under your account:
   Account settings → Publishing → Add a pending publisher.
2. Fill in:
   - PyPI project name: `bike-power-model`
   - Owner: `sam-dumont`
   - Repository: `bike-power-model-lib`
   - Workflow name: `release.yml`
   - Environment: `pypi`
3. In the GitHub repo, create an environment named `pypi`
   (Settings → Environments → New environment). Optionally require a reviewer
   so a publish waits for a manual approval.

Once the first release publishes, PyPI converts the pending publisher into a
normal trusted publisher tied to the project. No token is ever created.

## Cutting a release

The version is the tag. `hatch-vcs` reads it straight from git, so there is no
version string to bump in a file.

```bash
# make sure main is green and up to date
git checkout main && git pull

# alpha / beta / release candidate / final
git tag v0.0.1a0   && git push origin v0.0.1a0
git tag v0.1.0b1   && git push origin v0.1.0b1
git tag v0.1.0rc1  && git push origin v0.1.0rc1
git tag v0.1.0     && git push origin v0.1.0
```

Pushing the tag triggers `release.yml`, which:

1. builds the sdist and wheel,
2. runs the wheel-install smoke test,
3. creates a GitHub release (marked pre-release for `a` / `b` / `rc` versions),
4. publishes to PyPI.

## Pre-releases

While the engine is landing, ship alpha (`aN`) or beta (`bN`) versions. They
are installable only with the `--pre` flag:

```bash
pip install --pre bike-power-model
```

so a normal `pip install bike-power-model` never picks up an unfinished build.

## Dry run

To test the build without publishing, trigger the workflow manually
(Actions → Release → Run workflow) with `dry_run` left on. It builds and
smoke-tests the current ref and stops before the GitHub release and PyPI steps.

## After a release

- Confirm the version at `https://pypi.org/project/bike-power-model/`.
- Move the `[Unreleased]` notes in `CHANGELOG.md` under the new version.
- `pip install --pre bike-power-model==<version>` in a clean env as a final
  check.
