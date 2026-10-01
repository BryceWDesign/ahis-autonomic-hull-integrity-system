# AHIS v4.0.2, 2026-10-01

- Hardened executed-command verification from independent per-coordinate bounds to full-vector scenario coherence.
- Preserves complete response predictions for every declared finite uncertainty scenario.
- Rejects mixed-scenario held-out vectors with `RESPONSE_SCENARIO_INCONSISTENT`.
- Retains per-coordinate `RESPONSE_MODEL_INCONSISTENT` diagnostics for out-of-band responses.
- Adds `heldout_scenario_inconsistent` adversarial campaign coverage.
- Explicitly makes no physical sensor-noise or continuous uncertainty interpolation claim.
- Release suite increased to 224 tests and the v4 campaign to 31 cases.

# AHIS v4.0.1, 2026-10-01

- Hardened held-out verification against safe-looking but executed-command-inconsistent responses.
- Added finite-uncertainty response bands derived from the actual executed command.
- Added `heldout_model_inconsistent` adversarial campaign coverage.
- Preserved policy-envelope verification as a separate acceptance condition.
- Explicitly avoids claiming a physically calibrated sensor-noise model.
- Release suite increased to 223 tests and the v4 campaign to 30 cases.

# AHIS v4.0.0, 2026-10-01

Added the integrated Adaptive Survival Envelope software/HIL research path, bounded four-action reference model, SVD authority and safe-mode diagnostics, fixed-command robustness, active sensing, preservation/isolation state policy, hazard graphs, conservation ledgers, policy-bound held-out verification, source-bound replay and research completeness gates. Retained P1 hardware/CAD/firmware/calibration and v3 campaign. Added pinned validation dependencies and a Linux/Windows CI matrix. All physical capabilities remain unvalidated.

# Changelog

## 3.0.0 — Autonomic Structural Repair & Survivability Testbed

- Changed new-release licensing to the AHIS Evaluation License 1.0; Bryce Lovell retains commercial/operational/manufacturing licensing authority.
- Preserved the historical Apache-2.0 text solely to document earlier-distribution rights.
- Added finite repair-resource accounting and fail-closed repair planning.
- Added deterministic hardware-in-the-loop repair rig with E-stop, overpressure, resource-depletion and damaged-twin negative controls.
- Added anisotropic localization with explicit uncertainty, transparent multimodal evidence fusion, digital-twin discrepancy screening, uncertainty-bounded prognostics and hash-chained structural history.
- Added strict host/Pico hardware protocol and simultaneous independently calibrated two-agent actuation.
- Added AHIS-P1 low-energy gravity-head physical reference article with fixed geometry, generated STEP/STL CAD, a 54-line procurement BOM, wiring netlist, fabrication traveler, build inspection record, firmware, calibration tools and live physical-run controller.
- Added load-cell leak-rate measurement and pressure/head sensing with Pico-safe divider architecture.
- Added raw physical telemetry hashing, calibration binding, physical-only evidence parser, objective run assessment and fixed 2-of-3 campaign assessment.
- Added separate validation programs for ionomer, microvascular, vitrimer, SMA/MMC and sensor-network restoration research.
- Kept all physical demonstration flags false in this release. No synthetic result is promoted to a physical self-healing or hull-survivability claim.

## 2.0.0 — Historical predecessor

The previous repository generation established the v2 software architecture, deterministic campaign and conservative physical claim boundary. Rights for copies actually distributed under their historical license remain governed by that license.
