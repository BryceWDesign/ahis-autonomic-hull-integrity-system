# T-IMP-010 — Low-Velocity Impact (Peak Strain/Accel Delta)
This folder contains run packages for the AHIS PoC impact test defined in `docs/07_Test_Matrix.md`.

## Purpose
Compare **Baseline** vs **AHIS** coupon configurations under a controlled low-velocity impact test and report:
- peak substrate strain (µε) and/or peak acceleration (g)
- repeatability/variance across runs
- post-impact damage documentation (if captured under T-IMP-011 in parallel)

## Required run package structure
Each run must be stored under:

`results/T-IMP-010/<RUN_ID>/`

and must include:
- `README.md` (filled run report; use `docs/10_Data_and_Results_Template.md`)
- `raw/`
- `processed/`
- `plots/`
- `calibration/`
- `photos/`

## Notes
- Boundary conditions must be documented with photos. Fixture differences can dominate results.
- If a run is simulated, it must be labeled **SIMULATED** prominently and include a `SIMULATED_DATA_NOTICE.md`.

---
No data is included in this index file. It exists to enforce consistency and auditability.
