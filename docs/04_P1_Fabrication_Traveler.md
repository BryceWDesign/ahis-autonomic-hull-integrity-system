# P1 Fabrication Traveler

Record every completed step in a copy of `hardware/P1_BUILD_RECORD.csv`. A reference article is not canonical if a required inspection entry is missing.

## 1. Incoming inspection
1. Verify the two 6 mm polycarbonate plates and 10 mm spacer stock are flat, crack-free and large enough for the 150 x 150 mm finished parts.
2. Measure each 1.5 mm silicone gasket sheet at five distributed points; record minimum, maximum and average.
3. Verify the KIMAX 14612F-2000 bottom-outlet reservoir, PI1208S-US cell fitting, tubing and all electronics against the BOM identifiers.
4. Reject crazed, cracked, chemically attacked or visibly distorted pressure-boundary material.

## 2. Machine the cell
Use the supplied STEP files in `hardware/cad/`.

1. Finish front/back plates to 150.0 +/-0.2 mm square and 6.0 mm nominal thickness.
2. Finish spacer to 150.0 +/-0.2 mm square and 10.0 mm nominal thickness.
3. Machine the twelve 5.5 mm fastener holes at the registered CAD coordinates.
4. Drill the front center orifice with the 1.50 mm drill using a drill press and backing block.
5. Verify 1.45 mm GO passes and 1.55 mm NO-GO does not pass.
6. Machine the 17.0 mm back-plate bulkhead opening at CAD coordinate x=0 mm, y=+35 mm.
7. Machine the spacer 100 x 100 mm through cavity.
8. Deburr without rounding sealing lands. Wash, rinse and dry all wetted parts.

## 3. Gaskets
Cut two gaskets from `AHIS-P1-gasket.step`: 150 x 150 x 1.5 mm, 100 x 100 mm cavity and twelve 5.5 mm holes. Reject tears, folds and damaged sealing edges.

## 4. Cell assembly
Stack:

`front plate -> gasket -> 10 mm spacer -> gasket -> back plate`

Install M5 fasteners with washers under head and nut. Tighten in a crossing pattern only until the total gasket/spacer gap is **12.4 +/-0.1 mm** at left, right, top and bottom. This controls two nominal 1.5 mm gaskets to approximately 20% compression without inventing a torque value for the polymer stack. Reject visible plate crazing or bowing.

## 5. Gravity plumbing
1. Install PI1208S-US in the back plate per its manufacturer instructions.
2. Connect the KIMAX 14612F-2000 bottom outlet to 1/4 in OD PTFE tubing using the reservoir's supplied rigid-tube O-ring/cap hardware.
3. Connect that tube to the cell through the upstream tee and PI1208S-US.
4. Route the pressure branch continuously upward through the dry air leg; mount MPX5010DP above the maximum water level.
5. Keep the reservoir top open/vented throughout P1. Never connect compressed gas or a pressure pump.
6. Secure the reservoir support against tip-over. The calibrated pressure measurement, not a stand scale, determines water head.

## 6. Leak mass measurement
1. Mount the Adafruit 4540 load cell exactly as a cantilever according to the supplier's loading orientation.
2. Attach a rigid 100 x 100 x 3 mm minimum platform to the live end using the actual load-cell mounting-hole dimensions supplied with the purchased sensor. Do not drill the beam outside manufacturer mounting locations.
3. Center the 500 mL catch cup on that platform.
4. Confirm no tubing, cable, tray or cell component contacts the cup/platform/live beam.
5. Calibrate only after this final mechanical assembly is complete.

## 7. Two-agent delivery
1. Rigidly mount both Adafruit 1150 pumps.
2. Use physically separate 4 mm OD / 2 mm ID silicone lines from reservoir to nozzle for each agent.
3. Install both lines through `AHIS-P1-nozzle-bracket.step`; the two bore centers are 6 mm apart.
4. Mount the bracket on its independent articulated support and place its outlet face 2.0 +/-0.5 mm from the front plate centered on the controlled orifice.
5. Trim both outlet tubes flush with the bracket face. Do not create a shared wetted mixer upstream of the external convergence zone.
6. Confirm the normal water leak falls freely into the catch cup and the bracket cannot side-load the cell or load cell.

## 8. Electronics
Wire exactly from `hardware/P1_WIRING.csv` and `docs/05_P1_Wiring_and_Electronics.md`. Perform continuity and E-stop tests with pumps disconnected before wet operation.

## 9. Water-only fixture test
1. Place all wet hardware in/above the >=5 L secondary spill tray; keep electronics outside the wet zone.
2. Fill with clean water at approximately 100 mm measured head and inspect all seams/plumbing.
3. Increase to 500 +/-25 mm only after the first inspection passes.
4. Confirm the only intended water exit is the 1.50 mm front orifice.
5. Press E-stop and verify actuator-bus voltage collapses while Pico remains powered.

Any fixture leak, electrical anomaly or uncontrolled fluid path blocks calibration and testing.
