# P1 Autonomous Test Procedure

## Preconditions
- completed `hardware/P1_BUILD_RECORD.csv` copy;
- water-only fixture inspection passed;
- current accepted sensor and actual-agent pump calibration JSONs;
- matching sensor calibration copied to Pico as `device_calibration.json`;
- open/vented gravity reservoir, spill tray and dry pressure leg;
- independent agent lines primed to the nozzle face without cross-mixing;
- hard E-stop actuator-power removal demonstrated immediately before run.

## Agents
**A:** 2.00 g MilliporeSigma A2033 sodium alginate, hydrated in DI water and brought to final volume 100.0 mL.

**B:** 5.00 g MilliporeSigma C3881 calcium chloride dihydrate, dissolved in DI water and brought to final volume 100.0 mL.

Record reagent lots, actual masses, final volumes, preparation time and operator. Use current supplier SDS instructions, safety glasses and nitrile gloves.

## Establish canonical leak
1. Fill the cell and purge bubbles from the main water path.
2. Set calibrated measured head to 500 +/-25 mm.
3. Confirm seams/bulkhead/plumbing remain dry.
4. Start a unique run ID. The controller measures at least 20 baseline samples over 20 s.
5. Baseline must be >=20 mL/min **and** linear mass-fit R-squared >=0.95. Failure blocks repair actuation; do not alter acceptance criteria.

## Autonomous delivery and verification
Run the physical-only controller:

```bash
python scripts/p1_run_controller.py \
  --port <physical-serial-port> \
  --run-id P1-RUN-001 \
  --sensor-calibration sensor-calibration.json \
  --pump-calibration pump-calibration.json \
  --fixture-leak-check pass
```

Sequence:
1. host verifies calibration digest and live Pico safety state;
2. host computes **independent** A/B runtimes required for 8.0 mL each from measured pump rates;
3. host sends `ARM`; Pico energizes actuator relay only while its local interlocks pass;
4. host sends `PUMP_PAIR`; Pico starts both pumps together and independently stops each at its calibrated runtime while continuously checking E-stop and pressure/head;
5. host commands `DISARM`;
6. system dwells 60 s without manual manipulation of the seal zone;
7. host acquires at least 20 post-response samples over 20 s;
8. host hashes raw telemetry and writes a physical run JSON + objective assessment.

Any command/sensor/calibration/interlock failure aborts actuation.

## Per-run acceptance
All conditions must pass:
- baseline leak >=20 mL/min;
- post-response leak reduction >=80%;
- baseline and post linear-fit R-squared >=0.95;
- >=20 samples in each measurement window;
- maximum head <=800 mm;
- maximum pressure <=8 kPa;
- no E-stop violation;
- no unintended fixture leak.

## Canonical campaign
Clean the article and restore/verify the controlled 1.50 +/-0.05 mm orifice between independent runs. Run exactly three unique IDs. Assess them with:

```bash
python scripts/p1_assess_campaign.py run1.json run2.json run3.json P1-campaign-assessment.json
```

At least two of three must pass before the bounded statement **P1 low-energy autonomous leak seal demonstrated** is eligible for human review. Structural-strength and hull-survivability credit remain zero.
