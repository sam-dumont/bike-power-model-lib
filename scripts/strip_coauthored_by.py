#!/usr/bin/env python3
"""Strip any ``Co-authored-by`` trailer from a commit message.

Wired as a pre-commit ``commit-msg`` hook (see ``.pre-commit-config.yaml``) so
the trailer never lands in this repo's history, whatever adds it. Contribution
is credited outside the commit trail, by project policy.

Install the commit-msg stage once, alongside the normal hooks:

    uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
"""

from __future__ import annotations

import re
import sys

_TRAILER = re.compile(r"^\s*co-authored-by\s*:", re.IGNORECASE)


def main() -> int:
    if len(sys.argv) < 2:
        return 0
    path = sys.argv[1]
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    kept = [ln for ln in lines if not _TRAILER.match(ln)]

    # Drop blank lines left dangling at the end after removing trailers.
    while len(kept) >= 2 and kept[-1].strip() == "" and kept[-2].strip() == "":
        kept.pop()

    if kept != lines:
        with open(path, "w", encoding="utf-8") as fh:
            fh.writelines(kept)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
