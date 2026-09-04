# Physical Acceptance and Promotion

## Evidence hierarchy
1. Unit tests: code invariants only.
2. Deterministic HIL: control/fault behavior against a synthetic rig only.
3. P1 measured campaign: only the bounded low-energy leak-seal statement.
4. Mechanism-specific coupons: ionomer, microvascular, vitrimer, SMA/MMC or sensing-network restoration evidence.
5. Panels/subcomponents: structural-system evidence.
6. Full-scale qualification/certification: external engineering and regulatory activity.

## Physical evidence firewall
`ahis.physical.P1RunEvidence` requires `source_kind="PHYSICAL_MEASUREMENT"`, >=20 samples per leak window, accepted fit quality, measured head/pressure, calibration-bundle SHA-256 and raw-telemetry SHA-256. HIL/synthetic records are rejected rather than downgraded into ambiguous evidence.

## No automatic promotion
No executable automatically changes `PHYSICAL_STATUS.json` from false to true. `p1_assess_campaign.py` reports evidence only. Promotion requires deliberate human review of raw telemetry, hashes, calibrations, completed build record, inspection evidence, deviations and the generated assessments in a future release.

## Required P1 review package
- exactly three unique raw telemetry JSONL files;
- three physical run JSONs and receipts;
- campaign assessment receipt;
- sensor and pump calibration artifacts;
- completed build/fixture inspection record;
- reagent lot/preparation record;
- deviations;
- reviewer identity/date/decision.

Even a reviewed P1 pass does **not** promote restored structural strength, ionomer healing, composite healing, pressure-hull survival, return-to-service or certification.
