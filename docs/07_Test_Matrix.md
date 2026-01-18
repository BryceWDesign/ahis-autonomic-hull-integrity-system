# AHIS — Test Matrix (Claim → Metric → Method → Pass/Fail)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Proof-of-Concept (PoC). Not flight-qualified. Not crew-rated.

---

## 1) How to use this matrix
This is the repository’s “audit spine.” For every claim or requirement, this matrix defines:
- **Metric + units**
- **Test method**
- **Instrumentation**
- **Data products**
- **Acceptance criteria**

**Rule:** If a requirement is not mapped here, it is not an AHIS claim.

---

## 2) Test IDs and conventions
- **T-IMP-*** : Impact / shock tests
- **T-FAT-*** : Fatigue / cyclic durability
- **T-THM-*** : Thermal / environmental exposure
- **T-VIB-*** : Vibration tests
- **T-PRS-*** : Pressure / leak tests
- **T-SHM-*** : SHM-specific diagnostics
- **T-EMI-*** : EMI/ESD robustness tests
- **T-QA-***  : Documentation / reproducibility checks

Baseline condition:
- For comparative tests, measure **Baseline panel** and **AHIS panel** under identical conditions.

---

## 3) Matrix
### T-QA-001 — Documentation traceability audit
- **Maps to:** RQ-001
- **Metric:** % of claims with metric+method+acceptance (unitless)
- **Method:** Doc review against required fields; spot-check links
- **Instrumentation:** N/A
- **Data products:** audit checklist
- **Acceptance:** 100% compliance or claim labeled “Hypothesis”

---

### T-IMP-010 — Low-velocity impact: peak strain/accel delta (Passive Mode)
- **Maps to:** RQ-010
- **Metric:** peak substrate strain (µε), peak acceleration (g)
- **Method:** controlled low-velocity impact on coupon; fixed boundary condition
- **Instrumentation:** strain gauge and/or accelerometer; DAQ with timestamping
- **Data products:** time series + summary stats; calibration metadata
- **Acceptance:** threshold TBD after baseline; must show repeatable comparative deltas

---

### T-IMP-011 — Impact damage extent comparison (Passive Mode)
- **Maps to:** RQ-011
- **Metric:** damage area (cm²) or delamination proxy (defined method)
- **Method:** post-impact inspection using defined protocol (photo + measurement method)
- **Instrumentation:** inspection tools (camera, scale reference); optional NDT if available
- **Data products:** images + measured area table; notes
- **Acceptance:** threshold TBD; must document failure mode and repeatability

---

### T-FAT-020 — Cyclic durability: bondline and delamination trend
- **Maps to:** FM-P004, FM-S003, RQ-060 (data integrity)
- **Metric:** stiffness/FRF feature drift; visible delamination; sensor continuity
- **Method:** apply cyclic loading for defined cycles; periodic inspection checkpoints
- **Instrumentation:** optional accelerometer/FRF setup; continuity meter; inspection
- **Data products:** checkpoint logs; drift plots; photos
- **Acceptance:** PoC acceptance TBD; must report failure onset and cycles-to-failure

---

### T-THM-030 — Thermal cycling exposure (Passive + Instrumented Modes)
- **Maps to:** FM-P001, FM-S001, RQ-032
- **Metric:** performance drift (Δ peak strain/accel; Δ SHM features) vs cycles
- **Method:** thermal chamber cycling using declared profile; re-run baseline checks
- **Instrumentation:** temperature logger; DAQ for SHM and/or strain/accel
- **Data products:** pre/post and periodic baselines; drift summary
- **Acceptance:** TBD; mandatory is quantification + drift/compensation discussion

---

### T-VIB-040 — Vibration survivability (Instrumented Mode)
- **Maps to:** FM-S004, FM-SYS002
- **Metric:** continuity failures; noise increase; response repeatability
- **Method:** vibration exposure using defined profile; pre/post diagnostics
- **Instrumentation:** shaker + accelerometers; continuity checks; SHM recordings
- **Data products:** before/after comparison; failure log
- **Acceptance:** TBD; must not lose basic measurement capability without documentation

---

### T-PRS-050 — Pressure boundary: leak onset and leak rate
- **Maps to:** RQ-020, RQ-021, FM-SYS002
- **Metric:** leak rate (Pa/s or sccm); detection time (s)
- **Method:** sealed test volume or coupon fixture; controlled damage introduction (if used)
- **Instrumentation:** pressure sensor + logger; optional flow meter; timestamped SHM channels
- **Data products:** pressure decay curves; leak rate computation; detection time report
- **Acceptance:** detection threshold TBD; leak reporting mandatory with uncertainty

---

### T-SHM-060 — Event detection performance (Instrumented Mode)
- **Maps to:** RQ-030
- **Metric:** SNR; false positive/negative rates (PoC scale)
- **Method:** controlled event set (impacts/strain pulses) with known timing
- **Instrumentation:** PVDF channels + DAQ; optional accelerometer reference
- **Data products:** labeled dataset; threshold selection notes; performance summary
- **Acceptance:** TBD; must demonstrate repeatability and documented thresholds

---

### T-SHM-061 — Localization accuracy (Instrumented Mode, if implemented)
- **Maps to:** RQ-031
- **Metric:** localization error (cm)
- **Method:** impacts at known positions; compute estimate; compare to truth
- **Instrumentation:** PVDF node array + DAQ; position marking/jig
- **Data products:** localization error distribution; method description
- **Acceptance:** TBD after node geometry definition; must report error bounds

---

### T-SHM-062 — Diagnostic excitation repeatability (Instrumented + Excitation)
- **Maps to:** FM-D002
- **Metric:** feature variance across repeated runs (unit depends on feature)
- **Method:** repeated excitation sweeps under controlled boundary conditions
- **Instrumentation:** driver + DAQ; temperature monitoring
- **Data products:** repeated FRF/impedance curves; variance metrics
- **Acceptance:** TBD; must demonstrate stable baselines or explicitly quantify drift

---

### T-EMI-070 — EMI/ESD robustness (Instrumented Mode)
- **Maps to:** FM-S005
- **Metric:** false trigger rate; baseline corruption events; data loss
- **Method:** exposure per defined procedure; ESD handling and event logging
- **Instrumentation:** EMI environment (as available); ESD simulator (if available); logging
- **Data products:** event log; before/after baselines; incident report
- **Acceptance:** TBD; minimum requirement is full documentation of susceptibility

---

### T-QA-090 — Reproducibility package check
- **Maps to:** RQ-060
- **Metric:** “rebuildability” of results from raw data (pass/fail)
- **Method:** independent rerun of scripts/steps from raw to plots/tables
- **Instrumentation:** N/A
- **Data products:** reproduction notes; any diffs found
- **Acceptance:** plots/tables reproduced within stated numerical tolerance

---

## 4) Notes on TBD acceptance thresholds
PoC acceptance thresholds are set after baseline characterization and must not be stated as safety guarantees. Thresholds become fixed only when:
- measurement methods are stable,
- variance is quantified,
- and mission-relevant constraints (if declared) justify the chosen margins.

---

## 5) Cross-references
- Requirements: `docs/03_Requirements_and_Acceptance_Criteria.md`
- Failure modes: `docs/06_Failure_Modes_and_Risks.md`
- PoC procedures: `docs/09_PoC_Test_Procedures.md`

---
End of test matrix.
