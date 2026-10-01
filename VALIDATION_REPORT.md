# AHIS v4.0.0 validation report

This report distinguishes executed local checks from configured future CI and unperformed physical work.

| Check | Observed result | Scope |
|---|---|---|
| Supplied AHIS v3 release gate | GREEN, 112 tests | Baseline reproduced before modification |
| Supplied SymmetryLock tests | 45 passing | Donor mathematical repository independently exercised |
| v4 complete repository tests | 222 passing | Inherited suite plus new numerical/adversarial assurance checks |
| Retained v3 campaign | All pass conditions true | Original canonical digest retained |
| v4 survival campaign | 29/29 expected outcomes | Three limited-recovery cases and 26 isolation controls |
| Evidence audit | All 29 archived decisions replay | Integrity/source binding and decision reconstruction |
| Tamper controls | Altered and rehashed altered decisions rejected | SHA-256 alone is not treated as authentication |
| New code/test lint and format | PASS | Scope explicitly defined in QUALITY_GATE.md |
| Local interpreter matrix | Full release gate GREEN on Linux Python 3.11, 3.12 and 3.13 | Separate environments, 222 tests and 29-case replay on each |
| Isolated dependency consistency | PASS | Pinned validation environments |
| Wheel installation and CLI | PASS outside source checkout | Decision, replay audit and dependency consistency |
| P1 reference package | 54 BOM rows; six CAD envelopes pass | Package integrity, no physical run |
| Windows Python 3.13 dependencies | Numerical binary wheels available | Installation availability only, no Windows execution claim |
| GitHub Actions | NOT OBSERVED | Workflow included; actual status requires a push/run |
| Physical validation | NOT RUN | 15 physical/certification flags remain false |

`results/validation/` contains captured command output and environment records. `GREEN_STATUS.json` is a release assertion checked by `check_green.py`, not a substitute for execution. `MANIFEST.sha256` covers released repository files. The outer archive also includes a separate distribution wheel.

The numerical tests check the nominal leak solution against -8 ln(0.2), local authority with a missing objective against 1/sqrt(2), orthogonal SVD reconstruction, information-determinant gain, and an isotropic arrival-gradient formula. End-to-end controls cover hardware interlock denials, failed sensors, insufficient evidence, unconfirmed/failed containment, unavailable actuators, agent/electrical/cycle depletion, thermal and exact-lock overconstraint, a declared uncertainty failure, solver nonconvergence, unavailable/failed/reused held-out channels, mass/energy nonclosure, executed-command mismatch and measured-resource overdraw.

The reference nominal plan is a software/HIL result. It jointly uses paired repair volume, damping increment and heater fraction. Adding synthetic isolation can substitute for a lost sealing coordinate. Those observations do not validate a hull, formulation, sealant, heater, structural material, actuator or impact shield.

Remaining limitations are explicit in docs/claims_v4.json. Local tangent controllability is separate from bounded feasibility. Robustness covers a finite declared set. Propagation is a graph screen. R6-R9 have research and record-completeness support, with no physical promotion. R10 charged-particle shielding and operational structural requalification are not implemented.
