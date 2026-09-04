# P1 Reference Design

## Article
`AHIS-P1-LOW-ENERGY-LEAK-SEAL-CELL`

P1 is a transparent, low-energy hydrostatic test cell. It exists to prove or falsify the full autonomy chain with real sensors, real fluid delivery and real measured leak rate without invoking pressure-vessel or structural-hull claims.

## Cell geometry
All dimensions are millimetres unless noted.

- overall plate size: 150 x 150;
- front plate: clear polycarbonate, 6 thick;
- back plate: clear polycarbonate, 6 thick;
- center spacer: clear polycarbonate, 10 thick;
- spacer cavity: 100 x 100 through opening;
- front and back gaskets: silicone sheet, 1.5 thick each, Shore A 40-60;
- fasteners: twelve M5 x 35 A2-70 stainless screws with flat washers and nylon-insert nuts;
- fastener holes: 5.5 diameter at the coordinates encoded in `hardware/cad/generate_cad.py`;
- controlled damage orifice: 1.50 +/-0.05 diameter at front-plate center;
- water bulkhead opening: 17.0 diameter in back plate for John Guest PI1208S-US.

The assembled spacer/gasket gap target is 12.4 +/-0.1 mm. This corresponds to approximately 20% compression of each 1.5 mm gasket around the 10 mm spacer. Tighten in a cross pattern while measuring the plate-to-plate gap at four sides. Do not substitute an arbitrary torque target for gap control.

## Hydrostatic source
The reservoir is open to atmosphere. Nominal water head is 500 mm above the front-plate orifice. The hard software and hardware-test envelope is 800 mm head and 8 kPa differential pressure. Compressed gas and pump pressurization are prohibited for P1.

Pressure is measured through a **trapped dry-air leg** connected to the water line. The MPX5010DP is not intentionally exposed to liquid. Mount the sensor above the highest water level and route the pressure branch upward so gravity returns any accidental liquid toward the water line.

## Leak measurement
Escaping water falls into a 500 mL catch cup mounted on the 1 kg load cell. The HX711 digitizes mass. Leak rate is obtained from the mass-versus-time slope. The measurement path must be calibrated after the final load-cell mechanical mount is complete.

## Repair surrogate
P1 uses two dedicated delivery lines:

- Agent A: 2.0% w/v sodium alginate in DI water.
- Agent B: 5.0% w/v calcium chloride dihydrate in DI water.

Each pump is calibrated with its **actual assigned agent and installed tubing/nozzle**. The canonical target is 8.0 mL Agent A followed by 8.0 mL Agent B. Maximum single-pump runtime is 30 s. After delivery, wait 60 s before the post-response leak-rate window.

This chemistry is a system-level sealing surrogate. It is not an ionomer hull liner, a structural composite repair, or proof of self-healing load capacity.

## Nozzle geometry
The generated nozzle bracket holds two 4 mm OD / 2 mm ID silicone tubes with their ends located symmetrically around the damage orifice. The bracket keeps the wetted paths separate until discharge. Inspect that both outlets are unobstructed before every run.
