# AHIS — Autonomic Hull Integrity System
**Repository:** ahis-autonomic-hull-integrity-system  
**Author/Maintainer:** Bryce Lovell  
**Status:** Engineering proof-of-concept (PoC). Not flight-qualified. Not crew-rated.

## Purpose
AHIS is a consolidated design and verification repository for a **hull protection stack** intended to improve survivability against:
- **Impulsive mechanical loads** (impact/shock, debris strike, handling damage)
- **Fatigue and delamination growth** under cyclic loading
- **Pressure boundary compromise** (crack initiation, puncture propagation, leak onset)
- **Operational environments** relevant to spacecraft and high-performance marine structures

AHIS integrates two engineering directions:
1) **Passive, rate-dependent energy management** (PressureX lineage): a layer concept intended to increase resistance under high strain-rate events to reduce peak strain and spread load.
2) **Electromechanical structural health monitoring (SHM)** (Thaed lineage, scientifically reframed): PVDF-based sensing and diagnostic excitation for damage detection/localization and (optionally) bounded vibration attenuation.

This repo is written to be **auditable**: every claim must map to a measurable quantity and a test method.

---

## What AHIS is (and is not)
### AHIS is
- A **system architecture** for hull protection with clear subsystem boundaries (materials, sensing, electronics, verification).
- A **PoC build + test workflow** that produces repeatable data: strain, acceleration, leakage, and SHM metrics.
- A **measurement-first** framework for comparing designs by **mass, thickness, and performance deltas**.

### AHIS is not
- Not “force fields,” “mass nullification,” “Tesla 3-6-9,” or any untestable mechanism.
- Not a certification package.
- Not an operational safety guarantee.

---

## System concept (high-level)
AHIS is a layered stack with a verification harness:

### A) Passive protection (rate-dependent layer)
A rate-dependent interlayer (e.g., shear-thickening / viscoelastic concept) is used to:
- Increase effective stiffness/viscosity during high strain-rate events
- Reduce peak strain transmitted to the structural substrate
- Spread impulse over a larger area and time window

**Primary measurable outputs:**
- Peak strain reduction (%)
- Peak acceleration reduction (g)
- Energy absorption / impulse spreading metrics (derived from force/accel/strain)
- Post-event damage extent (area, delamination indicators)

### B) SHM skin (PVDF electromechanical layer)
PVDF and conductive electrodes are used for:
- **Sensing:** strain/impact → electrical response (direct piezoelectric effect)
- **Diagnostics:** injected waveforms → measured response (impedance/FRF/guided-wave methods)
- **Localization:** estimating damage region based on change in transfer functions/time-of-flight (if implemented)

**Primary measurable outputs:**
- Detection time (ms / s)
- Localization error (cm)
- Sensitivity/false positive rates (PoC statistical reporting)
- Environmental drift (temperature/vacuum cycling impact on baselines)

### C) Optional vibration attenuation / resonance control (bounded, experimental)
Vibration attenuation is treated as engineering control, not a guarantee. AHIS supports:
- Passive **shunt damping** (piezo + tuned electrical networks)
- **Feedback control** (sensor → controller → actuator), within realistic power budgets

This capability is formally scoped under the **Active Control Module (Mode E)** with explicit
stability/authority/power/EMI discipline:
- `docs/18_Active_Control_Module.md`
- `docs/19_Control_Architecture_and_Stability.md`
- `docs/20_Modal_Testing_FRF_Method.md`
- `docs/21_Actuator_Authority_and_Power_Budget.md`
- `docs/22_EMI_EMC_Design_Rules.md`

**Primary measurable outputs:**
- Δζ (damping ratio increase) per targeted mode
- Transmissibility reduction (dB) at resonance
- Power draw (W) and thermal rise (°C)
- (Mode E) stability margins (gain/phase) and saturation logging

---

## Threat model (PoC scope)
AHIS does not claim hypervelocity MMOD protection unless explicitly tested with appropriate facilities.
PoC scope targets:
- **Low-velocity impacts** representative of handling damage / tool strikes / suborbital debris regimes
- **Fatigue cycling** to observe delamination/crack growth trends
- **Pressure boundary integrity** (leak initiation and leak rate under defined damage)

**Out of PoC scope unless added later:**
- Hypervelocity impact (true MMOD)
- Flight certification and crew-rating requirements
- Full radiation qualification

---

## Proof-of-Concept (PoC) deliverables (what this repo is structured to produce)
1) **A build recipe** for a small coupon panel (materials stack, bonding, electrode routing, PVDF placement)
2) **Instrumentation harness** (sensing + DAQ + optional excitation driver)
3) **A test matrix** mapping every claim → measurement → instrument → pass/fail thresholds
4) **Repeatable data packages** in a standard structure with plots and raw logs
5) **A performance delta report** normalized by areal density (kg/m²) and thickness (mm), generated from real logs

---

## Repository structure
- `BOM/` — consolidated bill of materials and procurement placeholders
- `docs/` — architecture, requirements, threat model, science basis, risk/FMEA-lite, test matrix, PoC walkthroughs
- `src/analysis/` — analysis scripts (impact peaks, leak metrics, normalization, delta report generation)
- `results/` — strict evidence packages (raw + processed + calibration + photos)

> Note: any historical material imported later should be placed under a `legacy/` folder with clear disclaimers.
AHIS claims are defined by the canonical `docs/` set and evidence in `results/`.

---

## Engineering rules for this repo
- **No claim ships without a metric.** If it can’t be measured, it is labeled “Hypothesis.”
- **No safety claims without test evidence.** “Crew-safe” language is prohibited in PoC docs.
- **All outcomes must include failure modes.** If a mechanism can fail, it is documented.
- **All results are normalized.** Performance is reported per kg/m² and per mm thickness.

---

## Known technical risks (must be addressed)
- **Rate-dependent layer behavior vs temperature** (viscosity drift, freezing, softening)
- **Vacuum compatibility / outgassing** of polymers, adhesives, and STF carriers (if vacuum is relevant)
- **Bondline durability** under thermal gradients and cyclic strain
- **PVDF aging/depolarization** and baseline drift under environment
- **Electrode integrity** (cracking, corrosion, delamination) and EMI/ESD susceptibility
- **Contamination / maintenance hazards** from any fluid-like layer or encapsulant

AHIS is designed so each risk maps to a test protocol and acceptance criteria.

---

## How to read this repo (engineer-first path)
1) `docs/02_Threat_Model_and_Environments.md`
2) `docs/03_Requirements_and_Acceptance_Criteria.md`
3) `docs/01_Architecture_Overview.md`
4) `docs/06_Failure_Modes_and_Risks.md`
5) `docs/07_Test_Matrix.md`
6) `docs/08_PoC_Build_Walkthrough.md` and `docs/09_PoC_Test_Procedures.md`
7) `docs/17_Analysis_Pipeline_Walkthrough.md`

---

## Licensing (testing allowed; no profit)
AHIS is released under an **evaluation-only, non-commercial** license:
- anyone may read, test, and critique
- **no commercial/profit use** is permitted without a separate written agreement with the maintainer

See `LICENSE`.

---

## Contact
For commercial licensing, deployment permission, or consulting/hand-off discussions:
**Bryce Lovell**

---
**Bottom line:** AHIS is a measurement-first hull protection PoC repository. It is intentionally conservative in claims and explicit about what must be proven before any operational use.
