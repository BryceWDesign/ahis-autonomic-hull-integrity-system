# AHIS — Requirements and Acceptance Criteria (PoC)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Proof-of-Concept (PoC). Not flight-qualified. Not crew-rated.

---

## 1) How to use this document
This document defines **measurable** PoC requirements and pass/fail criteria.
- All requirements must be evaluated under explicitly stated test conditions.
- Where numeric thresholds are not yet justified by data, they are marked **TBD** and must be replaced after initial baseline testing.
- Requirements are reported normalized by **areal density (kg/m²)** and **thickness (mm)** where applicable.

---

## 2) Definitions
- **Baseline panel:** structural substrate with standard bonding/finish but **without** AHIS layers.
- **AHIS panel:** baseline panel plus AHIS passive layer and/or PVDF SHM skin (as defined per test).
- **Event detection:** identifying that a damage-relevant event occurred.
- **Localization:** estimating the region of damage with a defined error bound.

---

## 3) Requirements (PoC)
### RQ-001 — Documentation traceability (mandatory)
**Requirement:** Every claim in AHIS docs must map to:
- metric + units
- test method + instrumentation
- acceptance criteria

**Acceptance:** 100% of “claims” sections in docs have those elements or are labeled **Hypothesis**.

---

### RQ-010 — Passive layer: impulsive event strain reduction (PoC)
**Requirement:** Under a defined low-velocity impact test, AHIS passive configuration should reduce peak strain transmitted to the substrate relative to baseline.

**Metric:** Peak substrate strain (microstrain, µε) or equivalent strain-gauge output.  
**Acceptance:** Threshold **TBD** after baseline; initial target is “detectable improvement” with full reporting of uncertainty.  
**Notes:** This requirement is comparative; success requires repeatability and statistical reporting, not one-off wins.

---

### RQ-011 — Passive layer: damage extent reduction (PoC)
**Requirement:** Under the same defined impact test, AHIS passive configuration should reduce damage extent relative to baseline.

**Metric:** Damage area (cm²) or delamination indicator (NDT proxy) under defined inspection method.  
**Acceptance:** Threshold **TBD** after baseline; initial target is “reduced area” with repeatability and documentation of failure mode.

---

### RQ-020 — Pressure boundary integrity: leak onset detection (PoC)
**Requirement:** If a pressure boundary test is performed, the system must detect leak onset (instrumented mode) and report the event timestamp.

**Metric:** Detection time (s) relative to measured leak onset signal.  
**Acceptance:** **TBD** after selecting leak test apparatus and signal definition.  
**Notes:** Leak onset definition must be explicitly stated (e.g., pressure decay rate exceeding threshold).

---

### RQ-021 — Pressure boundary integrity: leak rate reporting (PoC)
**Requirement:** Leak rate must be measured and reported for baseline and AHIS panels under identical conditions.

**Metric:** Pressure decay (Pa/s), leak rate (sccm), or equivalent standard.  
**Acceptance:** Not a “pass/fail” at PoC stage unless a mission threshold is declared; mandatory is accurate measurement + uncertainty reporting.

---

### RQ-030 — SHM sensing: event detection (instrumented mode)
**Requirement:** PVDF SHM skin must detect defined impact/strain events above noise floor.

**Metric:** Detection sensitivity (signal-to-noise ratio), false negative rate.  
**Acceptance:** Demonstrate detection of controlled events with repeatability; statistical threshold **TBD** after baseline noise characterization.

---

### RQ-031 — SHM localization: damage region estimate (instrumented mode)
**Requirement:** If localization is implemented, the system must estimate damage region within a defined error bound.

**Metric:** Localization error (cm) relative to known impact/damage location.  
**Acceptance:** **TBD** after selecting panel size and sensor node spacing.  
**Notes:** Localization method must be documented (triangulation, model-based inversion, time-of-flight, etc.).

---

### RQ-032 — SHM baseline stability: environmental drift (instrumented mode)
**Requirement:** SHM baseline must remain usable after environmental exposure defined in tests.

**Metric:** Baseline drift (Δ) in impedance/FRF features vs temperature cycle count.  
**Acceptance:** **TBD** after selecting environment profile; mandatory is to quantify drift and document compensation strategy (if any).

---

### RQ-040 — Diagnostic excitation safety envelope (instrumented + excitation mode)
**Requirement:** Diagnostic excitation must remain within safe electrical limits for PVDF and the PoC driver hardware.

**Metric:** Peak-to-peak voltage (Vpp), current (mA), duty cycle, and temperature rise (°C).  
**Acceptance:** Do not exceed the PVDF drive envelope stated in the legacy driver notes unless independently validated; log and report actual outputs.

---

### RQ-050 — Mass and thickness accounting (mandatory)
**Requirement:** Any AHIS configuration must report:
- areal density (kg/m²)
- thickness (mm)
- added mass fraction (%)

**Acceptance:** 100% of PoC builds include measured values, not estimates.

---

### RQ-060 — Data integrity and reproducibility (mandatory)
**Requirement:** Every results package must include:
- raw data
- processed data
- calibration notes
- units and sampling rates
- scripts used to generate plots/tables (if applicable)

**Acceptance:** Reviewer can reproduce plots/tables from raw data using included scripts or documented steps.

---

## 4) Acceptance criteria policy (how TBD values become fixed)
1) Establish baseline distributions (mean/variance) for key metrics.
2) Set thresholds using:
   - mission-relevant constraints (if declared), or
   - statistical effect sizes (PoC), and
   - explicit safety margins only when justified by data.

No threshold may be presented as “crew-safety” without external validation.

---

## 5) Requirement-to-test mapping
All requirements must map to the test matrix:
- See `docs/07_Test_Matrix.md` for the claim/metric/instrument mapping.

---
End of requirements and acceptance criteria.
