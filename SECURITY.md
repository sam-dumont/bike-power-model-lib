# Security

## Reporting a vulnerability

Email **security@bikepowermodel.fit**, or open a private advisory on GitHub
(Security → Report a vulnerability). Please don't use a public issue for a real
vulnerability.

I'm a solo maintainer, so there's no formal SLA, but I read these and I'll work
with you on a fix. Happy to credit you in the changelog unless you'd rather stay
anonymous.

## What this is, and what actually leaves your machine

bike-power-model is a local library. It reads FIT and GPX files, runs the
physics on your machine, and writes FIT files back. It doesn't phone home.

The only data that leaves your machine is what you configure. If you point it at
a weather or elevation service, it sends that service the coordinates and
timestamps it needs, nothing more. Every one of those features has an offline
fallback, so the whole thing runs with no network at all (the test suite proves
it, with sockets blocked).

That keeps the realistic surface small: a malformed FIT or GPX that crashes or
hangs the parser, or a dependency shipping a known CVE in a release. Those are
the things worth reporting.
