# AHIS — Threat Model and Environments (PoC)
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Proof-of-Concept (PoC). Not flight-qualified. Not crew-rated.

---

## 1) Why a threat model exists in this repo
AHIS is measurement-first. “Protection” is only meaningful relative to:
- what threats are in scope,
- what environments apply, and
- what failure criteria define unacceptable outcomes.

This document defines the PoC threat scope and the environments that can materially change performance.

---

## 2) Threats (PoC in-scope)
### 2.1 Low-velocity impact / blunt strike
Representative examples (non-exhaustive):
- tool drop / handling strike
- loading/unloading impacts
- sub-orbital debris regimes where hypervelocity is not assumed

**Failure criteria (examples; finalized in Requirements doc):**
- cracking through pressure boundary
- delamination growth beyond defined area
- unacceptable peak strain/acceleration transmission to protected structure

### 2.2 Penetration onset / puncture propagation (non-hypervelocity)
Representative examples:
- sharp-object intrusion
- edge impacts initiating tear growth

**PoC objective:**
- measure whether the passive layer reduces damage growth rate and/or peak local strain
- detect onset rapidly via SHM skin (instrumented mode)

### 2.3 Fatigue, delamination growth, and bondline degradation
Threat mechanism:
- cyclic strain + thermal gradients drive microcrack growth, delamination, adhesive creep

**PoC objective:**
- demonstrate detectable SHM baseline shifts correlated with damage progression
- quantify durability margins over defined cycle counts (PoC-scale)

### 2.4 Pressure boundary compromise (leak initiation)
Threat mechanism:
- crack initiation or puncture that creates a leak path

**PoC objective:**
- define leak-rate measurement and thresholds
- detect/flag leak onset and locate region (instrumented mode)

---

## 3) Threats explicitly out of PoC scope (unless added later)
### 3.1 Hypervelocity MMOD (true orbital debris)
Hypervelocity impacts (km/s regime) produce shock, melt/vapor, and fragmentation behaviors
that are not addressed by PoC assumptions here.

**Rule:** AHIS must not claim MMOD hypervelocity protection without dedicated testing
(e.g., light gas gun range, validated hypervelocity test campaign).

### 3.2 Crew-rating, certification, and operational safety guarantees
This repo is not a certification artifact and does not provide safety guarantees.

### 3.3 Radiation qualification
Radiation effects on polymers, PVDF polarization stability, and electronics are out of PoC scope
unless specifically tested and documented.

---

## 4) Environments that materially affect AHIS performance
### 4.1 Temperature extremes and thermal cycling
Risks:
- rate-dependent layer viscosity drift / freezing / softening
- adhesive/bondline property changes and thermal expansion mismatch
- PVDF baseline drift and depolarization trends

PoC requirement:
- define temperature range used for PoC tests and report performance drift.

### 4.2 Vacuum / low pressure environments
Risks:
- polymer outgassing and void formation
- encapsulation bladder permeation/leakage
- adhesive cure and stability changes vs atmosphere

PoC requirement:
- if vacuum is claimed as relevant, materials must be screened for outgassing behavior.
This repo does not assume compliance without tests.

### 4.3 Moisture / salt / marine exposure (if applicable)
If AHIS is evaluated for marine hull contexts:
- corrosion at electrode interfaces
- moisture ingress into bondlines and encapsulation
- biofouling/chemical exposure

PoC requirement:
- explicitly declare whether marine exposure is in scope for a given test campaign.

### 4.4 Vibration and acoustic loading
Threat mechanism:
- resonance amplification, connector fretting, fatigue acceleration
- electronics susceptibility (instrumented mode)

PoC requirement:
- vibration test profiles must be defined; results must report transmissibility and failures.

### 4.5 EMI / ESD (instrumented mode)
Threat mechanism:
- false triggers, baseline corruption, data loss, latch-up (if applicable)
- sensor wiring acting as antennas

PoC requirement:
- instrumented mode must include EMI/ESD considerations and test procedures where relevant.

---

## 5) Outcomes and failure modes (what “bad” looks like)
AHIS evaluations consider at least these outcomes:

### 5.1 Structural outcomes
- through-crack / rupture
- delamination growth beyond threshold area
- bondline failure
- permanent deformation beyond threshold

### 5.2 Pressure boundary outcomes
- leak onset (defined by measurable leak rate)
- inability to maintain specified pressure differential over defined time

### 5.3 SHM outcomes (instrumented mode)
- missed detection (false negative)
- false alarm (false positive)
- localization error beyond threshold
- baseline drift leading to unusable diagnostics
- sensor/electrode delamination or wiring failure

### 5.4 Integration outcomes
- unacceptable mass/areal density increase for stated protection delta
- contamination risk (if any fluid-like layer is used)
- maintenance complexity that negates operational value

---

## 6) PoC “engineering seriousness” rule
AHIS documentation will only describe:
- what is tested,
- what is measured,
- what passed/failed,
- and what remains unknown.

Anything else is labeled **Hypothesis**.

---
End of threat model and environments.
