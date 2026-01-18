# AHIS — Delta Report (PoC)
**Status:** Proof-of-Concept summary. Not flight-qualified. Not crew-rated.  
**Source:** This report must be generated from run packages in `results/` with raw data + processed outputs.

## Run References
- Impact run package: `results/T-IMP-010/<RUN_ID>/`
- Panel metadata: `results/T-IMP-010/<RUN_ID>/processed/normalized_panel_metrics.csv`
- Impact grouped stats: `results/T-IMP-010/<RUN_ID>/processed/impact_peak_group_stats.csv`
- (Optional) Leak run package: `results/T-PRS-050/<LEAK_RUN_ID>/`

---

## Panel Normalization (Measured)
- Baseline group: n=**TBD**, mean areal density=**TBD** kg/m², mean thickness=**TBD** mm
- AHIS group: n=**TBD**, mean areal density=**TBD** kg/m², mean thickness=**TBD** mm

**Notes:** Values must be measured (mass, area, thickness). No estimates.

---

## Impact Peaks (Magnitude) — Baseline vs AHIS

### Metric: `strain_ue` (µε)  *(if recorded)*
- Baseline: n=**TBD**, mean|peak|=**TBD**, std=**TBD**
- AHIS: n=**TBD**, mean|peak|=**TBD**, std=**TBD**
- Δ(mean|peak|) = **TBD** (AHIS − Baseline)
- Normalized Δ per AHIS areal density = **TBD** / (kg/m²)
- Normalized Δ per AHIS thickness = **TBD** / mm

### Metric: `accel_g` (g)  *(if recorded)*
- Baseline: n=**TBD**, mean|peak|=**TBD**, std=**TBD**
- AHIS: n=**TBD**, mean|peak|=**TBD**, std=**TBD**
- Δ(mean|peak|) = **TBD** (AHIS − Baseline)
- Normalized Δ per AHIS areal density = **TBD** / (kg/m²)
- Normalized Δ per AHIS thickness = **TBD** / mm

---

## Pressure/Leak (Optional)
*(Only include if `T-PRS-050` was executed and processed outputs exist.)*
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
End of report.
