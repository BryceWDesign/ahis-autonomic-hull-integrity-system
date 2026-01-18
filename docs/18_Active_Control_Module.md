# AHIS — Active Control Module (Experimental)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Experimental PoC module. Not flight-qualified. Not crew-rated.

---

## 0) Scope statement (read first)
This module adds **experimental active vibration attenuation / resonance control** capability to AHIS **in a strictly bounded, testable way**.

AHIS core remains:
- passive, rate-dependent energy management (impact/shock load spreading), and
- PVDF-based structural health monitoring (SHM) for detection/diagnostics.

This module introduces an optional mode:
- **Instrumented + Active Control (Experimental)**

No “field control” is claimed. All effects are framed as standard **mechanical vibration control**.

---

## 1) What this module is intended to do
### 1.1 Active vibration attenuation (band-limited)
Reduce response near specific structural resonances by increasing effective damping or applying counter-action.

**Measurable outcomes:**
- transmissibility reduction (dB) at targeted modes
- damping ratio increase (Δζ) at targeted modes
- peak acceleration/strain reduction under defined excitation profiles

### 1.2 Resonance suppression (modal control)
Identify dominant modes (via FRF/modal testing), then apply:
- passive **shunt damping** (piezoelectric element + tuned electrical network), and/or
- **feedback control** (sensor → controller → actuator) with defined stability margins.

**Measurable outcomes:**
- modal peak amplitude reduction
- modal frequency shift (if observed) and associated tradeoffs
- stability margins (gain/phase) for closed-loop configurations

### 1.3 Instrumentation survivability and EMI/ESD robustness (support function)
This module includes EMI/ESD design practices to keep measurement/control stable.

**Measurable outcomes:**
- baseline corruption events during EMI exposure
- false trigger rate
- recovery behavior (time to regain stable baseline)

---

## 2) What this module does NOT claim
- Vehicle-wide “active isolation” across all frequencies and all operating conditions.
- Guaranteed vibration elimination.
- Any nonstandard physics (no “nullification,” no numerology-based harmonics).
- EMI/EMC “field control” as a protective mechanism; only standard shielding/grounding/filtering practices.
- Crew safety or flight readiness.

---

## 3) Modes (how this integrates with AHIS)
### Mode C — Instrumented (already in AHIS)
- PVDF sensing + DAQ for detection/diagnostics
- No actuation required

### Mode D — Instrumented + Diagnostic Excitation (already in AHIS)
- Adds multi-tone/chirp excitation for impedance/FRF/guided-wave diagnostics
- Not closed-loop control

### Mode E — Instrumented + Active Control (this module)
- Adds a controller and an actuator path
- Can be implemented as:
  - **E1: Shunt damping** (no digital controller required), or
  - **E2: Feedback control** (digital controller required), or
  - **E3: Hybrid** (shunt + feedback)

---

## 4) Actuator reality check (required)
Active control requires actuator authority. PVDF can be:
- a sensor,
- an excitation source for diagnostics,
- and in some contexts a small-signal actuator,
but **vehicle-scale control generally requires more actuator authority** than PVDF alone provides.

Therefore, AHIS Mode E must explicitly declare which actuator strategy is used:
- PVDF actuation (small-signal, coupon-scale)
- separate actuator (e.g., voice coil, piezo stack, inertial mass actuator) with PVDF sensing
- hybrid

No actuator strategy may be claimed without:
- actuator authority estimate (force/strain vs frequency)
- power budget (W) and thermal constraints
- stability considerations (feedback mode)

---

## 5) Control architecture overview (high level)
### 5.1 Sensing
- PVDF nodes (strain/impact response)
- optional accelerometers for reference and validation

### 5.2 Estimation / signal conditioning
- filtering and anti-aliasing consistent with sampling rates
- feature extraction for targeted modes (band-limited)

### 5.3 Control
- shunt network tuning (E1) and/or controller design (E2/E3)
- explicit stability margins for feedback control

### 5.4 Actuation
- defined actuator path
- output limits (Vpp/current/temperature rise)

---

## 6) Acceptance discipline (what must be proven)
Mode E is “real” only when tests demonstrate, under controlled boundary conditions:
- repeatable transmissibility reduction and/or Δζ improvement
- stable operation with defined gain/phase margins (feedback mode)
- no unacceptable power/thermal behavior
- documented failure modes (wiring fatigue, drift, EMI susceptibility)

All Mode E claims must map into the test matrix:
- `docs/07_Test_Matrix.md` (to be extended)

---

## 7) Primary risks (Mode E)
- actuator authority insufficient (no meaningful control effect)
- controller instability (feedback oscillation)
- temperature drift undermines tuning/baseline
- wiring/connector fatigue creates false signals
- EMI/ESD events corrupt sensing/control loop

These risks must be tested and reported (no assumptions).

---
End of Active Control Module.
