# AHIS — Control Architecture and Stability (Mode E)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Experimental PoC control guidance. Not flight-qualified. Not crew-rated.

---

## 0) Scope
This document defines a conservative, standard controls framing for AHIS **Mode E (Instrumented + Active Control)**:
- what the loop looks like,
- what must be measured,
- and how stability is demonstrated.

No stability claims are valid without measured plant response and repeatable test evidence.

---

## 1) Definitions (controls)
- **Plant:** the structure/fixture/coupon system being controlled (the mechanical system).
- **Sensor:** PVDF node(s) and/or accelerometer providing measured output.
- **Actuator:** device applying force/strain to the plant (PVDF actuation or separate actuator).
- **Controller:** algorithm or network that uses sensor data to compute actuator commands.
- **Open-loop response:** plant response without feedback (used for identification).
- **Closed-loop response:** response with feedback enabled.
- **Stability margins:** gain margin (GM) and phase margin (PM) describing robustness.

---

## 2) Why “active isolation” is not claimed by default
Active vibration control is inherently **band-limited**:
- actuator authority drops with frequency and mass coupling
- high-frequency behavior becomes difficult to control robustly
- time delay and sampling impose stability limits

Therefore, AHIS Mode E targets specific, identified modes/bands and reports results within that scope.

---

## 3) Control loop architecture (minimum viable PoC)
### 3.1 Signal chain
1) **Sense:** PVDF/accelerometer signal(s) sampled by DAQ
2) **Condition:** filtering, scaling, anti-alias, offset removal (documented)
3) **Control law:** compute actuator command
4) **Actuate:** apply command through driver/amplifier to actuator
5) **Measure:** observe response and compute transmissibility/Δζ

### 3.2 Recommended PoC approach: narrowband modal control
Mode E should begin with one target mode:
- Identify the mode frequency and damping (baseline)
- Apply control in a narrow band around that mode
- Measure transmissibility reduction and Δζ change
- Verify stability margins and repeatability

---

## 4) Plant identification (mandatory before feedback claims)
Feedback control requires a model of the plant response in the band of interest.

Minimum acceptable identification:
- measure **FRF** (input → output) for the fixture/coupon system under the exact boundary conditions used
- capture magnitude and phase across the band of interest
- document sensor and actuator placement

Outputs:
- baseline FRF plots/tables (with units)
- identified resonance frequency, damping estimate, and uncertainty

Cross-reference:
- `docs/20_Modal_Testing_FRF_Method.md`

---

## 5) Control strategies (PoC-appropriate)
### 5.1 E1 — Shunt damping (preferred first step)
Shunt damping uses a piezoelectric element and an electrical network to dissipate energy.
- advantage: no digital stability loop; lower complexity
- limitation: tuning sensitivity to temperature and boundary conditions

PoC must report:
- tuned frequency band
- sensitivity to drift (re-run after thermal exposure if relevant)

### 5.2 E2 — Feedback control (digital controller)
Feedback can target:
- acceleration minimization at a point
- strain reduction at a region
- transmissibility reduction from base excitation

PoC control laws should start simple:
- band-limited proportional control
- notch filters
- lead/lag compensation around the target mode

PoC must report:
- controller structure and parameters
- sampling rate and latency estimates
- stability margins

### 5.3 E3 — Hybrid
Use shunt damping to reduce resonance peak and feedback to refine response.
PoC must document both contributions separately.

---

## 6) Stability requirements (what must be shown)
### 6.1 What “stable” means in AHIS Mode E
A Mode E configuration is only considered stable if:
- no sustained oscillation occurs under nominal conditions
- no runaway output occurs under defined disturbances
- stability margins meet declared thresholds

### 6.2 Minimum stability margin targets (PoC)
These are conservative starting targets, not certification values:
- **Phase Margin (PM):** ≥ 30° (TBD by data)
- **Gain Margin (GM):** ≥ 6 dB (TBD by data)

If your measured system cannot meet these, you must either:
- reduce loop gain/bandwidth, or
- change actuator/sensor placement, or
- abandon feedback and use shunt-only for that configuration.

### 6.3 Demonstration methods (PoC)
- Open-loop FRF measurement and Bode stability assessment (preferred)
- Closed-loop response tests with step/burst excitations and monitoring for oscillation
- Repeatability checks across multiple runs

All stability demonstrations must be documented as:
- test ID
- fixture/boundary condition
- exact controller configuration
- plots/tables of margin estimates

---

## 7) Latency and sampling constraints (must be declared)
Feedback control is limited by delay:
- sensor sampling period
- DAQ buffering
- computation time
- driver/amplifier response

PoC requirement:
- declare sampling rate (Hz)
- declare estimated end-to-end latency (s) if known
- restrict control bandwidth accordingly

No “high bandwidth” claims without measured delay.

---

## 8) Failure modes specific to control (Mode E)
- unstable oscillation (controller instability)
- actuator saturation leading to distortion and instability
- sensor drift causing incorrect control action
- EMI/ESD causing false inputs and unsafe outputs
- mechanical decoupling (bondline/connector failure) invalidating the plant model

These map into:
- `docs/06_Failure_Modes_and_Risks.md` (system-level risk tracking)
- test matrix additions (next update)

---

## 9) What must be included in a Mode E results package
A Mode E results package must include:
- baseline FRF (open-loop) for the configuration
- controller parameters and version
- stability margin estimates (GM/PM or an equivalent robust measure)
- transmissibility/Δζ metrics with repeats and variance
- power draw and any thermal rise (if measured)
- failure logs (if any)

Use the standard results template:
- `docs/10_Data_and_Results_Template.md`

---
End of control architecture and stability.
