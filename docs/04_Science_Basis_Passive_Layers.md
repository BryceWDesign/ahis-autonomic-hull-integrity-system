# AHIS — Science Basis: Passive Rate-Dependent Layers (PressureX Lineage)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Proof-of-Concept (PoC). Not flight-qualified. Not crew-rated.

---

## 1) Purpose of the passive layer in AHIS
The passive layer is intended to improve hull survivability by changing how loads are transmitted during short-duration, high strain-rate events (impact/shock). The passive layer must be evaluated by **measurable deltas** relative to baseline:
- peak strain reduction
- peak acceleration reduction
- damage extent reduction
- (if tested) pressure boundary leak behavior

This document describes plausible, standard mechanisms consistent with a “rate-dependent” interlayer concept. It does not claim performance without tests.

---

## 2) Rate-dependent response (what “shear thickening” implies)
A rate-dependent layer is one where effective viscosity or stiffness increases as shear rate or strain-rate increases. The intended consequence is:
- under slow deformation: layer remains compliant
- under rapid deformation: layer stiffens/dissipates, spreading impulse and reducing local peak strain

In PoC terms, the question is not whether a label (“STF”) is used; it is whether the stack produces a measurable improvement under defined loading profiles.

---

## 3) Plausible mechanisms (measurable)
### 3.1 Impulse spreading via increased effective stiffness/viscosity
If the interlayer stiffens under high strain-rate, it can:
- increase contact duration (reducing peak force)
- increase effective contact area (spreading load)
- increase damping (reducing rebound and resonance coupling)

**Measurements:**
- time history of strain/accel during impact
- peak values and impulse proxies
- frequency content and ring-down behavior

### 3.2 Energy dissipation (viscous and interfacial losses)
Energy can be dissipated through:
- viscous losses in the interlayer (if fluid-like or viscoelastic)
- interfacial friction/slip between layers (if present)
- microstructural rearrangement in composites (material-dependent)

**Measurements:**
- hysteresis area in cyclic loading (if performed)
- ring-down decay / damping ratio estimates
- thermal rise (optional PoC measurement)

### 3.3 Crack/delamination growth resistance (architecture-dependent)
A compliant or dissipative interlayer can reduce crack driving forces by:
- blunting stress concentrations
- altering fracture path
- reducing interlaminar shear peaks (depending on stack)

**Measurements:**
- damage mapping (inspection method must be defined)
- delamination indicators and growth rate under cycling

---

## 4) Practical risks and constraints (must be tested, not assumed)
### 4.1 Temperature dependence
Rate-dependent layers can shift behavior significantly with temperature:
- viscosity drift or phase behavior changes
- freezing/softening that alters performance

**PoC requirement:** measure performance across declared temperature points or explicitly scope temperature.

### 4.2 Vacuum compatibility and outgassing
Polymer carriers, encapsulants, and adhesives can outgas or form voids under low pressure.

**PoC requirement:** if vacuum is relevant, materials must be screened and performance drift reported.

### 4.3 Encapsulation integrity and contamination risk
If the layer uses any fluid-like component, failure of encapsulation can introduce:
- contamination
- mass redistribution
- loss of function

**PoC requirement:** define encapsulation method and include durability checks.

### 4.4 Bondline durability
Many “protective” concepts fail at the interface:
- adhesive creep
- delamination
- edge sealing failure

**PoC requirement:** bondline and edge seal design must be treated as first-class engineering items.

---

## 5) What AHIS will not claim from the passive layer (until proven)
- Hypervelocity MMOD protection
- Crew safety guarantees
- Long-duration durability in flight environments
- Performance at temperature/vacuum extremes without explicit tests

---

## 6) Verification approach (how this becomes credible)
The passive layer is validated through comparative tests:
1) Build baseline and AHIS coupon panels with documented geometry
2) Apply defined impacts/vibration profiles with controlled boundary conditions
3) Measure strain/accel and inspect damage
4) Report deltas normalized by areal density and thickness
5) Document failure modes and conditions where performance degrades

Cross-reference:
- Requirements: `docs/03_Requirements_and_Acceptance_Criteria.md`
- Test mapping: `docs/07_Test_Matrix.md`
- PoC procedures: `docs/09_PoC_Test_Procedures.md`

---
End of passive layer science basis.
