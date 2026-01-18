# AHIS — Project Charter
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Proof-of-Concept (PoC) engineering repository (not flight-qualified, not crew-rated)  
**Date:** 2026-01-12

---

## 1) Mission
Build an **auditable, measurement-first** proof-of-concept for a hull protection stack that combines:
- **Passive, rate-dependent load/energy management** (PressureX lineage), and
- **Electromechanical Structural Health Monitoring (SHM)** using PVDF-based sensing/diagnostic excitation (Thaed lineage, reframed into standard engineering terms),

to improve detection, localization, and mitigation planning for hull damage that can compromise structural integrity and pressure boundaries.

---

## 2) Primary objective
Produce a repository that a technical reviewer can evaluate without trust:
- Every claimed mechanism maps to **metrics + units**
- Every metric maps to a **test method + instrumentation**
- Every test has **pass/fail acceptance criteria**
- Every limitation is explicitly stated

---

## 3) Scope (PoC)
### In scope
- Layer-stack definition (materials + interfaces) for coupon-scale panels
- Passive layer concept evaluation via mechanical testing
- PVDF-based SHM concept evaluation via:
  - strain/impact sensing
  - multi-tone/chirp excitation for diagnostics
  - impedance/admittance or FRF tracking for change detection
  - localization methods with explicit error bounds
- Documentation: requirements, threat model, risks, test matrix, and results templates

### Explicitly out of scope (unless added later with dedicated testing)
- Crew-rating / certification / safety guarantees
- Hypervelocity MMOD protection claims
- Full radiation qualification
- Production manufacturing process qualification
- Any nonstandard physics framing (no “nullification,” no numerology-based claims)

---

## 4) Engineering principles (repo rules)
1) **No claim without a metric.**  
   If it cannot be measured, it is labeled **Hypothesis**.
2) **No safety claims without evidence.**  
   “Crew-safe” and “flight-ready” language is prohibited in PoC docs.
3) **Conservative terminology only.**  
   Use standard terms: SHM, modal analysis, FRF, impedance/admittance, guided waves, damping ratio, transmissibility.
4) **Normalization is mandatory.**  
   Report performance per **areal density (kg/m²)** and **thickness (mm)**.
5) **Traceability is mandatory.**  
   All major content must map to either legacy sources (PressureX / Thaed) or clearly labeled new work.

---

## 5) Success criteria (what “done” looks like at PoC stage)
AHIS PoC is considered successful when the repo contains:
- A coherent architecture describing subsystems, interfaces, and assumptions
- A complete test matrix mapping each claim → measurement → instrument → pass/fail threshold
- A build walkthrough that yields a repeatable coupon panel configuration
- At least one end-to-end results package (simulated or measured, clearly labeled) using the repo’s templates, including:
  - peak strain / acceleration under controlled impact or vibration
  - SHM change detection outputs and localization error (if localization is attempted)
  - documented failure modes and limitations

---

## 6) Key risks to manage (must be tracked)
- Temperature dependence of rate-dependent layers (viscosity drift / freezing / softening)
- Vacuum compatibility / outgassing of polymers, adhesives, encapsulants
- Bondline durability under cyclic strain and thermal gradients
- PVDF aging/depolarization and baseline drift
- Electrode integrity (cracking/corrosion/delamination) and EMI/ESD susceptibility
- Contamination / maintenance risk from any fluid-like layer or encapsulation breach

Each risk must map to a verification plan or be explicitly deferred.

---

## 7) Deliverables (repo artifacts)
Minimum deliverables to maintain engineering credibility:
- Threat model + environments
- Requirements + acceptance criteria
- Architecture overview
- Science basis documents for passive and SHM subsystems
- Failure modes and risks (FMEA-lite)
- Test matrix + test procedures
- PoC build walkthrough
- Data/results reporting templates
- Source traceability map (legacy → AHIS)

---

## 8) Change control
All major changes must:
- Identify affected claims/metrics/tests
- Update acceptance criteria and the test matrix if needed
- Preserve traceability to legacy sources or explain the deviation

---
End of charter.
