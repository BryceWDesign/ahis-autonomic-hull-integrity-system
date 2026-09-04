# AHIS — Autonomic Hull Integrity System v3.0.0

**Evaluation-licensed autonomic structural-repair and survivability research testbed.**

AHIS v3 advances the original passive protection + structural-health-monitoring proof of concept into an executable closed-loop research architecture:

`detect -> localize -> fuse evidence -> assess uncertainty -> check resources/interlocks -> command bounded repair -> measure response -> verify -> retain structural history`

The release includes a concrete low-energy physical reference article, **AHIS-P1**, so the repository can be taken beyond software/HIL into reproducible bench testing without claiming results that have not been measured.

## Current status

- Repository/software release gate: see `GREEN_STATUS.json` and `FINAL_STATUS.md`.
- Physical status: `PHYSICAL_STATUS.json` remains **AWAITING_PHYSICAL_VALIDATION**.
- P1 physical leak-seal performance: **not demonstrated by this repository release**.
- Structural self-healing strength recovery: **not demonstrated**.
- Full-scale hull survivability, operational return-to-service, depth rating and certification: **not claimed**.

Synthetic/HIL results never receive physical credit.

## What v3 contains

### Autonomic control and assurance
- finite repair-agent, electrical-energy, thermal-margin and actuator-cycle accounting;
- fail-closed hardware interlocks;
- bounded repair recipes and executable repair planning;
- deterministic HIL rig and negative-control campaign;
- strict host/Pico JSONL hardware protocol;
- hard E-stop architecture that physically removes actuator relay-coil power while the controller remains alive to report the fault;
- paired repair-agent delivery with independent measured pump calibrations.

### Structural intelligence
- anisotropic damage localization with an explicit uncertainty radius;
- quality-weighted multimodal evidence fusion;
- digital-twin discrepancy checks;
- uncertainty-bounded relative remaining-life screening;
- tamper-evident SHA-256 structural event history.

These are research tools. The digital twin and prognostics are not certified life predictions.

### AHIS-P1 physical reference article
P1 is a deliberately low-energy gravity-head leak-seal demonstrator. It includes:

- procurement BOM: `BOM/AHIS-P1-procurement.csv`;
- generated STEP/STL fixture CAD under `hardware/cad/`;
- dimensional build traveler and inspection record;
- exact wiring netlist and Pico 2 firmware;
- pressure, load-cell and actual-agent pump calibration tools;
- live physical run controller with no synthetic mode;
- raw telemetry hashing and evidence receipts;
- objective per-run acceptance and a fixed three-run campaign rule.

P1 uses sodium alginate + calcium chloride as a **system-level sealing surrogate**. Passing P1 would demonstrate only the bounded low-energy autonomous leak-seal response. It does not establish structural-strength restoration or hull self-healing.

## Repair research programs

The repository separately defines physical validation programs for:

1. puncture-responsive ionomer/self-sealing layers;
2. replenishable microvascular composite repair;
3. electrothermal vitrimer repair;
4. SMA + low-melting-phase metal-matrix repair;
5. recovery of damaged sensing/electrical networks.

They remain at zero physical claim credit until their own specimens and measurements exist. See `docs/09_Repair_Mechanism_Research_Programs.md` and `provenance/TECHNICAL_BASIS_V3_2026.json`.

## Software verification

Python 3.11+:

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python scripts/run_v3_campaign.py
python check_green.py
```

`check_green.py` is the release authority for repository/software status. It verifies compilation, tests, deterministic campaign behavior and claim boundary, evaluation-license boundary, P1 BOM/CAD/status integrity, absence of release junk/unresolved markers, and the complete SHA-256 manifest.

## Building and running P1

Read in this order:

1. `docs/02_Claim_Boundary.md`
2. `docs/03_P1_Reference_Design.md`
3. `BOM/README.md`
4. `docs/04_P1_Fabrication_Traveler.md`
5. `docs/05_P1_Wiring_and_Electronics.md`
6. `docs/06_P1_Calibration.md`
7. `docs/07_P1_Autonomous_Test_Procedure.md`
8. `docs/08_Physical_Acceptance_and_Promotion.md`

Physical host dependency:

```bash
python -m pip install -e '.[hardware]'
```

A live run requires an actual Pico serial port and measured calibration artifacts:

```bash
python scripts/p1_run_controller.py \
  --port <physical-serial-port> \
  --run-id P1-RUN-001 \
  --sensor-calibration sensor-calibration.json \
  --pump-calibration pump-calibration.json \
  --fixture-leak-check pass
```

There is intentionally no HIL/synthetic switch in the physical-run controller.

## License

**AHIS v3.0.0 and later in this release are source-available for evaluation under `LICENSE`; they are not open source.**

Commercial, operational, manufacturing, integration, deployment, paid-consulting and redistribution uses require separate written permission from **Bryce Lovell**.

Preferred licensing contact: <https://www.linkedin.com/in/brycewdesign/>

Earlier copies that were actually distributed under Apache License 2.0 retain the rights granted with those copies. The historical Apache text is retained in `LICENSES/Apache-2.0-historical.txt`; it does not license v3.

## Repository map

- `src/ahis/` — executable AHIS logic
- `tests/` — unit and invariant tests
- `scripts/` — campaigns, calibration, physical evidence and release tooling
- `hardware/` — P1 CAD, wiring, build record and Pico firmware
- `BOM/` — canonical P1 procurement list
- `configs/` — reference article configuration
- `docs/` — architecture, fabrication, testing, safety, licensing and validation path
- `provenance/` — technical basis/source traceability
- `results/v3_extreme_campaign/` — deterministic software/HIL evidence only

## Core rule

**Software can prove software behavior. Hardware measurements can prove only what was actually measured. Neither is allowed to silently promote the other.**
