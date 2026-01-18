# AHIS — Delta Report (PoC) — SIMULATED DEMO
**Status:** SIMULATED output to validate the analysis pipeline format. Not measured data. Not flight-qualified. Not crew-rated.

## Panel Normalization (Measured)
- Baseline group: n=2, mean areal density=12.34 kg/m², mean thickness=2.10 mm
- AHIS group: n=2, mean areal density=16.52 kg/m², mean thickness=3.05 mm

## Impact Peaks (Magnitude) — Baseline vs AHIS

### Metric: `strain_ue`
- Baseline: n=2, mean|peak|=2269.626, std=6.00213
- AHIS: n=2, mean|peak|=1809.471, std=8.87827
- Δ(mean|peak|) = -460.155 (AHIS − Baseline)
- Normalized Δ per AHIS areal density = -27.8544 / (kg/m²)
- Normalized Δ per AHIS thickness = -150.871 / mm

### Metric: `accel_g`
- Baseline: n=2, mean|peak|=56.761, std=0.26144
- AHIS: n=2, mean|peak|=45.543, std=0.14365
- Δ(mean|peak|) = -11.2180 (AHIS − Baseline)
- Normalized Δ per AHIS areal density = -0.679056 / (kg/m²)
- Normalized Δ per AHIS thickness = -3.67804 / mm

## Interpretation Discipline
- This report summarizes processed datasets only; it does not certify safety or mission readiness.
- Any confounders (fixture changes, temperature drift, insufficient repeats) must be stated in the run package README.
