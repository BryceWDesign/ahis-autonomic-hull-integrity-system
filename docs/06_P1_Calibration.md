# P1 Calibration

No calibration values are shipped as physical evidence. Calibrate the exact assembled article and retain the generated JSON artifacts.

## Pressure/head + load-cell calibration
Follow `hardware/calibration/README.md` and create measured CSV inputs.

Pressure: at least four stabilized open-atmosphere gravity-head points spanning zero through at least 750 mm.

Load cell: final mounted platform + catch cup, with zero and at least three verified masses spanning approximately 100-500 g.

Run:

```bash
python scripts/p1_sensor_calibration.py pressure-measured.csv loadcell-measured.csv sensor-calibration.json
```

The tool rejects pressure fits with maximum residual >0.15 kPa and load-cell fits with maximum residual >2.0 g. Copy the accepted JSON to the Pico filesystem as `device_calibration.json`. The live host checks its SHA-256 against the Pico-reported digest.

## Pump calibration
Calibrate each installed pump with its assigned **final agent, final tubing and final nozzle**. Record at least three volumetric trials per channel:

`channel,trial,runtime_s,delivered_volume_ml`

Run:

```bash
python scripts/p1_pump_calibration.py pump-measured.csv pump-calibration.json
```

The tool rejects either channel if coefficient of variation exceeds 0.10. Recalibrate after pump, tubing, nozzle, agent concentration or relevant drive-voltage changes.

## Binding
The physical run record binds the sensor calibration SHA and pump calibration SHA into one calibration-bundle digest, and binds the complete raw telemetry file with a separate SHA-256. A digest mismatch invalidates the run.
