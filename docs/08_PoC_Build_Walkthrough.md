# AHIS — Proof-of-Concept (PoC) Build Walkthrough
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** PoC build instructions. Not flight-qualified. Not crew-rated.

---

## 0) Safety and scope notice
This walkthrough describes a **coupon-scale** PoC panel build intended for lab evaluation.
It does **not** create a certified protective system.

If you use adhesives, coatings, or solvents:
- follow manufacturer SDS instructions
- use PPE and ventilation
- treat all cutting/lamination operations as hazardous

---

## 1) Build objective
Produce one or more coupon panels in controlled configurations so tests can compare:
- **Baseline panel** vs **AHIS passive** vs **AHIS instrumented**
under identical boundary conditions.

**Build outputs (required):**
- measured thickness (mm) and areal density (kg/m²) for each coupon
- build log with materials, batch identifiers, cure schedules, and photos

---

## 2) Panel configurations (PoC minimum set)
### Config A — Baseline panel
- Structural substrate only (your chosen coupon substrate)
- Standard surface prep and any required protective coating
- No passive layer, no PVDF layer

### Config B — AHIS Passive Mode
- Baseline panel + passive rate-dependent interlayer (encapsulated/laminated)
- No PVDF or electronics

### Config C — AHIS Instrumented Mode
- AHIS Passive Mode + PVDF SHM skin + electrode routing
- No diagnostic excitation required for first SHM data collection

### Optional Config D — Instrumented + Diagnostic Excitation
- Config C + waveform driver connection for impedance/FRF/guided-wave diagnostics

---

## 3) Prerequisites (what must be decided before building)
These are required to avoid non-repeatable builds:

1) **Coupon geometry:** length/width/thickness targets  
2) **Substrate material:** and its surface preparation method  
3) **Passive layer approach:** encapsulation method and edge sealing  
4) **PVDF layout (if instrumented):** node positions, routing, strain relief  
5) **Cure schedule:** adhesives/encapsulants cure time and temperature  
6) **Documentation:** how you will record thickness, mass, and photos

If any item above is unknown, document it as “TBD” and do not claim repeatability.

---

## 4) Step-by-step build (PoC)
### Step 1 — Create a build record
Create a build log entry with:
- date/time
- coupon ID (e.g., `AHIS-PANEL-001-A` for baseline)
- substrate spec
- materials batch identifiers
- ambient conditions (approx. temp/humidity if relevant)

Take “before” photos of the substrate and measured dimensions.

### Step 2 — Surface preparation (baseline and all AHIS variants)
Perform surface prep appropriate to the substrate:
- degrease/clean per material requirements
- abrasion/scuff if bonding requires it
- remove dust; ensure dry, contaminant-free surface

Record the method used. If multiple coupons are built, surface prep must be consistent.

### Step 3 — Build Baseline coupon (Config A)
- No additional layers
- If coating is used, apply consistently across all coupons in the set

Measure and record:
- thickness (mm)
- mass (g)
- area (m²) → compute areal density (kg/m²)

### Step 4 — Prepare passive layer materials (Config B/C/D)
AHIS passive concept assumes an interlayer that changes behavior under high strain-rate.
At PoC stage, the build must be explicit about:
- interlayer thickness target
- encapsulation method (if any fluid-like component exists)
- edge sealing method

**Required record:**
- layer thickness target (mm)
- encapsulation seam method
- edge seal method and cure schedule

### Step 5 — Laminate passive layer onto substrate (Config B/C/D)
- Apply passive layer onto the substrate with consistent pressure and alignment
- Avoid trapped air and voids
- Complete edge sealing per defined method

Cure per manufacturer schedule and record:
- cure time
- cure temperature
- any post-cure steps

After cure, measure:
- thickness (mm)
- mass (g)
- compute areal density (kg/m²)

### Step 6 — Add PVDF SHM skin (Config C/D)
The PVDF SHM skin requires:
- PVDF placement location(s)
- electrode contact routing
- strain relief and protection for lead exits

**Required record:**
- PVDF orientation and placement photo
- electrode material type and contact method
- routing path and anchoring method (strain relief)
- continuity check results (before encapsulation, if used)

After assembly, measure:
- thickness (mm)
- mass (g)
- compute areal density (kg/m²)

### Step 7 — Electrical bring-up (Config C/D)
Instrumented mode bring-up is verification, not deployment.

Minimum checks:
- PVDF channel continuity and stable baseline noise level
- no intermittent wiring behavior when gently flexed
- documented DAQ settings (input range, sampling rate)

**Record:**
- baseline noise capture (short dataset)
- DAQ configuration
- wiring diagram photo

### Step 8 — Optional diagnostic excitation bring-up (Config D)
If diagnostic excitation is used:
- stay within the PoC safety envelope defined for PVDF and driver hardware
- record waveform type, amplitude (Vpp), and frequency plan

**Record:**
- actual measured output (if measured)
- test run ID and configuration

---

## 5) Build quality checks (mandatory)
Before any testing, perform and record:
- visual inspection for voids, wrinkles, delamination edges
- thickness and mass measurements
- electrode continuity (instrumented mode)
- consistent coupon labeling visible in photos

If any coupon fails inspection, it must be logged and either rebuilt or excluded from comparisons.

---

## 6) What “auto-repair” means at PoC stage (language discipline)
Unless a validated self-sealing mechanism is implemented and tested, do not claim “auto-repair.”
At PoC stage, AHIS supports:
- **damage detection and localization**
- **repair-guided inspection**
- **mitigation planning**
Self-sealing claims require a defined mechanism and a leak test proving it.

---

## 7) Outputs required for every build
A PoC build is not “complete” unless the repo includes:
- build log entry
- measured thickness and areal density
- photos (before/after, close-ups of edges and wiring)
- DAQ baseline dataset (instrumented mode)
- a clear statement of what is TBD

Cross-reference:
- BOM: `BOM/AHIS_Full_BillOfMaterials.md`
- Requirements: `docs/03_Requirements_and_Acceptance_Criteria.md`
- Test matrix: `docs/07_Test_Matrix.md`

---
End of PoC build walkthrough.
