# AHIS — Science Basis: PVDF Structural Health Monitoring (SHM) Skin
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Proof-of-Concept (PoC). Not flight-qualified. Not crew-rated.

---

## 1) Purpose of the PVDF SHM skin in AHIS
The PVDF-based SHM skin is intended to provide **measurable** integrity information about the hull stack:
- Detect damaging events (impact, abnormal strain transients)
- Detect changes consistent with damage growth (delamination, cracking, bondline failure)
- Localize likely damage regions (when node geometry and methods support it)
- Provide post-event diagnostic checks (compare current response to baseline)

This document replaces any nonstandard framing with standard SHM methods used in engineering practice.

---

## 2) Physical basis (standard electromechanical coupling)
PVDF (polyvinylidene fluoride) exhibits piezoelectric behavior:

### 2.1 Direct piezoelectric effect (sensing)
Mechanical strain/stress applied to PVDF produces charge separation, yielding a measurable voltage/current when connected to an input circuit.

**Observable quantity:** PVDF voltage response (V) as a function of strain/impact transients.

### 2.2 Inverse piezoelectric effect (actuation / diagnostic excitation)
Applying an electric field to PVDF induces strain. In PoC, this is used for diagnostic excitation and response measurement.

**Observable quantity:** response features (amplitude/phase vs frequency; time-of-flight; impedance) under controlled excitation.

---

## 3) SHM modalities supported by AHIS (PoC)
AHIS treats SHM as measurable signal processing, not “field effects.”

### 3.1 Event detection (transient monitoring)
Use PVDF outputs (and optional accelerometers/strain gauges) to detect abnormal events.

**Typical measurable features:**
- peak amplitude
- rise time / impulse-like signatures
- energy in defined frequency bands
- threshold crossing with hysteresis to avoid chatter

**Required reporting:**
- noise floor characterization
- detection threshold justification
- false positive / false negative discussion (PoC-scale)

### 3.2 Impedance/admittance-based SHM (electromechanical impedance)
By injecting a small diagnostic excitation and measuring electrical impedance/admittance at a node, changes in the coupled structure can be detected.

**Measurable outputs:**
- impedance magnitude/phase vs frequency
- feature deltas vs baseline (e.g., resonant peak shifts)

**Notes:**
- Requires stable baseline measurement and temperature-aware interpretation.
- PoC goal is change detection and repeatability; not certification-grade conclusions.

### 3.3 Frequency Response Function (FRF) / modal tracking
Excite the structure with a controlled waveform (sine sweep, chirp, multi-tone) and measure response.

**Measurable outputs:**
- FRF magnitude/phase changes
- modal frequency shifts
- damping ratio changes (Δζ) if identifiable

### 3.4 Guided-wave concepts (Lamb-wave style PoC)
With appropriate node spacing and sampling, guided waves can be used to detect defects through changes in time-of-flight and attenuation.

**Measurable outputs:**
- arrival time shifts
- attenuation changes
- scattering signatures

**PoC constraints:**
- Requires careful boundary condition control and calibration.
- Localization accuracy must be reported with explicit error bounds.

---

## 4) What “multi-tone / chirp excitation” replaces
Any legacy “3/6/9” or numerology-driven “harmonic” language is replaced by:
- **multi-tone excitation** (multiple discrete frequencies)
- **chirp / swept-sine** (continuous frequency sweep)
- **burst excitation** (short packets used in guided-wave methods)

Frequency selection is based on:
- expected modal bands (from modal/FRF characterization)
- sensor bandwidth and DAQ sampling constraints
- desired spatial resolution vs attenuation characteristics

---

## 5) Electronics and measurement constraints (PoC realities)
### 5.1 Sampling and bandwidth
- Sampling rate must be justified by the highest frequency content of interest.
- Anti-alias filtering and calibration must be documented.

### 5.2 Wiring, shielding, and EMI/ESD
PVDF nodes can be high-impedance and sensitive:
- cable routing and shielding strategy must be documented
- baseline drift due to EMI must be measured or mitigated
- ESD handling must be included for instrumented assemblies

### 5.3 Environmental drift
PVDF and bondlines can drift with:
- temperature
- humidity (if applicable)
- mechanical aging

PoC requirement: measure baseline drift and document compensation or limitations.

---

## 6) Failure modes specific to PVDF SHM skin (must be tracked)
- PVDF depolarization or sensitivity loss
- electrode cracking/corrosion/delamination
- bondline degradation decoupling sensor from structure
- connector/cable fatigue under vibration
- false triggers due to EMI or microphonic wiring

Each failure mode must map to a test/inspection step in the test matrix.

---

## 7) What AHIS will not claim from SHM skin (until proven)
- Guaranteed detection under all conditions
- Guaranteed localization without quantified error bounds
- Operational use readiness without environmental and durability testing

---

## 8) Verification approach (how SHM becomes credible in AHIS)
1) Establish baseline signals under controlled conditions
2) Apply controlled events (impact/cycling) with known locations/severity bins
3) Quantify detection performance (SNR, thresholds, false alarms)
4) If localization is attempted, report localization error distributions
5) Repeat after environmental exposure (thermal cycling, vibration, EMI checks) and report drift

Cross-reference:
- Requirements: `docs/03_Requirements_and_Acceptance_Criteria.md`
- Threat model: `docs/02_Threat_Model_and_Environments.md`
- Test mapping: `docs/07_Test_Matrix.md`

---
End of PVDF SHM science basis.
