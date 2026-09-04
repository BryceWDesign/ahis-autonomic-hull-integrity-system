# P1 physical calibration inputs

No calibration numbers are shipped as evidence. Generate them from the assembled physical article.

## Pressure CSV
Create a CSV with exactly these columns:

`reference_head_mm,adc_fraction`

Record at least four stabilized points spanning zero through at least 750 mm of water head. `adc_fraction` is the Pico ADC reading divided by 65535. The gravity source must remain open to atmosphere.

Run:

```bash
python scripts/p1_sensor_calibration.py pressure-measured.csv loadcell-measured.csv sensor-calibration.json
```

## Load-cell CSV
Create a CSV with exactly:

`reference_mass_g,hx711_counts`

Record the empty installed catch-cup state plus at least three certified/verified applied masses, including points near 100 g, 300 g, and 500 g. The catch cup and platform must remain in their final mounted configuration.

## Pump CSV
Create a CSV with exactly:

`channel,trial,runtime_s,delivered_volume_ml`

Calibrate each installed pump using its **assigned final P1 agent, tubing, and nozzle**. Record at least three independent volumetric trials for A and three for B.

Run:

```bash
python scripts/p1_pump_calibration.py pump-measured.csv pump-calibration.json
```

Copy the generated `sensor-calibration.json` to the Pico filesystem as `device_calibration.json`. The host controller checks the live Pico calibration digest before it will actuate a repair run.
