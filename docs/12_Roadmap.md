# AHIS — Roadmap
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Planning document (PoC → evidence-driven iterations)

---

## 0) Roadmap rule
AHIS progresses only by closing unknowns with:
- defined tests,
- measured data,
- and documented limitations.

Anything not tested remains “Hypothesis.”

---

## Phase 0 — Repo foundation (documentation and discipline)
**Goal:** Make the repo reviewable without trust.

Deliverables:
- Threat model + environments
- Requirements + acceptance criteria policy
- Architecture overview
- Science basis documents (passive + PVDF SHM)
- Failure modes and risks (FMEA-lite)
- Test matrix + PoC procedures + results templates

Exit criteria:
- A reviewer can trace any claim to a test plan and a metric.

---

## Phase 1 — Baseline establishment (repeatability first)
**Goal:** Build baseline and AHIS coupons with controlled boundary conditions and quantify variance.

Work items:
- Define coupon geometry and fixture conditions (documented)
- Build Config A (baseline) and Config B (passive)
- Perform repeated low-velocity impact and/or vibration tests (T-IMP-010, T-IMP-011, T-VIB-040)
- Establish statistical baselines and measurement uncertainty

Exit criteria:
- Repeatable baseline distributions for strain/accel and damage extent.
- “TBD” thresholds in requirements begin conversion to fixed values.

---

## Phase 2 — Instrumented SHM PoC (detection and drift)
**Goal:** Demonstrate reliable sensing and characterize drift.

Work items:
- Build Config C (instrumented)
- Capture baseline noise and controlled event datasets (T-SHM-060)
- Characterize baseline drift vs temperature cycles (T-THM-030)
- Document false triggers and mitigation (wiring/shielding strategy)

Exit criteria:
- Event detection demonstrated with repeatable thresholds and documented error modes.
- Drift quantified and either compensated or bounded.

---

## Phase 3 — Diagnostic excitation (repeatability and features)
**Goal:** Validate diagnostic excitation methods for change detection.

Work items:
- Build Config D (instrumented + excitation)
- Implement multi-tone/chirp diagnostic sweeps (T-SHM-062)
- Quantify repeatability vs boundary conditions and temperature
- Identify stable features for change detection

Exit criteria:
- Diagnostic curves repeatable within defined variance bounds under controlled conditions.
- Feature set documented for baseline comparisons.

---

## Phase 4 — Pressure boundary evaluation (if pursued)
**Goal:** Measure leak behavior and correlate detection timing.

Work items:
- Define sealed fixture and leak measurement method (T-PRS-050)
- Test baseline vs AHIS for leak onset and leak rate
- Document dominant leak paths (often edges/seals) and redesign accordingly

Exit criteria:
- Leak onset definition and leak rate computation validated and repeatable.

---

## Phase 5 — Environmental robustness and integration realism
**Goal:** Close the biggest engineering objections.

Work items:
- Expand thermal/vibration profiles to more realistic regimes
- EMI/ESD checks for instrumented mode (T-EMI-070)
- Materials screening for vacuum/outgassing if space environment is claimed
- Long-duration aging checks (bondline and electrode durability)

Exit criteria:
- Documented survivability envelope and failure boundaries.
- Clear mass/thickness vs performance trade curve.

---

## Phase 6 — MMOD / hypervelocity (only with proper facilities)
**Goal:** Evaluate true orbital debris relevance.

Work items:
- Define hypervelocity test program (external facility)
- Update threat model and requirements specifically for MMOD
- Publish results with strict limitations

Exit criteria:
- No MMOD protection claims without hypervelocity test evidence.

---

## Backlog (known open items)
- Replace all legacy “3/6/9” references in imported legacy docs with standard SHM terms or quarantine legacy docs under `legacy/` with disclaimers.
- Resolve PressureX “no electronics” vs “sensor module” documentation mismatch by enforcing Passive vs Instrumented modes consistently.
- Add a traceability map for which files/ideas originate from which legacy repo.

---
End of roadmap.
