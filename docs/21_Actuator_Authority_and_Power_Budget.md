# AHIS — Actuator Authority and Power Budget (Mode E)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Experimental PoC guidance. Not flight-qualified. Not crew-rated.

---

## 0) Purpose
Active vibration control only works if the actuator can meaningfully influence the plant (structure) in the frequency band of interest. This document defines what AHIS Mode E must report so engineers can judge feasibility without hand-waving:

- actuator type and placement
- authority (what it can physically do)
- bandwidth limits
- power and thermal behavior
- saturation and failure modes

No Mode E performance claim is valid without this accounting.

---

## 1) Actuator strategies (declare one explicitly)
### E1 — PVDF as actuator (small-signal, coupon-scale)
PVDF can be used as an actuator for:
- diagnostic excitation
- small-signal actuation near targeted modes

**Constraint:** authority is typically limited; vehicle-scale effects are not assumed.

### E2 — Separate actuator with PVDF sensing (most realistic scaling path)
Examples (not exhaustive):
- voice coil / electromagnetic shaker actuator
- piezo stack actuator
- inertial mass actuator
- bonded patch actuator (piezoelectric ceramic)

**Benefit:** greater force authority and clearer calibration.

### E3 — Hybrid
- PVDF for sensing + diagnostics
- separate actuator for control authority

---

## 2) What “authority” means (measurable)
Authority must be expressed as measurable quantities:
- maximum force (N) or equivalent strain/acceleration effect at the measurement point
- maximum displacement/strain output (if applicable)
- frequency range where authority is meaningful (Hz)
- saturation behavior (clipping, thermal limiting)

If the actuator input is a voltage command, authority must be linked to a physical output by calibration
(e.g., command → force proxy or response magnitude under a standardized condition).

---

## 3) Minimum authority evidence (PoC)
Mode E requires at least one of the following evidence types:

### 3.1 Transfer function evidence (preferred)
- input: actuator command (calibrated) or measured force/base acceleration
- output: acceleration/strain at sensor locations

Show that the actuator can excite the target mode with sufficient amplitude to matter.

### 3.2 Controlled excitation benchmark
Apply a standardized excitation and report:
- response amplitude vs frequency
- repeatability across runs
- dependence on boundary conditions

---

## 4) Power budget accounting (mandatory)
For any Mode E run package, record:
- supply voltage (V)
- current draw (A)
- average power (W)
- peak power (W) if measurable
- duty cycle and duration

If current/power are not measured directly, state “not measured” (do not infer).

---

## 5) Thermal behavior (mandatory if power is non-trivial)
Active systems convert energy to heat via:
- actuator losses
- driver/amplifier inefficiency
- shunt network dissipation (E1)

Mode E run packages should include:
- temperature rise at actuator/driver location (°C) if measured
- test duration and ambient temperature
- any thermal limiting behavior (throttle/shutdown)

If not measured, state “not measured.”

---

## 6) Saturation, clipping, and stability implications
Actuator saturation can destabilize feedback loops by:
- introducing nonlinearities
- changing effective gain/phase
- causing limit cycles

Mode E must:
- define command limits
- log any saturations during runs
- report whether stability margins were evaluated with saturation in mind

---

## 7) Failure modes (Mode E actuator path)
- actuator detachment or bondline failure (loss of coupling)
- driver overcurrent/thermal shutdown
- wiring fatigue and intermittent outputs
- EMI/ESD-induced miscommand (if instrumented without protection)
- reduced authority due to temperature drift or material changes

These must map to test and inspection steps in the test matrix.

---

## 8) What Mode E must publish (minimum deliverables)
For a Mode E PoC claim to be taken seriously, publish:
- actuator description and placement with photos
- authority evidence (FRF/transfer function) in target band
- power draw measurements
- any thermal rise measurements
- saturation events and loop stability notes

Cross-reference:
- Control/stability: `docs/19_Control_Architecture_and_Stability.md`
- FRF method: `docs/20_Modal_Testing_FRF_Method.md`

---
End of actuator authority and power budget.
