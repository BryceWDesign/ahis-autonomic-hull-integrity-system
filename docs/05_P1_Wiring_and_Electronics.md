# P1 Wiring and Electronics

`hardware/P1_WIRING.csv` is the canonical netlist.

## Power architecture

`12 V isolated supply -> 3 A fuse -> logic branch + actuator branch`

- **Logic:** fused 12 V -> Pololu D24V22F5 -> 5 V -> Pico VSYS and MPX5010DP.
- **Actuator:** fused 12 V -> Pololu 2482 COM; relay NO -> pump actuator bus.
- **Hard E-stop:** NC-A interrupts the Pololu 2482 **VDD/relay-coil supply**. The relay therefore cannot remain energized after the E-stop contact opens, even if firmware is wrong.
- **Monitored E-stop:** independent NC-B pulls Pico GP15 low when healthy; GP15 internal pull-up reads high when that contact opens.

The Pololu 2482 12 V carrier exposes EN/VDD/GND; its manufacturer specifies activation from a digital-high EN signal beginning at approximately 2.5 V. Pico GP6 therefore drives EN while the separate NC-A contact retains hard authority over the 12 V coil supply.

## Pico 2 pin map
| Function | Pin |
|---|---|
| Pump A driver | GP2 |
| Pump B driver | GP3 |
| HX711 DOUT | GP4 |
| HX711 CLK | GP5 |
| Pololu 2482 EN | GP6 |
| E-stop NC-B monitor | GP15 |
| MPX pressure ADC | GP26 / ADC0 |
| HX711 logic | 3V3 |
| Common logic return | GND |

## Pressure interface
MPX5010DP uses a nominal 5 V supply and can output well above the Pico ADC rail. Never wire sensor VOUT directly to GP26.

Install at the sensor:
- 1.0 uF and 0.01 uF supply decoupling;
- 470 pF VOUT-to-ground filter;
- 10.0 kOhm from VOUT to the ADC node;
- 22.0 kOhm ADC node to ground.

Divider ratio: `22 / (10 + 22) = 0.6875`. The installed sensor/divider/ADC chain is then physically calibrated; firmware does not award accuracy from the nominal transfer function alone.

## Load cell
Run the Adafruit HX711 logic from 3.3 V. Wire the Adafruit 4540 load cell to E+/E-/A+/A- according to the actual product wiring documentation and verify sign during calibration. Do not rely on wire color alone if the purchased revision differs.

## Pump drivers
Each Adafruit 5648 receives relay-switched actuator-bus positive at the pump, common ground, and its Pico signal. The driver performs low-side switching. Pump A and B remain independent through the nozzle outlet.

## Mandatory dead-power inspections
- fuse upstream of both branches;
- no exposed conductor in the spill zone;
- relay **NO**, not NC, feeds actuator bus;
- NC-A physically removes relay-coil VDD;
- actuator bus measures approximately 0 V with E-stop pressed;
- Pico remains alive with E-stop pressed and reports the open contact;
- pumps remain disconnected until these conditions have been measured with a DMM.
