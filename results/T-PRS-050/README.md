# T-PRS-050 — Pressure / Leak Test (Leak Onset + Leak Rate)
This folder contains run packages for the AHIS PoC pressure/leak test defined in `docs/07_Test_Matrix.md`.

## Purpose
Measure and report:
- leak onset (as explicitly defined in the run report)
- leak rate (Pa/s or sccm; method must be stated)
- (instrumented mode) detection time relative to leak onset
- dominant leak paths (often edge seals) via photos and notes

## Required run package structure
Each run must be stored under:

`results/T-PRS-050/<RUN_ID>/`

and must include:
- `README.md` (filled run report; use `docs/10_Data_and_Results_Template.md`)
- `raw/` (pressure logs unmodified)
- `processed/` (computed leak rate tables/curves)
- `plots/` (pressure vs time, leak-rate plots with units)
- `calibration/` (sensor calibration/config)
- `photos/` (fixture + seal details + post-test inspection)

## Leak onset definition (mandatory)
Every run must explicitly define “leak onset,” for example:
- pressure decay rate exceeds a threshold (Pa/s) for a sustained time window, or
- a flow meter reading exceeds a threshold (sccm)

No leak onset definition = invalid run.

## Notes
- If the fixture introduces known leak paths unrelated to the coupon, document them and treat results as fixture-limited.
- If data is simulated, it must be labeled **SIMULATED** and include `SIMULATED_DATA_NOTICE.md`.

---
No data is included in this index file. It exists to enforce consistency and auditability.
