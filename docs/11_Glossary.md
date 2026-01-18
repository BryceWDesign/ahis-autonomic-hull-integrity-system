# AHIS — Glossary
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** PoC reference

---

## Terms
**Acceptance Criteria**  
Pass/fail thresholds defined for a metric under a specified test method and conditions.

**Areal Density (kg/m²)**  
Mass per unit area of a panel or layer stack. Used to normalize performance deltas.

**Baseline Panel**  
A coupon or structure without AHIS layers, tested under the same conditions as AHIS configurations.

**Bondline**  
The adhesive/interface region between layers. Common failure origin for laminated structures.

**Chirp (Swept-Frequency Excitation)**  
A waveform whose frequency increases or decreases over time, used to excite a broad band for diagnostics.

**Coupon**  
A test sample panel of defined geometry used for controlled laboratory evaluation.

**DAQ (Data Acquisition)**  
Hardware/software used to sample sensor signals (voltage, acceleration, strain, pressure) at known rates with calibrated ranges.

**Damage Extent**  
A measurable representation of damage, e.g., crack length, delamination area, dent depth, or other defined indicator.

**Delamination**  
Separation between layers in a composite/laminate stack, often driven by interlaminar stresses and bondline weaknesses.

**Detection Time**  
Time from a defined event onset (impact/leak threshold) to the system’s detection report.

**Electromechanical Impedance (EMI) SHM (not electromagnetic interference)**  
A structural health monitoring method where electrical impedance/admittance measured at a piezoelectric element changes with structural boundary conditions and damage state.

**Electrode Layer**  
Conductive layer used to collect or apply electric fields to PVDF elements (material can vary; not inherently “graphene-only”).

**ESD (Electrostatic Discharge)**  
A sudden electrostatic discharge event that can disrupt or damage electronics and high-impedance sensing lines.

**Failure Mode**  
A specific mechanism by which the system fails (e.g., bondline delamination, wiring fatigue, baseline drift).

**FRF (Frequency Response Function)**  
The frequency-domain relationship between input excitation and measured output; used for modal/diagnostic tracking.

**Guided Waves (e.g., Lamb waves)**  
Elastic waves that propagate along thin plates/shells; damage alters time-of-flight, attenuation, and scattering.

**Impact (Low-Velocity, PoC scope)**  
A controlled strike event where deformation and damage occur without assuming hypervelocity fragmentation physics.

**Instrumented Mode**  
AHIS configuration including PVDF sensing, routing, and DAQ, intended for SHM measurements.

**Leak Rate**  
Rate of pressure decay or flow through a boundary compromise, measured in defined units (e.g., Pa/s or sccm) under specified conditions.

**Localization Error (cm)**  
Distance between estimated damage location and known ground-truth location.

**Modal Frequency**  
A resonant frequency associated with a structural mode; damage and boundary changes can shift modal parameters.

**MMOD (Micrometeoroid and Orbital Debris)**  
Orbital debris threats that often involve hypervelocity impacts. AHIS PoC does not claim MMOD protection unless tested.

**Passive Mode**  
AHIS configuration that includes only passive layer(s) without electronics.

**Piezoelectric Effect (Direct)**  
Mechanical stress/strain generating electric charge/voltage in a piezoelectric material (sensing).

**Piezoelectric Effect (Inverse)**  
Applied electric field generating mechanical strain in a piezoelectric material (actuation/excitation).

**PoC (Proof-of-Concept)**  
A demonstration intended to validate feasibility and measurement workflow, not flight qualification.

**Pressure Boundary**  
A structure intended to contain a pressure differential; failure includes leaks or rupture.

**Repeatability**  
Ability to produce consistent results under repeated tests with controlled conditions.

**SNR (Signal-to-Noise Ratio)**  
Ratio of signal amplitude/power to noise amplitude/power; higher is better for reliable detection.

**Shunt Damping**  
Using an electrical network connected to a piezoelectric element to dissipate mechanical energy via electromechanical coupling.

**Strain (µε)**  
Deformation measure; microstrain (µε) is strain × 10⁶.

**Thermal Cycling**  
Repeated temperature excursions used to stress materials, bondlines, and sensors to observe drift/failure.

**Transmissibility (dB)**  
Ratio of response amplitude at one location to input amplitude, often used to measure vibration isolation/attenuation.

**Vpp (Volts peak-to-peak)**  
Voltage difference between waveform maximum and minimum.

---

## Naming discipline note
AHIS does not use nonstandard terms such as “nullification” or numerology-based “3/6/9” framing. All concepts must be expressed in standard engineering terminology.

---
End of glossary.
