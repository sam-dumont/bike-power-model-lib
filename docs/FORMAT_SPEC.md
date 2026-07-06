# Garmin Power Guide FIT Format Specification

**Version**: 1.0 (April 2026)
**Status**: Reverse-engineered from device exports. Two sample files verified.

## Overview

Garmin's Power Guide feature stores per-segment power targets in two undocumented FIT message types:

- **Message 352**: Power Guide Summary (1 per file)
- **Message 353**: Power Guide Split (N per file, one per segment)

These messages are NOT in the official Garmin FIT SDK Profile. No existing FIT library (fitparse, fitdecode, Golden Cheetah, fit-tool) documents them.

## File Structure

A Power Guide FIT file contains:

```
[FIT Header (14 bytes)]
[File ID Message (standard, global mesg 0)]
[Message 352 Definition Record]
[Message 352 Data Record]
[Message 353 Definition Record]
[Message 353 Data Record] × N splits
[CRC (2 bytes)]
```

Architecture is **big-endian** (architecture byte = 1 in definition records).

## Message 352 — Power Guide Summary

One per file. Contains rider profile, physics parameters, and aggregate stats.

| Field # | Name | Base Type | Size | Unit | Description |
|---------|------|-----------|------|------|-------------|
| 1 | name | string | 32 | — | Power guide name (null-padded) |
| 2 | split_count | uint16 | 2 | — | Number of splits |
| 3 | course_pk | uint32z | 4 | — | Garmin course ID (0 if custom) |
| 4 | created_timestamp | uint32 | 4 | s | FIT timestamp (seconds since 1989-12-31 UTC) |
| 5 | unknown | uint8 | 1 | — | Always 1 in samples |
| 6 | user_ftp | uint16 | 2 | W | Functional Threshold Power |
| 7 | goal_effort | float32 | 4 | — | Difficulty slider: 0.0 (easiest) → 1.0 (hardest) |
| 8 | aero_coefficient | float32 | 4 | m² | CdA (aerodynamic drag area) |
| 9 | rolling_resistance | float32 | 4 | — | Crr (rolling resistance coefficient) |
| 10 | rider_mass | uint16 | 2 | hg | Rider mass in hectograms (÷100 = kg) |
| 11 | bike_mass | uint16 | 2 | hg | Bike mass in hectograms (÷100 = kg) |
| 13 | min_segment_length | uint32 | 4 | — | Always 0 in samples |
| 14 | estimated_duration | uint32 | 4 | ms | Total estimated duration in milliseconds |
| 15 | ftp_usage_pct | float32 | 4 | % | Duration-weighted mean power as % of FTP |
| 16 | max_power_pct | uint32 | 4 | % FTP | Max split power as % of FTP |
| 17 | mean_power_pct | uint32 | 4 | % FTP | Mean split power as % of FTP |
| 18 | aero_profile | uint8 | 1 | enum | Rider position preset |
| 19 | terrain_profile | uint8 | 1 | enum | Surface type preset |

### Aero Profile Enum (field 18)

| Value | Name | Default CdA (m²) |
|-------|------|-------------------|
| 0 | RELAXED | 0.6915 |
| 1 | STANDARD | 0.4768 |
| 2 | OPTIMIZED | 0.3695 |

All values confirmed from device-exported FIT files. Note: CdA may vary from defaults depending on rider dimensions. The actual CdA is stored in field 8.

### Terrain Profile Enum (field 19)

| Value | Name | Default Crr |
|-------|------|-------------|
| 0 | MOUNTAIN | 0.0120 |
| 1 | GRAVEL | 0.0090 |
| 2 | ROAD | 0.0040 |

All values confirmed from device-exported FIT files (April 2026).

## Message 353 — Power Guide Split

N per file (one per course segment). Contains the per-segment power target and geometry.

| Field # | Name | Base Type | Size | Unit | Description |
|---------|------|-----------|------|------|-------------|
| 254 | message_index | uint16 | 2 | — | 1-based split index |
| 1 | power_target_pct | uint32 | 4 | % FTP | Target power as % of FTP |
| 2 | distance | uint32 | 4 | cm | Segment distance in centimeters |
| 3 | estimated_duration | uint32 | 4 | ms | Estimated time in milliseconds |
| 4 | mean_grade | sint16 | 2 | 0.01% | Mean gradient (×100, so 11 = 0.11%) |
| 5 | unknown | sint16 | 2 | — | Always 0x7FFF (32767) in samples |
| 6 | start_latitude | sint32 | 4 | semi | Semicircles (×180/2³¹ = degrees) |
| 7 | start_longitude | sint32 | 4 | semi | Semicircles |
| 8 | end_latitude | sint32 | 4 | semi | Semicircles |
| 9 | end_longitude | sint32 | 4 | semi | Semicircles |
| 10 | elevation_change | sint32 | 4 | cm | Signed, centimeters |
| 11 | heading | sint32 | 4 | 0.0001 rad | Heading × 10000 |

## Encoding Notes

### Coordinates
FIT uses semicircles for GPS coordinates: `degrees = semicircles × (180 / 2³¹)`

### Timestamps
FIT epoch is 1989-12-31T00:00:00 UTC. Offset from Unix epoch: 631,065,600 seconds.

### CRC
FIT uses CRC-16 with polynomial 0xA001 (bit-reversed representation). Applied to all bytes between header and CRC.

## Splitting Algorithm

Garmin segments courses based purely on the elevation profile:
- Splits at gradient sign changes (uphill↔downhill)
- Splits at large gradient shifts (>~0.3-0.5%)
- Flat sections merge into long splits (up to 6km)
- Split geometry is identical regardless of rider profile or effort level
- The Roubaix course (147km, 420m elevation) → 89 splits
- The Olympos course (125km, 2133m elevation) → 142 splits

## Physics Model

Power targets follow a standard cycling power balance:

```
P = (m·g·grade + Crr·m·g + ½·ρ·CdA·v²) · v
```

The `goal_effort` slider controls a target speed; power follows from physics on each segment's gradient. Verified within 2-3% of Garmin's values across 801 data points (89 splits × 9 configurations).

## Verification

This spec was reverse-engineered by cross-referencing:
1. Binary FIT files exported from Garmin devices
2. JSON API exports from Garmin Connect
3. 9 configurations covering 3 positions × 3 terrains × 3 effort levels
4. 2 different courses (flat Roubaix, mountainous Olympos)

All field mappings verified. A reference reader/writer for this format lands with the bike-power-model engine; this library is in pre-release (see the repository for status).
