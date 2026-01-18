# AHIS Results Directory

This folder holds **evidence packages** produced by AHIS proof-of-concept tests.
No safety claims are permitted without real measured data stored here in the required format.

## 1) Required structure (per run)
Create one folder per test run:

`results/<TEST_ID>/<RUN_ID>/`

Example:
`results/T-IMP-010/RUN_2026-01-12_AHIS-PANEL-003/`

Each run folder must contain:

- `README.md` (the filled-out run report)
- `raw/` (raw data files, unmodified)
- `processed/` (derived datasets created from raw)
- `plots/` (exported figures)
- `calibration/` (DAQ configs, calibration notes)
- `photos/` (fixture photos + post-test inspection photos)

Use the canonical template:
- `docs/10_Data_and_Results_Template.md`

## 2) Naming rules (so reviewers can audit quickly)
- `TEST_ID` must match the IDs defined in `docs/07_Test_Matrix.md` (e.g., `T-IMP-010`).
- `RUN_ID` must include:
  - date (YYYY-MM-DD)
  - coupon ID(s)
  - configuration (A/B/C/D)
  - any key parameter (e.g., impact energy label or pressure ΔP label)

Example RUN_ID pattern:
`RUN_YYYY-MM-DD_<COUPONID>_CFG-C_IMPACT-E2`

## 3) Data integrity rules
- Never edit raw files after capture. If correction is required, place corrected versions in `processed/` and explain in the run `README.md`.
- All plots must include labeled axes and units.
- If data is simulated, it must be labeled **SIMULATED** in:
  - the run `README.md` title line
  - a `SIMULATED_DATA_NOTICE.md` file inside the run folder

## 4) What “counts” as evidence in AHIS
A run counts as evidence only if:
- the run report is complete
- raw data exists and matches the described instrumentation
- processing steps are reproducible
- results are normalized by **areal density (kg/m²)** and **thickness (mm)** where applicable

## 5) What does NOT count
- screenshots without raw data
- plots without units
- claims without a mapped test ID and method
- fabricated numbers

---
This directory is intentionally strict. The point is to make external technical review possible without trust.
