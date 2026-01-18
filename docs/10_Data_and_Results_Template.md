# AHIS — Data and Results Template (Required Format)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** PoC reporting template. Not flight-qualified. Not crew-rated.

---

## 1) Purpose
This template defines the minimum structure for any AHIS results package.
If results cannot be reproduced from the included raw data and notes, they do not count.

---

## 2) Directory layout (required)
Create a folder for each test run:

`results/<TEST_ID>/<RUN_ID>/`

Example:
- `results/T-IMP-010/RUN_2026-01-12_AHIS-PANEL-003/`

Inside each run folder:

- `README.md` (this report, filled out)
- `raw/` (raw logs, unmodified)
- `processed/` (derived datasets)
- `plots/` (exported plots/images)
- `calibration/` (calibration notes, config dumps)
- `photos/` (fixture and post-test inspection photos)

---

## 3) Run report template (copy/paste below into results/<TEST_ID>/<RUN_ID>/README.md)
## Run metadata
- **Test ID:**  
- **Run ID:**  
- **Date/Time (local):**  
- **Operator:**  
- **Location (lab/fixture):**  

## Coupon metadata
- **Baseline coupon ID(s):**  
- **AHIS coupon ID(s):**  
- **Configuration(s):** (A=Baseline, B=Passive, C=Instrumented, D=Instrumented+Excitation)  
- **Measured thickness (mm):**  
- **Measured mass (g):**  
- **Coupon area (m²):**  
- **Areal density (kg/m²):**  

## Build traceability
- **Build log reference:** (link or identifier)
- **Materials / batches:** (record identifiers; do not guess)
- **Bonding / cure schedule:** (time/temp/steps)

## Threat / environment declaration
- **Threat category:** (impact, fatigue, thermal, vibration, pressure/leak, SHM diagnostics)  
- **Environment conditions:** (temperature, humidity if relevant, chamber settings, etc.)  
- **Out-of-scope notes:** (anything not controlled)

## Fixture and boundary conditions
- **Fixture description:**  
- **Mounting method:**  
- **Boundary condition notes:** (clamped edges, free edges, bolt torque if used)  
- **Photos:** (list files in `photos/`)

## Instrumentation
List every sensor/channel.
- **DAQ hardware:**  
- **Sampling rate (Hz):**  
- **Input ranges:**  
- **Filters (if any):**  
- **Sensors:** (PVDF nodes, strain gauges, accelerometers, pressure sensors)  
- **Channel map:** (channel → sensor → location)

## Calibration and verification
- **Calibration files:** (list in `calibration/`)  
- **Pre-test checks performed:** (continuity, baseline noise capture, etc.)  
- **Baseline dataset file(s):**  

## Procedure summary
- **Procedure followed:** (reference to `docs/09_PoC_Test_Procedures.md` section)  
- **Key parameters:** (impact energy, cycle count, vibration profile, pressure differential, excitation plan)  
- **Deviations:** (must be explicitly listed)

## Raw data
- **Raw file list:** (what’s in `raw/`)  
- **Time synchronization:** (how timestamps align across channels)

## Processing steps
Describe exactly how `processed/` and `plots/` were generated.
- **Script(s) used:** (path + version/hash if available)
- **Processing parameters:** (windowing, thresholds, feature extraction)
- **Assumptions:** (units, offsets, coordinate mapping)

## Metrics and results (required)
Report metrics with units, uncertainty if known, and comparative baseline vs AHIS.

### Primary metrics (examples; choose those relevant)
- Peak strain (µε): baseline vs AHIS  
- Peak acceleration (g): baseline vs AHIS  
- Damage area (cm²): baseline vs AHIS  
- Leak rate (Pa/s or sccm): baseline vs AHIS  
- Detection time (s):  
- Localization error (cm):  
- Baseline drift (Δ feature):  

### Normalization (mandatory)
- **Δ per areal density (kg/m²):**  
- **Δ per thickness (mm):**  

## Pass/Fail vs acceptance criteria
- **Acceptance criteria reference:** (`docs/03_Requirements_and_Acceptance_Criteria.md`)  
- **Result:** Pass / Fail / TBD (with explanation)

## Failure modes observed (required if any)
Reference `docs/06_Failure_Modes_and_Risks.md` identifiers when possible:
- Observed failure mode(s):  
- Onset conditions:  
- Photos:  

## Limitations and confounders (mandatory)
List anything that could invalidate interpretation:
- fixture variability
- temperature drift
- sensor placement uncertainty
- insufficient repeats
- uncontrolled boundary conditions

## Conclusions (conservative, PoC-appropriate)
- What was actually shown by the data (no extrapolation)
- What remains unknown
- What should be tested next

---

## 4) Required file formats
- Raw data: CSV or simple binary with reader notes
- Plots: PNG (include axis labels and units)
- Photos: JPG/PNG with scale references where relevant
- Keep filenames descriptive and include coupon IDs where possible.

---
End of results template.
