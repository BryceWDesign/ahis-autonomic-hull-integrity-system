# AHIS — Run Plan: Baseline vs AHIS (PoC Minimum Viable Evidence)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** PoC run plan. Not flight-qualified. Not crew-rated.

---

## 0) Purpose
This run plan defines the **minimum** set of controlled experiments that produces the kind of data a SpaceX engineer will actually read:
- clear boundary conditions
- repeatability/variance
- normalized deltas per kg/m² and per mm
- explicit limitations

This plan does not fabricate results. It defines how to produce them.

---

## 1) What “success” means for this plan (PoC-level)
A successful execution produces at least:
- one complete impact dataset package (T-IMP-010) with repeats and variance, baseline vs AHIS
- optional but strongly recommended: one pressure/leak dataset package (T-PRS-050)
- a one-page delta summary built from real measurements (generated later by analysis scripts)

---

## 2) Coupon configurations (required)
Build and label at least these configurations:

### Config A — Baseline
- Substrate only
- Surface prep documented

### Config B — AHIS Passive
- Baseline + passive rate-dependent interlayer
- Edge sealing method documented (even if “none”)

### Config C — AHIS Instrumented (recommended for SHM)
- Config B + PVDF SHM skin + routing + strain relief
- Baseline noise capture required

> If you cannot build C initially, you can still run a credible Phase-1 dataset with A vs B.

---

## 3) Coupon count and repeats (minimum)
To avoid “one-off” results, you need repeats at two levels:
- across impacts on the same coupon (within-coupon repeatability)
- across at least two coupons per configuration (between-coupon variability)

### Minimum starting point (Phase 1)
- Config A: 2 coupons
- Config B: 2 coupons
- Each coupon: N impact repeats (N = TBD; must be enough to show variance; do not publish single-hit conclusions)

Record N explicitly in each run package.

---

## 4) Pre-run measurement requirements (mandatory)
Before testing each coupon:
- measure thickness (mm)
- measure mass (g)
- measure area (m²)
- compute areal density (kg/m²)
- photograph edges and bondlines with a scale reference

Instrumented mode (Config C):
- continuity check of PVDF/electrodes
- baseline noise capture dataset
- document DAQ settings (range, sampling rate)

---

## 5) Test 1 — T-IMP-010 (Impact: peak strain/accel delta) — REQUIRED
### 5.1 Boundary conditions (must be identical for A and B/C)
- Choose a single fixture and clamp condition and do not change it.
- Document per `docs/15_Fixture_and_Boundary_Conditions.md`.

### 5.2 Instrumentation (choose what you actually have; do not guess)
Minimum acceptable:
- either strain gauge(s) OR accelerometer(s) with timestamped DAQ

Recommended:
- strain gauge(s) + accelerometer(s) synchronized

### 5.3 Impact parameters (must be explicitly declared)
- striker geometry (shape + dimensions)
- impact energy control method (drop height + mass, or actuator settings)
- impact location coordinates on coupon (mm)
- cooldown time between repeats (if any)

### 5.4 Outputs (must be computed and reported)
For each impact:
- peak strain (µε) and/or peak acceleration (g)
- time series plots with units
Across repeats:
- mean and variance for baseline vs AHIS
- normalized delta per areal density and thickness

Store run packages under:
- `results/T-IMP-010/<RUN_ID>/...`

---

## 6) Test 2 — T-IMP-011 (Impact: damage extent) — STRONGLY RECOMMENDED
Run in parallel with T-IMP-010 if possible.

### Outputs
- photos with scale
- damage area (cm²) measured by a defined method
- failure mode classification (edge delamination, bondline failure, cracking, etc.)

---

## 7) Test 3 — T-PRS-050 (Pressure/leak) — OPTIONAL BUT HIGH VALUE
Pressure boundary integrity is where reviewers get serious fast.

### 7.1 Fixture requirements
- sealed test volume method must be documented
- seal type and clamp method documented
- pressure sensor calibration/config logged

### 7.2 Leak onset definition (mandatory)
Each run must define leak onset as:
- pressure decay rate threshold (Pa/s) over a time window, OR
- flow threshold (sccm) over a time window

### Outputs
- pressure vs time curve
- computed leak rate with method
- (if instrumented) detection time relative to leak onset

Store run packages under:
- `results/T-PRS-050/<RUN_ID>/...`

---

## 8) Environmental controls (declare what you can actually control)
At minimum, record:
- temperature at time of test (°C)
Optional:
- humidity, chamber profile (for thermal cycling)

Do not imply thermal/vacuum relevance without running those tests.

---

## 9) Reporting requirements (what makes it “reviewable”)
Every run package must:
- include raw data unmodified
- include processed outputs with reproducible steps
- include calibration notes
- declare confounders and deviations

Use:
- `docs/10_Data_and_Results_Template.md`

---

## 10) Immediate next step after data exists
Once the first real datasets exist, AHIS should produce a single-page summary:
- Δpeak strain (µε) and/or Δpeak accel (g)
- Δdamage area (cm²) (if measured)
- Δleak rate (if measured)
- normalized per kg/m² and per mm
- number of repeats and variance

(Analysis scripts and the delta report template are added in subsequent commits.)

---
End of run plan.
