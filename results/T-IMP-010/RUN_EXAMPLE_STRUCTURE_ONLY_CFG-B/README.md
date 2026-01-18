# RUN_EXAMPLE_STRUCTURE_ONLY_CFG-B — STRUCTURE ONLY (NO DATA)
**Test ID:** T-IMP-010  
**Status:** This run package is a **structure example only**. It contains **no raw data** and must not be interpreted as evidence.

This folder exists to show contributors exactly how an AHIS run package is organized.

---

## Run metadata
- **Test ID:** T-IMP-010
- **Run ID:** RUN_EXAMPLE_STRUCTURE_ONLY_CFG-B
- **Date/Time (local):** N/A (example)
- **Operator:** N/A
- **Location (lab/fixture):** N/A

## Coupon metadata
- **Baseline coupon ID(s):** TBD
- **AHIS coupon ID(s):** TBD
- **Configuration(s):** B (AHIS Passive) *(example)*
- **Measured thickness (mm):** TBD
- **Measured mass (g):** TBD
- **Coupon area (m²):** TBD
- **Areal density (kg/m²):** TBD

## Build traceability
- **Build log reference:** TBD
- **Materials / batches:** TBD
- **Bonding / cure schedule:** TBD

## Threat / environment declaration
- **Threat category:** low-velocity impact
- **Environment conditions:** TBD (temperature, etc.)
- **Out-of-scope notes:** hypervelocity MMOD not in PoC scope

## Fixture and boundary conditions
- **Fixture description:** TBD
- **Mounting method:** TBD
- **Boundary condition notes:** TBD
- **Photos:** (place fixture photos in `photos/`)

## Instrumentation
- **DAQ hardware:** TBD
- **Sampling rate (Hz):** TBD
- **Input ranges:** TBD
- **Sensors:** (strain gauge / accelerometer) TBD
- **Channel map:** TBD

## Calibration and verification
- **Calibration files:** (place in `calibration/`)
- **Pre-test checks performed:** TBD
- **Baseline dataset file(s):** TBD

## Procedure summary
- **Procedure followed:** See `docs/09_PoC_Test_Procedures.md` (Impact section)
- **Key parameters:** striker geometry, impact energy method, impact coordinates (all TBD)
- **Deviations:** none (example)

## Raw data
Place raw CSV files in `raw/` (unmodified).
- **Raw file list:** none (example)
- **Time synchronization:** N/A

## Processing steps
Place processed outputs in `processed/` and document how they were produced.
- **Script(s) used:** e.g., `src/analysis/impact_peak_metrics.py`
- **Processing parameters:** time column, metric columns (TBD)
- **Assumptions:** none (example)

## Metrics and results
No results. This is a structure-only example.

## Pass/Fail vs acceptance criteria
Not applicable (no data).

## Failure modes observed
Not applicable (no test performed).

## Limitations and confounders
Not applicable (no test performed).

## Conclusions
This folder demonstrates the required run package structure only.
No claims may be derived from it.
