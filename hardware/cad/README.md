# AHIS-P1 CAD

The STEP/STL files in this directory are generated from `generate_cad.py` and the fixed P1 geometry in `configs/p1_reference.json`.

Canonical parts:
- front plate: 150 x 150 x 6 mm, 1.5 mm center orifice, 12 fastener holes;
- back plate: 150 x 150 x 6 mm, registered 17 mm fluid opening, 12 fastener holes;
- spacer: 150 x 150 x 10 mm with 100 x 100 mm cavity;
- gasket: 150 x 150 x 1.5 mm with 100 x 100 mm cavity;
- two-line nozzle bracket;
- 22 mm E-stop panel.

`dimensions.json` is the machine-readable dimensional registry. The generated solids are low-energy bench-fixture references only; they are not pressure-vessel or hull drawings.

CadQuery is needed only to regenerate CAD, not to run normal AHIS tests. The released STEP/STL outputs are covered by `MANIFEST.sha256`.
