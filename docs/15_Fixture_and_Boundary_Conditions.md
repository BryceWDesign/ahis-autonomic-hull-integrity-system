# AHIS — Fixture and Boundary Conditions (PoC Standard)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** PoC guidance. Not flight-qualified. Not crew-rated.

---

## 1) Why this document exists
In coupon testing, **fixtures and boundary conditions often dominate outcomes**. If baseline and AHIS coupons are not tested under identical constraints, deltas are not meaningful. This document standardizes what must be recorded so results are reviewable by external engineers.

---

## 2) Universal rules (apply to every test)
For every run package, you must document:

1) **Coupon geometry**
- Length/width/thickness (mm)
- Layup or substrate type (if applicable)
- Configuration (A/B/C/D)

2) **Constraint condition**
- Which edges are clamped vs free
- Clamp length along each edge (mm)
- Clamp pressure method (bolts/torque or uniform clamp system)

3) **Contact interfaces**
- Any rubber pads, shims, or spacers (material + thickness)
- Surface finish and friction-relevant notes if it can affect slip

4) **Photos (mandatory)**
- full fixture overview
- close-up of each clamped edge
- sensor routing and strain relief
- any seals (for pressure tests)

If any of the above changes between baseline and AHIS runs, it must be treated as a confounder.

---

## 3) Recommended coupon sizes (PoC default)
AHIS does not mandate a specific size; however, for repeatable PoC work, choose one and stick to it.

Suggested defaults (choose one and declare it in your run plan):
- **100 mm × 100 mm** coupons (small, easy to fixture)
- **150 mm × 150 mm** coupons (more room for sensors and node spacing)

Record actual dimensions for every coupon (measured, not nominal).

---

## 4) Impact test fixture standard (T-IMP-010 / T-IMP-011)
### 4.1 Boundary condition options (pick one and keep consistent)
- **Fully clamped perimeter**: all four edges clamped
- **Two-edge clamp**: two opposite edges clamped, two free (more flexible response)

For whichever is used, record:
- clamp span per edge (mm)
- bolt pattern and bolt torque (if bolts used)
- backing plate material and thickness (mm)

### 4.2 Impact location and striker geometry (mandatory)
Each run must include:
- striker tip shape (flat/rounded/conical) and dimensions (mm)
- target impact coordinates relative to coupon center (mm)
- impact energy control method (drop height and mass, or instrumented actuator)
- number of repeats and cooldown time between impacts (if relevant)

### 4.3 Instrumentation placement (mandatory)
If strain gauges and/or accelerometers are used:
- exact location (mm from center and/or from edges)
- orientation (for strain)
- adhesive type and cure method (for gauges)

---

## 5) Pressure/leak fixture standard (T-PRS-050)
Pressure/leak results are frequently fixture-limited. Your run package must explicitly separate:
- fixture leakage
- coupon leakage
- seal leakage (edge/interface)

### 5.1 Required declarations
- Test volume description (geometry and approximate volume, if known)
- Seal type(s) used (gasket material, O-ring, adhesive sealant, etc.)
- Clamp method and torque (if applicable)
- Pressure sensor type and logging rate
- Initial pressure differential and duration

### 5.2 Leak onset definition (mandatory)
Define leak onset in measurable terms, e.g.:
- pressure decay rate exceeds X Pa/s for Y seconds, or
- measured flow exceeds X sccm for Y seconds

No leak onset definition = invalid run.

---

## 6) Environmental conditions (required)
For each run, record:
- temperature (°C) at start and during test (if monitored)
- humidity (if relevant to your materials)
- any chamber settings for thermal tests

---

## 7) Acceptance discipline
AHIS does not treat “one good hit” as evidence. To be reviewable:
- repeat runs must exist
- variance must be reported
- all boundary conditions must be documented

Cross-reference:
- Test matrix: `docs/07_Test_Matrix.md`
- Results format: `docs/10_Data_and_Results_Template.md`

---
End of fixture and boundary condition standard.
