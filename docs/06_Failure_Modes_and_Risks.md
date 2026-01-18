# AHIS — Failure Modes and Risks (FMEA-lite)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Proof-of-Concept (PoC). Not flight-qualified. Not crew-rated.

---

## 1) Purpose
AHIS must be evaluated by measurable outcomes and must explicitly document how it can fail.
This document is a **lightweight FMEA-style** list to ensure risks are not hidden.

**Rule:** Any risk listed here must either:
- map to a test/inspection in `docs/07_Test_Matrix.md`, or
- be explicitly deferred with rationale and declared “unknown.”

---

## 2) Definitions
- **Failure mode:** a specific way the system can fail.
- **Effect:** what the failure causes at the system level.
- **Cause:** likely mechanism(s) producing the failure.
- **Detection:** how we would know it happened (inspection, sensor signature, test result).
- **Mitigation:** design/process change to reduce likelihood or impact.

Severity/occurrence/detection scoring is optional at PoC stage; AHIS prioritizes **enumeration + test mapping**.

---

## 3) Passive layer (rate-dependent / STF-like interlayer) risks
### FM-P001 — Temperature-driven performance collapse
- **Effect:** passive layer no longer provides intended impulse spreading; may stiffen excessively or become ineffective.
- **Cause:** viscosity drift, freezing, softening, phase changes; polymer transitions.
- **Detection:** impact/vibration metrics degrade vs baseline; temperature sweep shows non-monotonic behavior.
- **Mitigation:** material screening; define operational temperature envelope; encapsulation adjustments; alternative rate-dependent materials.

### FM-P002 — Encapsulation breach / leakage (if fluid-like layer exists)
- **Effect:** contamination risk; loss of function; mass redistribution; degraded bonding.
- **Cause:** puncture, seam failure, permeation, poor edge sealing.
- **Detection:** visible leakage, mass loss, pressure decay, post-test inspection.
- **Mitigation:** robust encapsulation design; redundancy; edge seal qualification; containment barriers.

### FM-P003 — Outgassing / voiding (vacuum-relevant)
- **Effect:** void formation; bondline weakening; sensor drift; pressure boundary compromise.
- **Cause:** volatile components in polymers/adhesives/encapsulants.
- **Detection:** mass loss, voids after vacuum exposure, mechanical property shifts.
- **Mitigation:** vacuum-compatible material selection; bake-out procedures; explicit outgassing tests.

### FM-P004 — Bondline creep / delamination initiation
- **Effect:** reduced load transfer; delamination growth under cycling; rapid failure after impact.
- **Cause:** adhesive creep, thermal mismatch, poor surface prep, moisture ingress.
- **Detection:** NDT proxy (tap test / ultrasound if available), edge peel, stiffness/FRF changes.
- **Mitigation:** surface preparation protocol; adhesive selection; mechanical interlocks; edge sealing; fatigue testing.

---

## 4) PVDF SHM skin risks (instrumented mode)
### FM-S001 — Baseline drift makes diagnostics unusable
- **Effect:** false alarms or missed detections; inability to compare to baseline.
- **Cause:** temperature sensitivity, aging, depolarization, adhesive creep, humidity (if applicable).
- **Detection:** baseline feature drift beyond threshold; repeat tests fail to match within tolerance.
- **Mitigation:** baseline compensation strategies; environmental characterization; recalibration schedule; improved bonding.

### FM-S002 — PVDF depolarization / sensitivity loss
- **Effect:** reduced SNR; event detection failure.
- **Cause:** thermal exposure, mechanical fatigue, material aging, improper handling.
- **Detection:** declining response amplitude for standardized calibration events.
- **Mitigation:** operating envelope limits; protective encapsulation; periodic calibration checks.

### FM-S003 — Electrode degradation (cracking/corrosion/delamination)
- **Effect:** open circuits; noisy signals; nonfunctional actuation/measurement.
- **Cause:** strain cycling, thermal cycling, moisture/salt exposure, galvanic corrosion.
- **Detection:** continuity checks, visual inspection, rising contact resistance, erratic signals.
- **Mitigation:** electrode material choice; strain relief; corrosion barriers; environmental sealing; routing redesign.

### FM-S004 — Wiring/connector fatigue or microphonics
- **Effect:** intermittent signals; false triggers; data loss.
- **Cause:** vibration, poor strain relief, cable routing, connector fretting.
- **Detection:** intermittent continuity; noise correlated with motion; vibration test failures.
- **Mitigation:** strain relief; connector selection; cable shielding; mechanical routing constraints.

### FM-S005 — EMI/ESD susceptibility corrupts SHM readings
- **Effect:** false triggers; baseline corruption; hardware resets.
- **Cause:** unshielded runs; high impedance nodes; inadequate grounding; ESD events.
- **Detection:** correlation with EMI exposure; repeatability failures; ESD tests.
- **Mitigation:** shielding/grounding plan; input protection; filtering; ESD handling procedures.

---

## 5) Diagnostic excitation / driver risks
### FM-D001 — Overdrive damages PVDF or bondline
- **Effect:** permanent sensitivity loss; delamination; localized heating.
- **Cause:** excessive Vpp, duty cycle, or current; incorrect gain staging.
- **Detection:** temperature rise; post-drive sensitivity drop; visual delamination; electrical anomalies.
- **Mitigation:** hard limits; monitoring; conservative envelopes; stepwise characterization.

### FM-D002 — Excitation results are non-repeatable (false conclusions)
- **Effect:** misinterpretation of structural state; invalid change detection.
- **Cause:** inconsistent boundary conditions; temperature drift; inconsistent coupling to fixtures.
- **Detection:** high variance in repeated runs; inconsistent FRF/impedance features.
- **Mitigation:** fixture control; environmental control; standardized coupling procedure; repeatability thresholds.

---

## 6) System-level risks
### FM-SYS001 — Mass/thickness penalty exceeds benefit
- **Effect:** unacceptable integration cost for the achieved protection delta.
- **Cause:** heavy layers, thick encapsulation, extensive wiring.
- **Detection:** normalized performance deltas (per kg/m² and mm) fail to justify added mass.
- **Mitigation:** optimization; remove non-contributing layers; target-only reinforcement; architecture revision.

### FM-SYS002 — Edge effects dominate failure
- **Effect:** leak paths or delamination initiate at edges, negating layer performance.
- **Cause:** poor edge sealing; stress concentrations; fixture boundary mismatch.
- **Detection:** repeated edge-origin failures; consistent leak location at seams.
- **Mitigation:** edge design as first-class subsystem; dedicated edge qualification tests.

### FM-SYS003 — “Auto-repair” expectation exceeds implemented capability
- **Effect:** reviewer distrust; misuse risk.
- **Cause:** terminology suggesting autonomous healing without a validated mechanism.
- **Detection:** documentation review; mismatch between claims and evidence.
- **Mitigation:** strict language discipline: “self-sealing mechanism” only if implemented and tested; otherwise “repair-guided.”

---

## 7) Required mappings
- Each failure mode above must map to tests/inspections in `docs/07_Test_Matrix.md`.
- Deferred risks must be tracked in `docs/12_Roadmap.md` with an explicit plan.

---
End of failure modes and risks.
