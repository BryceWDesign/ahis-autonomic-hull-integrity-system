# Design Review Checklist

Before calling a future AHIS change release-ready, answer every item with evidence.

## Software
- Does every actuator path fail closed on E-stop, pressure, sensor and resource faults?
- Are synthetic/HIL and physical evidence types impossible to confuse programmatically?
- Are all claim boundaries machine-readable?
- Are algorithms deterministic where the campaign expects deterministic receipts?
- Are calibration identities bound to physical run records?

## Mechanical
- Does CAD match the BOM and build traveler?
- Are sealing surfaces and controlled-orifice dimensions inspected?
- Is the hydrostatic source physically incapable of accidental compressed-gas pressurization in the canonical setup?
- Are wet and electrical zones segregated?

## Measurement
- Is each sensor calibrated in final installed configuration?
- Are pump rates measured with actual agents and tubing?
- Is leak rate measured rather than visually estimated?
- Are fixture leaks separately ruled out?

## Claims
- Does any prose imply structural healing where only sealing was tested?
- Does any manufacturer or literature number appear as if it were AHIS test data?
- Are return-to-service and certification claims still externally gated?
