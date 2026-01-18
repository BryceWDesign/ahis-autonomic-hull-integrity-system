# RUN_REAL_DATA_STARTER — T-IMP-010 (REAL DATA PLACEHOLDER)
**Status:** Ready for real data ingestion. No results until raw logs are present.

## Run metadata
- **Test ID:** T-IMP-010
- **Run ID:** RUN_REAL_DATA_STARTER
- **Date/Time (local):** ____________________
- **Operator:** ____________________
- **Location (lab/fixture):** ____________________

## Coupon metadata
- **Baseline coupon ID(s):** ____________________
- **AHIS coupon ID(s):** ____________________
- **Configuration(s):** A (Baseline) vs B (Passive) and/or C (Instrumented)
- **Measured thickness (mm):** Baseline ____ / AHIS ____
- **Measured mass (g):** Baseline ____ / AHIS ____
- **Coupon area (m²):** ____________________
- **Areal density (kg/m²):** Baseline ____ / AHIS ____

## Threat / environment declaration
- **Threat category:** low-velocity impact (PoC)
- **Temperature (°C):** ________
- **Notes:** ______________________________________________

## Fixture and boundary conditions (MANDATORY)
Attach photos in this folder’s `photos/`:
- Full fixture overview
- Close-up of clamps/edges
- Sensor routing and strain relief

Record:
- **Clamp condition:** ____________________
- **Clamp span (mm):** ____________________
- **Bolt torque (if used):** ____________________
- **Backing plate / pads (material + thickness):** ____________________

## Impact parameters (MANDATORY)
- **Striker geometry (shape + dimensions):** ____________________
- **Impact method:** drop height + mass OR actuator settings
- **Impact location (mm from center):** X ____ / Y ____
- **Repeats (N):** ________
- **Cooldown time between impacts:** ________

## Instrumentation
- **DAQ hardware:** ____________________
- **Sampling rate (Hz):** ____________________
- **Input ranges:** ____________________
- **Sensors used:** strain gauge / accelerometer / PVDF (circle)
- **Channel map:** __________________________________________

## Raw data (place files in `raw/`)
Put each impact time-series CSV in:
`results/T-IMP-010/RUN_REAL_DATA_STARTER/raw/`

Each CSV must include:
- a time column (seconds) (e.g., `time_s`)
- one or more metric columns (e.g., `strain_ue`, `accel_g`)

List raw files captured:
- __________________________________________
- __________________________________________

## Group map (required for baseline vs AHIS stats)
Create:
`results/T-IMP-010/RUN_REAL_DATA_STARTER/processed/impact_file_groups.csv`

Format:
```csv
filename,group
<file1>.csv,baseline
<file2>.csv,baseline
<file3>.csv,ahis
<file4>.csv,ahis
Panel metadata (required for normalization)

Create:
results/T-IMP-010/RUN_REAL_DATA_STARTER/processed/panel_metadata.csv

Required columns:
coupon_id,config,group,mass_g,area_m2,thickness_mm,notes

Processing steps (commands you ran)

1. Peak extraction:
python3 src/analysis/impact_peak_metrics.py \
  --input results/T-IMP-010/RUN_REAL_DATA_STARTER/raw \
  --output results/T-IMP-010/RUN_REAL_DATA_STARTER/processed \
  --time-col time_s \
  --metric strain_ue \
  --metric accel_g \
  --map results/T-IMP-010/RUN_REAL_DATA_STARTER/processed/impact_file_groups.csv

2. Normalization:
python3 src/analysis/normalization_utils.py \
  --input results/T-IMP-010/RUN_REAL_DATA_STARTER/processed/panel_metadata.csv \
  --output results/T-IMP-010/RUN_REAL_DATA_STARTER/processed/normalized_panel_metrics.csv

3. Delta report:
python3 src/analysis/delta_report_generator.py \
  --impact-stats results/T-IMP-010/RUN_REAL_DATA_STARTER/processed/impact_peak_group_stats.csv \
  --panel-metrics results/T-IMP-010/RUN_REAL_DATA_STARTER/processed/normalized_panel_metrics.csv \
  --out-dir results/T-IMP-010/RUN_REAL_DATA_STARTER/processed \
  --baseline-group baseline \
  --ahis-group ahis \
  --impact-metric strain_ue \
  --impact-metric accel_g

Results (do not fill until generated)

Generated report: processed/DELTA_REPORT.md

Key plots (if any): plots/

Post-impact photos: photos/

Damage extent (if also running T-IMP-011): ____________________

Confounders / deviations (mandatory)

This run package is valid evidence only when raw/ contains real captured logs and processed/ is generated from them with reproducible steps.

