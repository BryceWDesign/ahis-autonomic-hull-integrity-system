# AHIS — EMI/EMC Design Rules (Instrumented Modes C/D/E)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** PoC design guidance. Not flight-qualified. Not crew-rated.

---

## 0) Purpose
Instrumented sensing and control are often defeated by EMI/ESD long before “physics” fails.
This document defines pragmatic EMI/EMC rules to keep AHIS instrumentation stable.

This is not “field control.” It is standard:
- shielding
- grounding
- filtering
- routing discipline
- susceptibility testing and reporting

---

## 1) What EMI/EMC means in AHIS
- **EMI (electromagnetic interference):** unwanted coupled energy that corrupts signals.
- **EMC (compatibility):** the system operates correctly in its electromagnetic environment.
- **ESD:** single-event discharge that can reset/damage electronics and corrupt baselines.

In AHIS, the risk is:
- false triggers
- baseline drift/corruption
- unstable control behavior (Mode E)
- data loss and non-reproducible diagnostics

---

## 2) High-level rules (PoC minimum)
### Rule 1 — Treat PVDF nodes as sensitive / high-impedance by default
- Keep leads short.
- Use shielding where practical.
- Provide strain relief to avoid microphonic cable noise.

### Rule 2 — Separate power and signal paths
- Route power lines away from PVDF and analog front ends.
- If crossing is unavoidable, cross at 90° and document it.

### Rule 3 — Establish a single grounding strategy and document it
PoC systems typically choose one:
- single-point ground (star ground) at DAQ/receiver
- chassis ground + signal reference discipline

Do not mix strategies without a diagram.

### Rule 4 — Input protection for instrumented channels
- ESD diodes / transient suppressors where appropriate
- series resistors and RC filtering if it does not compromise bandwidth goals
- document the analog front-end assumptions

### Rule 5 — Log EMI context
If you test near motors, switch-mode supplies, radios, or lab equipment:
- document it in the run package
- do not interpret spurious data as structural signatures

---

## 3) Wiring and shielding practices
### 3.1 Shielded cable usage
- Use shielded twisted pairs for sensitive analog runs where possible.
- Terminate shields consistently (document whether single-ended or both-ends).
- Avoid floating shields with unknown coupling.

### 3.2 Strain relief
Mechanical motion of cables can produce noise and intermittent connections.
- strain relief at PVDF nodes and connector exits is mandatory for repeatability.

### 3.3 Connector discipline
- avoid loose jumper wiring for “final” PoC evidence runs
- document connector type and any intermittent behavior

---

## 4) Filtering practices (PoC)
Filtering must be chosen to match sampling rate and signal bandwidth needs.

### 4.1 Anti-aliasing
If sampling rate is Fs:
- your analog bandwidth must be bounded below Fs/2
- document whether analog anti-alias filtering is present

### 4.2 Control loop implications (Mode E)
Filtering introduces phase delay that can destabilize feedback.
Mode E runs must document:
- filter types and cutoff frequencies
- whether phase margin was evaluated with filters in place

---

## 5) ESD handling (minimum)
- define ESD handling steps for coupons and boards
- document any ESD events during testing
- if an ESD simulator is used, record procedure and outcomes

---

## 6) Susceptibility testing (how AHIS proves EMI/ESD robustness)
AHIS does not assume EMI robustness. It measures it.

### 6.1 Minimum PoC checks
- baseline capture in a “quiet” environment
- baseline capture in a “noisy” environment (if applicable)
- document difference and false trigger behavior

### 6.2 Formal checks (if equipment available)
- ESD simulation per a declared procedure
- EMI exposure in a shielded environment

All outcomes must be logged as:
- false trigger rate
- baseline corruption events
- recovery behavior (time to stable baseline)

Cross-reference:
- test matrix `T-EMI-070` in `docs/07_Test_Matrix.md`

---

## 7) Required deliverables for instrumented runs
Every instrumented run package must include:
- wiring diagram photo or sketch
- grounding strategy declaration
- DAQ settings and sampling rate
- shielding/strain relief description
- any EMI/ESD incidents observed

If any of these are missing, treat the run as “non-auditable.”

---
End of EMI/EMC design rules.
