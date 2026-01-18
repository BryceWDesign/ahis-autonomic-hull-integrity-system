# AHIS — Analysis Pipeline Walkthrough (PoC)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** PoC workflow documentation. Not flight-qualified. Not crew-rated.

---

## 0) Purpose
This walkthrough explains exactly how to go from:
- raw test logs (CSV)
to:
- processed peak metrics, leak metrics (optional),
- normalization (kg/m², mm),
- and a one-page delta summary (`DELTA_REPORT.md`)

No numbers are invented. This pipeline only processes what you provide.

---

## 1) Prerequisites
- Python 3 installed
- Raw data exported as CSV files with headers
- You must know your column names (this pipeline does not guess units)

Recommended folder convention:
- `results/<TEST_ID>/<RUN_ID>/raw/` contains the raw CSVs
- outputs go to `results/<TEST_ID>/<RUN_ID>/processed/`

---

## 2) Prepare the run package folders
Create a run folder using the required structure:

`results/<TEST_ID>/<RUN_ID>/`

Inside it, create:
- `raw/`
- `processed/`
- `plots/` (optional; not used by current scripts)
- `calibration/`
- `photos/`

Fill out the run report:
- `results/<TEST_ID>/<RUN_ID>/README.md` using `docs/10_Data_and_Results_Template.md`

---

## 3) Impact pipeline (T-IMP-010)
### 3.1 Place raw CSV files
Put each impact time-series CSV in:
- `results/T-IMP-010/<RUN_ID>/raw/`

Each CSV must include:
- a time column (seconds) — default name expected: `time_s`
- one or more metric columns, e.g.:
  - `strain_ue` (microstrain, µε) OR your own name
  - `accel_g` (g) OR your own name

If your column names differ, you will pass them explicitly on the command line.

### 3.2 (Optional) Create a file-to-group mapping
If you want baseline vs AHIS grouped statistics, create:

`results/T-IMP-010/<RUN_ID>/processed/impact_file_groups.csv`

Format (required header):
```csv
filename,group
hit1.csv,baseline
hit2.csv,baseline
hit3.csv,ahis
hit4.csv,ahis
The filename must match the CSV basename in raw/.

3.3 Run peak extraction

From repo root, run:
python3 src/analysis/impact_peak_metrics.py \
  --input results/T-IMP-010/<RUN_ID>/raw \
  --output results/T-IMP-010/<RUN_ID>/processed \
  --time-col time_s \
  --metric strain_ue \
  --metric accel_g \
  --map results/T-IMP-010/<RUN_ID>/processed/impact_file_groups.csv

Outputs:

processed/impact_peak_summary.csv

processed/impact_peak_group_stats.csv (only if --map is provided)

If you do not have one of the metrics (e.g., no accelerometer), remove that --metric line.

4) Panel normalization (kg/m², mm)
4.1 Create panel metadata CSV

Create:

results/T-IMP-010/<RUN_ID>/processed/panel_metadata.csv

Required columns:

coupon_id

config

group

area_m2

thickness_mm

either mass_g or mass_kg

Example:
coupon_id,config,group,mass_g,area_m2,thickness_mm,notes
AHIS-PANEL-001,A,baseline,123.4,0.0100,2.10,baseline coupon
AHIS-PANEL-002,B,ahis,165.2,0.0100,3.05,passive layer added

4.2 Run normalization
python3 src/analysis/normalization_utils.py \
  --input results/T-IMP-010/<RUN_ID>/processed/panel_metadata.csv \
  --output results/T-IMP-010/<RUN_ID>/processed/normalized_panel_metrics.csv
Output:

processed/normalized_panel_metrics.csv

5) Optional leak pipeline (T-PRS-050)

This section applies only if you ran a pressure/leak test.

5.1 Place raw pressure log

Place a single pressure log CSV in:

results/T-PRS-050/<RUN_ID>/raw/pressure_log.csv (name optional)

CSV must include:

time column in seconds (default expected: time_s)

pressure column (default expected: pressure_pa)
Units must be consistent; thresholds must match your units.

5.2 Run leak metrics with explicit onset rule

You must choose:

--rate-threshold (positive number; applied as dp/dt <= -threshold)

--window-seconds (continuous duration for onset)

Example:
python3 src/analysis/leak_rate_metrics.py \
  --input results/T-PRS-050/<RUN_ID>/raw/pressure_log.csv \
  --output results/T-PRS-050/<RUN_ID>/processed \
  --time-col time_s \
  --pressure-col pressure_pa \
  --rate-threshold 5.0 \
  --window-seconds 2.0
Outputs:

processed/leak_rate_timeseries.csv

processed/leak_onset_summary.csv

processed/leak_rate_summary.csv

6) Generate the one-page delta report (engineering summary)

This step produces the “Elon page” from processed data.

Minimum required inputs:

impact_peak_group_stats.csv

normalized_panel_metrics.csv

Optional:

leak_onset_summary.csv

leak_rate_summary.csv

Run:
python3 src/analysis/delta_report_generator.py \
  --impact-stats results/T-IMP-010/<RUN_ID>/processed/impact_peak_group_stats.csv \
  --panel-metrics results/T-IMP-010/<RUN_ID>/processed/normalized_panel_metrics.csv \
  --out-dir results/T-IMP-010/<RUN_ID>/processed \
  --baseline-group baseline \
  --ahis-group ahis \
  --impact-metric strain_ue \
  --impact-metric accel_g

Optional leak inputs:
  --leak-onset results/T-PRS-050/<LEAK_RUN_ID>/processed/leak_onset_summary.csv \
  --leak-rate  results/T-PRS-050/<LEAK_RUN_ID>/processed/leak_rate_summary.csv

Outputs:

processed/DELTA_REPORT.md

processed/delta_report_values.csv

7) Common failure points (and what they mean)

“Missing column …”
Your CSV headers don’t match the column names you passed. Fix the CLI args or rename headers.

“Time column must be strictly increasing”
Your time series has duplicate or out-of-order timestamps. Fix export or resample.

“No leak onset found …”
Your threshold/window is too strict or units don’t match. Adjust thresholds or verify units.

“Group map missing entries …”
Your impact_file_groups.csv doesn’t include all files in raw/. Add mappings or remove --map.

8) Discipline rule (required)

These scripts do not validate safety. They produce auditable metrics and deltas.
Any conclusions must:

cite the run packages

list confounders

avoid operational claims unless proven by additional testing

End of analysis pipeline walkthrough.
