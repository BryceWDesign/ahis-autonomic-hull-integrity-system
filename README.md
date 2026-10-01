# AHIS, Autonomic Hull Integrity System v4.0.2

**Evaluation-licensed adaptive structural-survivability software/HIL research platform.**

AHIS v4 implements the Adaptive Survival Envelope: characterize damage, enter preservation, assess remaining control authority, coordinate bounded responses, verify using held-out evidence, and recover only to a limited state or isolate.

**Current physical status: AWAITING_PHYSICAL_VALIDATION.** This release demonstrates software behavior in a manufactured reference experiment. It does not demonstrate material healing strength, physical impact protection, pressure-hull survival, radiation shielding, certification or operational return to service.

## What changed from v3

| v3 foundation retained | v4 addition |
|---|---|
| Fixed two-agent recipe planner | Joint bounded response/resource planner with declared uncertainty cases |
| Mechanism eligibility | Scaled reachable/unreachable objective decomposition and exact protected modes |
| Repair/degraded-state decisions | Explicit preservation, confirmed containment, repair, verification and isolation transitions |
| Fixed sensor geometry/localization | Anisotropic D-optimal advisory among surviving declared sensors |
| Resource reservation | Archived command/consumption binding, conservation and measured-loss accounting |
| Post-repair acceptance | Required held-out coordinates using exact policy limits and distinct acquisition groups |
| Hash-chained history | Source-bound replay from the complete archived raw request |
| R1-R5 research lanes | R6-R9 protection/network screens and program-specific review gates |

The four-action reference basis uses paired repair-agent volume, separate modal damping, a synthetic heater/strain coordinate and synthetic isolation. Leak and modal responses call the retained AHIS models. Heater/isolation coefficients are manufactured for the experiment, not empirically calibrated. Sensing stays diagnostic; there is no integrated piezoelectric sensor/actuator fiber-mesh implementation.

## Executable proof

The 31-case campaign exercises successful limited recovery and required refusals: lost actuators, depleted resources, unsafe heating, exact-lock overconstraint, failed containment, insufficient sensing, failed/reused verification channels, conservation failures, mismatched commands and resource overdraw. A rejected proposal has zero authorized commands. A failed post-response verification preserves consumed resources rather than pretending they were never used.

The local authority diagnostic only assesses currently violated objectives using surviving command coordinates. The nonlinear optimizer separately enforces all two-sided protected limits and action/resource bounds. Neither an inverse solution nor a full-rank matrix automatically earns acceptance.

The optimizer is a local constrained solver; no global optimum is claimed. Its uncertainty result covers only the declared finite cases. Graph propagation, layer-mass accounting, reversible phase and supplied geometry-candidate ranking are explicit research screens, not validated fracture/CFD/FEA or ballistic models.

## Run

Python 3.11 through 3.13 are the validation targets. Use a virtual environment and the pinned dependency file:

```bash
python -m pip install -r requirements-validation.txt
python -m pip install --no-build-isolation -e .
python -m pip check
python check_green.py
```

The authoritative release gate requires **224 passing tests**, both campaigns, archived replay, claim boundaries, new code lint/format, P1 BOM/CAD integrity, release hygiene and a complete file manifest. GREEN is software/repository status only. See VALIDATION_REPORT.md for executed checks and limits. GitHub CI is configured; its actual run is not claimed in this handoff.

Generate your own work outside the release tree:

```bash
python -m ahis decide configs/survival_reference.json --out ../nominal-evidence.json
python -m ahis audit ../nominal-evidence.json
python -m ahis campaign --config configs/survival_reference.json --out ../my-survival-campaign
```

The installed `ahis` command exposes the same interface. `decide` exits 0 for limited recovery, 2 for rejection/isolation and 1 for invalid input. Audit/campaign exit nonzero on failure. Every new-path result has zero physical credit and zero hardware authority. No device dispatch is performed.

SHA-256 supplies integrity relative to a trusted reference, not signatures or authentication. Retain the printed digest separately and use `audit --trusted-digest` when an external reference is available. Numerical replay uses declared tolerances and exact structural/boolean checks; source hashes and bundle integrity are exact.

## Complete P1 handoff retained

The v3 low-energy gravity-head leak-seal reference article remains included: 54-row procurement BOM, STEP/STL fixture CAD, wiring, dimensional build record, Pico 2 firmware, actual-agent pump/sensor calibration tools, physical-only run controller and physical acceptance scripts.

P1 uses a sealing surrogate. No P1 physical run is claimed here. The new synthetic multi-action planner is not connected to P1 hardware. Begin physical-reference review with docs/02_Claim_Boundary.md and docs/03_P1_Reference_Design.md, then the fabrication, wiring, calibration and acceptance documents.

## Protection and research scope

R1-R5 cover fast sealing, vascular repair, vitrimer repair, SMA metal-matrix repair and sensing restoration. R6 is Stress-Adaptive Protective Interphase; R7 is Multilayer Impact Protection; R8 is Adaptive Structural Architecture; R9 is Resilient Diagnostic Network. All physical programs remain NOT_RUN. Their required measurement/test categories and completeness gates are executable, but eligibility for human review grants no physical credit.

R10, Active Charged-Particle Shield Integrity, is **NOT_IMPLEMENTED** and separate from core AHIS. No fusion, plasma, magnetic debris barrier or radiation-shield performance claim is imported from SymmetryLock. Biological inspiration is documented in research provenance only; the engineering architecture does not depend on biological material.

## Read next

- HANDOFF.md: PowerShell/Linux setup, reproducible commands and existing-Git-checkout instructions.
- PROOF_OF_CONCEPT.md: concrete campaign comparisons and rejection evidence.
- docs/19_Adaptive_Survival_Architecture.md: implementation and integration map.
- docs/20_Mathematics_and_Model_Limits.md: equations, scales, assumptions and boundaries.
- docs/21_Evidence_Replay_and_Threat_Model.md: replay, held-out evidence and external trust.
- docs/22_Protection_and_Research_Programs.md: R6-R10 and physical work still required.
- docs/claims_v4.json: machine-readable implemented/screened/unimplemented claims.
- BOM/: complete P1 procurement list and recorded software dependencies/notices.

## License

AHIS v4 retains **AHIS Evaluation License 1.0**, source-available for evaluation rather than open source. Commercial, operational, manufacturing, integration, deployment, paid-consulting and redistribution uses require separate written permission from **Bryce Lovell**.

Licensing contact: https://www.linkedin.com/in/brycewdesign/

Earlier copies actually distributed under Apache License 2.0 retain their existing rights. The historical text remains in LICENSES/Apache-2.0-historical.txt. Third-party distributions retain their own terms. There is no patent freedom-to-operate guarantee.

**Software evidence proves software behavior; physical claims require measured physical evidence and explicit review.**
