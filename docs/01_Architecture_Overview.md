# AHIS — Architecture Overview
**Project:** Autonomic Hull Integrity System (AHIS)  
**Maintainer:** Bryce Lovell  
**Status:** Proof-of-Concept (PoC) architecture (not flight-qualified, not crew-rated)

---

## 1) System intent
AHIS is a **layered hull protection concept** plus an **instrumentation and verification harness**. It combines:
- **Passive, rate-dependent energy management** to reduce peak strain during impulsive events, and
- **Electromechanical SHM (Structural Health Monitoring)** using PVDF-based sensing and diagnostic excitation to detect and localize damage onset and growth.

The architecture is designed so each function can be evaluated independently:
- **Passive Mode:** passive stack only (no electronics required)
- **Instrumented Mode:** passive stack + PVDF SHM layer + data collection
- **Instrumented + Diagnostic Excitation:** adds waveform injection for impedance/FRF/guided-wave diagnostics
- **Optional Attenuation Mode:** adds damping/shunt/control strategies (explicitly experimental at PoC stage)

---

## 2) Subsystems
### 2.1 Layer Stack (mechanical)
**Purpose:** manage energy and load paths; limit damage propagation; maintain pressure boundary margin.

**Conceptual layers (implementation-specific):**
- Outer protective surface (coating/strike face; material-dependent)
- Passive rate-dependent interlayer (PressureX lineage; e.g., STF/viscoelastic encapsulated layer)
- Structural substrate (vehicle hull laminate/metal)
- Bonding interfaces and edge sealing (critical for durability)

**Measurable outputs:**
- Peak strain reduction (%)
- Peak acceleration reduction (g)
- Damage extent (area, delamination indicators)
- Leak initiation threshold and leak rate (when pressure boundary is tested)

### 2.2 PVDF SHM Skin (electromechanical)
**Purpose:** detect, trend, and localize damage; support diagnostic checks before/after events.

**Elements:**
- PVDF layer(s) as sensors (direct piezoelectric effect)
- Conductive electrode layer(s) to collect/drive signals
- Node layout (actuator/sensor placement geometry)
- Cabling/connectorization suited to the PoC environment

**Measurable outputs:**
- Detection time (ms/s)
- Localization error (cm)
- Baseline drift vs environment (Δ over thermal cycles, etc.)
- Signal-to-noise ratio and false positive rate (PoC reporting)

### 2.3 Waveform Driver (diagnostic excitation)
**Purpose:** inject controlled excitations for SHM methods:
- Impedance/admittance changes (electromechanical impedance)
- Frequency response function (FRF) tracking
- Guided-wave / multi-tone / chirp diagnostic energy injection

**Notes:**
- Any legacy “3/6/9” language is replaced by standard “multi-tone / chirp excitation.”
- Excitation parameters are chosen via modal/FRF considerations, not numerology.

**Measurable outputs:**
- Transfer-function changes vs baseline
- Repeatability and temperature dependence
- Excitation power budget (W) and thermal rise (°C)

### 2.4 Data Acquisition (DAQ) + Analysis
**Purpose:** capture synchronized signals and produce repeatable metrics.

**Signals (PoC):**
- PVDF voltage outputs
- Optional pressure sensor signals (if used for leak/pressure retention tests)
- Accelerometers / strain gauges (if used for impact/vibration tests)
- Environmental telemetry (temperature)

**Outputs:**
- Standardized results packages (raw + processed) following repo templates
- Metrics normalized by areal density and thickness

---

## 3) Data flow (closed-loop concept without over-claiming)
AHIS is framed as a closed-loop integrity system, but PoC stages may implement only the early steps.

1) **Detect:** event signatures from PVDF/strain/accel/pressure
2) **Localize:** estimate region of damage using node response changes (cm error target defined in requirements)
3) **Assess:** estimate severity (classification bins; PoC)
4) **Mitigate (optional):** mitigation planning and isolation (architecture placeholder unless built)
5) **Verify:** post-event diagnostic excitation and comparison to baseline

At PoC stage, “Mitigate” is typically **procedural** unless a specific actuator/repair mechanism is introduced and tested.

---

## 4) Interfaces (what must be defined for composability)
### 4.1 Mechanical interfaces
- Layer thickness (mm), areal density (kg/m²)
- Bondline type and cure process (if used)
- Edge sealing method (leak paths and durability are dominated here)
- Mounting/fixture boundary conditions for tests

### 4.2 Electrical interfaces
- PVDF electrode routing and shielding approach
- Driver output envelope (Vpp limit defined by PoC safety constraints)
- DAQ input range and sampling rate (must be justified by expected bandwidth)

### 4.3 Data interfaces
- Standard file naming and directory layout for results packages
- Units and calibration metadata required for every dataset

---

## 5) Key architectural risks (must be closed by tests)
- Rate-dependent layer behavior across temperature (drift / freezing / softening)
- Vacuum/outgassing compatibility of polymers/adhesives/encapsulants
- Bondline fatigue and delamination growth
- PVDF baseline drift and depolarization risk
- Electrode cracking/corrosion/delamination
- EMI/ESD susceptibility in instrumented mode

Each risk maps to `docs/06_Failure_Modes_and_Risks.md` and the test matrix.

---

## 6) What makes this architecture “serious”
- Passive performance is evaluated even with **zero electronics**
- Instrumented claims are limited to **SHM detection/localization** and are tied to metrics
- “Auto-repair” is not claimed unless a defined mechanism is added and validated
- All PoC outputs are normalized by mass/thickness and reported with limitations

---
End of architecture overview.
