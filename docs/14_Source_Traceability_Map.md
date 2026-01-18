# AHIS — Source Traceability Map (Legacy → AHIS)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Traceability reference for reviewers

---

## 1) Purpose
AHIS is a new repository built from two legacy repositories:
- PressureX (passive protective layer concepts + PoC test protocol structure)
- IX-Thaed-Armor (PVDF/electrode panel concepts + install/driver notes)

This map:
- identifies where AHIS concepts originated,
- flags legacy content that requires scientific reframing,
- and provides reviewers a clean provenance view.

---

## 2) Concept-level traceability
### 2.1 Passive, rate-dependent protective layer
- **Legacy source:** PressureX
- **AHIS location:** `docs/04_Science_Basis_Passive_Layers.md` and Requirements/Test Matrix mappings
- **Notes:** Performance is not assumed; must be proven via `T-IMP-*` and durability tests.

### 2.2 PVDF sensing layer for SHM
- **Legacy source:** IX-Thaed-Armor (PVDF mesh and electrode concept)
- **AHIS location:** `docs/05_Science_Basis_PVDF_SHM.md` and SHM tests `T-SHM-*`
- **Notes:** Reframed into standard piezoelectric SHM; any nonstandard language is explicitly excluded from AHIS claims.

### 2.3 Diagnostic excitation (“multi-tone/chirp”)
- **Legacy source:** IX-Thaed-Armor driver notes (`hardware/PVDF_Waveform_Driver.md`)
- **AHIS location:** `docs/05_Science_Basis_PVDF_SHM.md`, `docs/07_Test_Matrix.md` (T-SHM-062)
- **Notes:** Frequency selection is based on modal/FRF considerations. No numerology-based framing.

### 2.4 PoC test protocol discipline
- **Legacy source:** PressureX test protocol documents
- **AHIS location:** `docs/07_Test_Matrix.md`, `docs/09_PoC_Test_Procedures.md`, `docs/10_Data_and_Results_Template.md`
- **Notes:** AHIS strengthens traceability and results packaging rules.

---

## 3) File-level traceability (known legacy anchors)
This section names the key legacy files identified in the two imported zips that informed AHIS documents.

### PressureX anchors
- `README.md` (PressureX) — passive layer concept framing and material candidates
- `hardware/bom.csv` — prototyping electronics BOM (placeholders included)
- `PressureX/tests/vibration_test_protocol.md` — vibration test equipment framing
- `PressureX/tests/thermal_cycling_test_protocol.md` — thermal cycling equipment framing
- `PressureX/environmental_tests/emi_esd_test_protocol.md` — EMI/ESD test framing

### IX-Thaed-Armor anchors
- `BOM/IX-Thaed-Armor_BillOfMaterials.md` — materials stack and vendor examples (contains truncated specs; preserved as placeholders)
- `hardware/PVDF_Waveform_Driver.md` — waveform driver options and PVDF safety notes
- `docs/Power_Interface.md` — power envelope statements (as-written)
- `src/simulate_pvdf_layer_response.py` — PVDF response simulation scaffold
- `src/waveform_gen.py` — waveform generation scaffold

---

## 4) Legacy content quarantine policy
If AHIS imports legacy docs that contain nonstandard physics language (e.g., “nullification”),
they must either:
- be rewritten into standard engineering terms before inclusion in AHIS “claims,” or
- be placed under a `legacy/` folder with a visible disclaimer that they are historical notes
  and not AHIS-validated mechanisms.

AHIS claims are defined only by the docs and tests in the canonical `docs/` set.

---

## 5) What this map does not do
This map does not assert:
- that legacy claims are correct,
- that any performance is proven,
- or that the repo is certified for operational use.

It only provides provenance and a discipline for converting legacy notes into testable engineering statements.

---
End of traceability map.
