# AHIS — Modal Testing and FRF Method (Mode E Support)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** PoC method. Not flight-qualified. Not crew-rated.

---

## 0) Purpose
Active control (Mode E) must start with evidence: identify the plant’s dominant modes under the exact boundary conditions used for testing. This document defines a PoC method to obtain:

- Frequency Response Function (FRF) magnitude/phase
- Resonant frequencies (fn)
- Damping estimates (ζ, PoC-level)
- Repeatability/variance across runs

No control claim is valid without a documented baseline FRF.

---

## 1) What is an FRF (in AHIS terms)
An FRF is the frequency-domain relationship between:
- an **input excitation** (force/command/base motion)
and
- an **output response** (acceleration, strain, PVDF node response)

FRF is used to:
- find resonances
- quantify damping and transmissibility
- select control bands and tune shunt/control filters

---

## 2) PoC measurement approach (choose one and declare it)
### Option A — Base excitation (preferred for transmissibility)
- Input: shaker table acceleration (measured)
- Output: coupon acceleration/strain at measurement points

This yields transmissibility FRFs that map directly to “how much vibration gets through.”

### Option B — Instrumented impact hammer (if available)
- Input: force hammer time series (measured)
- Output: acceleration/strain response

This is common for quick modal identification.

### Option C — Actuator command as input (if calibrated)
- Input: actuator command signal (requires calibration to a physical quantity)
- Output: response

This is acceptable only if actuator input can be meaningfully referenced.

---

## 3) Boundary conditions (mandatory)
FRFs are fixture-dependent. Every FRF dataset must include:
- clamp geometry and torque (if applicable)
- fixture materials and thickness
- any shims/pads and their thickness/material
- photos of all constraints

Cross-reference:
- `docs/15_Fixture_and_Boundary_Conditions.md`

---

## 4) Sensor selection and placement (PoC guidance)
### 4.1 Output sensors
Preferred outputs for modal/FRF work:
- accelerometers (clear physical output)
- strain gauges (for local strain modes)

PVDF can be used as an output channel, but:
- it is more sensitive to wiring/impedance drift
- it requires careful baseline characterization

### 4.2 Placement discipline
- place at least one sensor near expected high participation regions (not at nodes)
- document coordinates (mm) relative to coupon center/edges
- keep placement identical across baseline and AHIS coupons

---

## 5) Excitation plan (minimum viable)
### 5.1 Frequency sweep / chirp
- define sweep band (start/end frequency)
- define sweep duration
- record amplitude level and any saturation behavior

### 5.2 Multi-tone (if used)
- list each tone frequency
- list amplitude per tone
- justify selection (e.g., around known resonances)

---

## 6) Data capture requirements
Every FRF dataset must record:
- sampling rate (Hz)
- anti-alias filtering (if any)
- windowing method (if used)
- number of averages (if using spectral averaging)
- temperature at time of test (°C) if relevant

---

## 7) Minimal processing outputs (what must be reported)
At PoC stage, report at least:
- FRF magnitude vs frequency (units must be explicit)
- FRF phase vs frequency
- identified resonance frequency (fn) and an estimated damping indicator

PoC-level damping estimate can be reported as:
- half-power bandwidth estimate (if appropriate and documented)
or
- ring-down decay estimate (time-domain method) if performed

If damping is estimated, include:
- method
- limitations
- repeatability variance

---

## 8) Acceptance and repeatability rules
An FRF dataset is considered usable for Mode E only if:
- boundary conditions are fully documented
- repeat FRFs are consistent within declared variance
- the target mode(s) are identifiable (not buried in noise or dominated by fixture artifacts)

If the FRF shifts significantly between runs:
- treat it as evidence of an uncontrolled variable (fixture, temperature, bonding changes)
- do not proceed to feedback tuning until repeatability is improved

---

## 9) Outputs and file placement
Place FRF datasets under the relevant test ID folder, e.g.:
- `results/T-VIB-040/<RUN_ID>/` or a Mode-E-specific test folder added in the matrix update

Include:
- raw time series
- processed FRF tables
- plots with units
- and the run README describing the method

Use:
- `docs/10_Data_and_Results_Template.md`

---
End of modal testing / FRF method.
