# Digital Twin, Prognostics and Structural Memory

## Digital-twin discrepancy screen
The digital-twin module compares measured modal frequencies, static strain and leak rate with a declared baseline using explicit tolerances. A discrepancy is evidence that either structure, environment or model has changed; it is not automatically labeled as one damage type.

## Prognostics
The RUL screen reports lower, nominal and upper cycle counts from a declared cumulative-damage state and uncertainty. The result is explicitly marked `SCREEN_ONLY_UNCERTIFIED`. It exists to make uncertainty unavoidable in maintenance logic, not to replace qualified S-N data or fracture mechanics.

## Structural memory
The history module creates a SHA-256 chain across damage, repair, verification and maintenance events. A later repair cannot erase earlier fatigue or damage history. Tampering with a stored event breaks chain verification.
