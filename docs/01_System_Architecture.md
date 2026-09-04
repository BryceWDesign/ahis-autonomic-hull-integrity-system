# AHIS v3 System Architecture

## Closed loop

`observe -> fuse -> localize -> classify -> gate -> allocate -> actuate -> monitor -> verify -> record -> requalify-or-degrade`

### Observe
AHIS accepts multiple evidence channels rather than treating one sensor as truth. The v3 software includes transparent fusion of channel score and channel quality, plus an anisotropic time-of-arrival localization model that reports an uncertainty radius.

### Gate
A repair command is denied when any hard interlock or resource requirement fails. P1 hard gates include E-stop state, sensor validity, hydrostatic head, pressure, calibrated pump rate, repair-agent availability, electrical-energy allowance and actuator-cycle budget.

### Actuate
The P1 reference article has two physically independent peristaltic delivery channels. Firmware controls them through MOSFET drivers only when the actuator-power relay is energized. A normally-closed E-stop path physically removes relay-coil power; a second NC contact is monitored by the Pico.

### Verify
P1 does not use visual inspection as its success metric. A load cell measures collected fluid mass so pre-response and post-response leak rates can be compared. Physical acceptance requires at least 80% measured leak-rate reduction from a baseline of at least 20 mL/min, while remaining within the low-energy test envelope.

### Record
`StructuralHistory` creates a SHA-256-linked event chain. Campaign receipts and physical-run receipts bind the evidence to its declared authority. HIL evidence is never accepted by the physical evidence parser.

## Advanced research layers
The v3 software also includes:
- finite repair-resource accounting;
- uncertainty-aware anisotropic localization;
- multimodal evidence fusion;
- digital-twin discrepancy screening;
- uncertainty-bounded fatigue/RUL screening;
- persistent structural history;
- deterministic HIL fault injection;
- physical-only acceptance logic.

These modules are deliberately auditable and dependency-light. They are research control infrastructure, not certified structural allowables.
