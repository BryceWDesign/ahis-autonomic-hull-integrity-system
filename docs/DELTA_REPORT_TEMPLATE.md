# AHIS — Delta Report (PoC) Template
**Status:** Template only. Not measured data. Not flight-qualified. Not crew-rated.

This file is a **human-readable template** that mirrors the structure produced by:
- `src/analysis/delta_report_generator.py`

Use this when you want to:
- review the expected report format before data exists, or
- hand-edit a draft summary **only after** you have real processed outputs.

**Rule:** Do not publish numeric deltas as “measured” unless they were generated from a real run package
with raw files in `results/<TEST_ID>/<RUN_ID>/raw/` and processing documented in that run’s README.

---

## Run References
- Impact run package: `results/T-IMP-010/<RUN_ID>/`
- Panel metrics: `results/T-IMP-010/<RUN_ID>/processed/normalized_panel_metrics.csv`
- Impact grouped stats: `results/T-IMP-010/<RUN_ID>/processed/impact_peak_group_stats.csv`
- (Optional) Leak run package: `results/T-PRS-050/<LEAK_RUN_ID>/`

---

## Panel Normalization (Measured)
- Baseline group: n=**TBD**, mean areal density=**TBD** kg/m², mean thickness=**TBD** mm
- AHIS group: n=**TBD**, mean areal density=**TBD** kg/m², mean thickness=**TBD** mm

Notes:
- Values must be measured (mass, area, thickness). No estimates.
- Groups must match the labels used in `panel_metadata.csv` (e.g., baseline, ahis).

---

## Impact Peaks (Magnitude) — Baseline vs AHIS

### Metric: `strain_ue` *(if recorded)*
- Baseline: n=**TBD**, mean|peak|=**TBD**, std=**TBD**
- AHIS: n=**TBD**, mean|peak|=**TBD**, std=**TBD**
- Δ(mean|peak|) = **TBD** (AHIS − Baseline)
- Normalized Δ per AHIS areal density = **TBD** / (kg/m²)
- Normalized Δ per AHIS thickness = **TBD** / mm

### Metric: `accel_g` *(if recorded)*
- Baseline: n=**TBD**, mean|peak|=**TBD**, std=**TBD**
- AHIS: n=**TBD**, mean|peak|=**TBD**, std=**TBD**
- Δ(mean|peak|) = **TBD** (AHIS − Baseline)
- Normalized Δ per AHIS areal density = **TBD** / (kg/m²)
- Normalized Δ per AHIS thickness = **TBD** / mm

---

## Pressure/Leak (Optional)
Include only if `T-PRS-050` was executed and processed outputs exist.
- Leak onset time (s): **TBD** (threshold=**TBD** per s, window=**TBD** s)
- Mean dP/dt over onset window: **TBD** per s
- Median dP/dt over onset window: **TBD** per s

---

## Confounders / Limitations (Mandatory)
- Fixture/boundary condition differences: **TBD**
- Temperature drift during runs: **TBD**
- Sensor placement uncertainty: **TBD**
- Repeat count adequacy: **TBD**
- Edge seal leakage vs coupon leakage (pressure tests): **TBD**

---

## Interpretation Discipline
- This report summarizes **processed datasets only**; it does not certify safety or mission readiness.
- Any claim must cite the corresponding run package README and raw files.
- If repeats/variance are insufficient, results must be labeled “preliminary.”

---
End of template.
