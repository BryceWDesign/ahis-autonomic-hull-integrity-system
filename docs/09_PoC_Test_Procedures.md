# AHIS — Proof-of-Concept (PoC) Test Procedures
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** PoC procedures. Not flight-qualified. Not crew-rated.

---

## 0) Safety and scope notice
These procedures describe coupon-scale tests. They are intended to produce **repeatable measurements** and document failure modes.
They do not constitute certification or safety validation.

---

## 1) Test package rule (mandatory)
Every test run must produce a “results package” that includes:
- test ID, date/time, operator
- coupon IDs (baseline and AHIS) and configuration (A/B/C/D)
- fixture/boundary condition description + photos
- instrumentation list + calibration notes
- raw data + processed data + plots/tables
- observed failures and post-test inspection photos

Use `docs/10_Data_and_Results_Template.md` for the package structure.

---

## 2) Pre-test checklist (mandatory)
Before any test:
1) Verify coupon labeling and configuration
2) Record thickness (mm), mass (g), and compute areal density (kg/m²)
3) Visual inspection of edges, bondlines, electrodes, wiring
4) Instrumentation continuity check (instrumented mode)
5) Confirm DAQ settings (sampling rate, ranges, time sync)
6) Capture baseline noise dataset (instrumented mode)

If any item fails, log it and do not proceed until corrected.

---

## 3) Test procedures by category
### 3.1 T-IMP-010 / T-IMP-011 — Low-velocity impact
**Objective:** Compare baseline vs AHIS passive/instrumented coupons for:
- peak strain/accel deltas
- damage extent deltas

**Procedure (PoC):**
1) Mount coupon in a repeatable fixture. Document boundary conditions.
2) Place strain gauge(s) and/or accelerometer(s) consistently across coupons.
3) Define the impact energy or drop height and striker geometry.
4) Perform a minimum of N repeats (N is defined in the run plan; PoC default is “enough to show variance,” not a single hit).
5) Record time series during each impact.
6) Post-impact inspection:
   - photograph with scale reference
   - measure damage area using defined method

**Required outputs:**
- peak strain (µε) and peak acceleration (g) per run
- mean/variance comparison baseline vs AHIS
- damage photos and measured area table

**Notes:**
- Do not change fixture conditions between baseline and AHIS runs.
- If multiple impact locations are used, mark them and record coordinates.

---

### 3.2 T-FAT-020 — Cyclic durability (bondline/delamination trend)
**Objective:** Observe degradation and correlate to SHM drift.

**Procedure (PoC):**
1) Define cyclic loading profile (amplitude, frequency, cycles).
2) Apply cycles in batches with defined checkpoints (e.g., every X cycles).
3) At each checkpoint:
   - visual inspection
   - continuity checks (instrumented mode)
   - capture SHM baseline dataset (if instrumented)
   - optional FRF/impedance diagnostic sweep (if excitation mode is used)

**Required outputs:**
- checkpoint log including cycles-to-onset for any visible failure
- SHM drift plots vs cycle count
- documentation of failure mode (edge delamination, bondline failure, etc.)

---

### 3.3 T-THM-030 — Thermal cycling exposure
**Objective:** Quantify performance drift and baseline stability.

**Procedure (PoC):**
1) Define thermal profile (min/max temperature, dwell, ramp, cycle count).
2) Place coupons in chamber; log temperature at coupon or fixture where possible.
3) At defined cycle checkpoints:
   - remove (if required) and measure baseline SHM response (instrumented)
   - optionally rerun a small standardized impact or excitation check (consistent method)

**Required outputs:**
- drift summary (Δ feature) vs cycle count
- any material changes (warping, delamination, adhesive changes) documented

---

### 3.4 T-VIB-040 — Vibration survivability (instrumented mode)
**Objective:** Identify wiring/connector and sensor survivability issues.

**Procedure (PoC):**
1) Mount instrumented coupon in vibration fixture with defined orientation.
2) Apply defined vibration profile.
3) Pre/post comparisons:
   - continuity checks
   - baseline noise capture
   - diagnostic sweep if implemented

**Required outputs:**
- before/after signal quality metrics
- failure logs with photos (strain relief failures, connector issues)

---

### 3.5 T-PRS-050 — Pressure / leak tests (if performed)
**Objective:** Measure leak onset and leak rate; correlate detection timing (instrumented).

**Procedure (PoC):**
1) Define sealed test volume and coupon integration method (document leak paths and seals).
2) Calibrate pressure sensor/logger.
3) Establish initial pressure differential (declare value and units).
4) Monitor pressure decay over time.
5) If controlled damage introduction is used, record the method and timestamp.
6) For instrumented mode, record PVDF/SHM channels synchronized to pressure logs.

**Required outputs:**
- pressure vs time curve
- computed leak rate with method and uncertainty
- detection time relative to defined “leak onset” threshold

**Notes:**
- “Leak onset” must be explicitly defined (e.g., pressure decay rate exceeds threshold).
- Edge seals dominate results; document them thoroughly.

---

### 3.6 T-SHM-060 / T-SHM-062 — SHM detection + diagnostic excitation
**Objective:** Demonstrate repeatable detection and/or baseline tracking.

**Procedure (PoC):**
1) Record baseline dataset under controlled conditions.
2) Apply controlled events or excitation sweeps:
   - multi-tone, chirp, or swept-sine
   - record amplitude (Vpp), frequency plan, duration
3) Repeat runs to quantify variance.
4) Compare features to baseline; document drift with temperature if applicable.

**Required outputs:**
- feature definitions
- repeatability metrics (variance)
- detection thresholds and justification (PoC)

**Safety envelope:**
- Do not exceed the PVDF voltage envelope stated in legacy driver notes unless independently validated.
- Record actual outputs and temperature rise if measured.

---

## 4) Post-test inspection (mandatory)
After any mechanical or environmental test:
- visual inspection of edges, bondlines, electrodes, wiring
- photo documentation with scale reference
- continuity checks for instrumented coupons
- note any delamination initiation or growth

All failures must be categorized using `docs/06_Failure_Modes_and_Risks.md` identifiers where possible.

---

## 5) Reporting rule
A test is not “complete” until the repo contains:
- raw data
- processed data
- plots/tables
- calibration notes
- and an interpretation section that explicitly states limitations and confounders

Cross-reference:
- Requirements: `docs/03_Requirements_and_Acceptance_Criteria.md`
- Test matrix: `docs/07_Test_Matrix.md`
- Results template: `docs/10_Data_and_Results_Template.md`

---
End of PoC test procedures.
