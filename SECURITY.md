# Security policy

## Reporting a vulnerability

Email **sam@dropbars.be** with details. PGP isn't required; if you'd like to
encrypt, ask in a first message and a key will be provided.

I'll acknowledge within 72 hours. For verified issues I'll work with you on a
fix and coordinated disclosure, with credit in the changelog unless you prefer
to stay anonymous.

## Scope

In scope:

- The `bike-power-model` Python library and its command-line interface.
- The Garmin Power Guide FIT writer (messages 352/353) and the FIT/GPX parsing
  paths.
- The dependency supply chain (a malicious or vulnerable dependency shipped in
  a release).

Out of scope:

- Third-party services the library can optionally talk to (weather APIs,
  elevation data sources). Report those to the provider.
- Denial-of-service by feeding the library deliberately huge inputs. Parse
  what you'd actually ride.

## Data handling

The library reads FIT and GPX files, which can contain personal data (GPS
tracks, heart rate, power, body metrics). It processes them locally and does
not transmit them anywhere. Optional network features (weather, elevation) send
only what they need (coordinates, timestamps) to the endpoint you configure,
and every one has a documented offline fallback.

If a finding involves personal data leaving the machine unexpectedly, flag it
prominently in the report subject so I can prioritise.
