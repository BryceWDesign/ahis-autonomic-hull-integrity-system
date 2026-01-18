# AHIS — Full Bill of Materials (BOM)
**Version:** 0.1 (derived-from-legacy; placeholders preserved)  
**Author:** Bryce Lovell  
**Scope:** Proof-of-concept (PoC) materials + instrumentation + test equipment.

## What this BOM is
This BOM consolidates items explicitly referenced in the two legacy inputs used to form AHIS:
- PressureX zip (notably `hardware/bom.csv` and test protocol equipment lists)
- IX-Thaed-Armor zip (notably `BOM/IX-Thaed-Armor_BillOfMaterials.md`, `hardware/PVDF_Waveform_Driver.md`, and `docs/Power_Interface.md`)

This BOM is intentionally strict:
- **No invented vendor SKUs**
- **No assumed part numbers**
- If the legacy source was generic/placeholder, it stays generic/placeholder here.

## What this BOM is NOT
- Not a flight bill of materials
- Not a procurement-ready BOM for production
- Not a certification or safety claim

---

# A) Hull / Armor Materials (Layer Stack Concepts)
**Source:** IX-Thaed-Armor legacy BOM (material categories and examples as written; truncated specs remain “TBD”).

| Item # | Material / Layer | Legacy Notes | Typical PoC Form Factor | Vendor Examples (as legacy-style examples) |
|---:|---|---|---|---|
| A1 | Conductive sheet electrode layer | Graphene mentioned as an option; treat as “conductive electrode layer” for manufacturability | 12"×12" sheet | Graphenea, ACS Materials |
| A2 | Adhesion seed layer | Ti or Cr thin adhesion layer for noble-metal deposition | thin film process | Kurt J. Lesker (process supplies) |
| A3 | Conductive coating / plating | Gold plating referenced in legacy notes; any conductive coating must be documented | deposition session / coating | Sigma-Aldrich (materials), process vendors |
| A4 | PVDF piezoelectric layer | PVDF mesh/film referenced; used for sensing/diagnostic excitation | film/mesh sheet | TDK, Measurement Specialties (examples) |
| A5 | Damping / matrix layer | Silicone/ceramic blend referenced; treat as “damping matrix candidate” | sheet/cast layer | Momentive, Wacker (examples) |
| A6 | Transfer/bonding polymer (if used) | Graphene transfer polymers referenced (PVA/PMMA) | consumable | common lab supply |

**Notes:**
- If you choose to actually use graphene, document transfer method, electrode routing, and durability risks.
- If you substitute a different electrode material (foil/mesh), document it and keep the SHM method intact.

---

# B) Passive Energy-Management Layer (PressureX Lineage)
**Source:** PressureX concepts (materials described generically; PoC requires explicit material selection and screening).

| Item # | Category | Examples Mentioned | PoC Notes (must be specified before build) |
|---:|---|---|---|
| B1 | Rate-dependent interlayer candidate | Silica-in-PEG style STF candidates | Must define mix, encapsulation, thickness, and temperature envelope |
| B2 | Encapsulation membrane candidate | TPU/fluoropolymer style membranes | Must define seam method, permeability, and edge sealing |
| B3 | Edge sealing materials | not specified in legacy BOM | Must specify seal approach; dominates leak behavior |

**Important:** The passive layer is only “real” after comparative testing per `docs/07_Test_Matrix.md`.

---

# C) Optional Instrumentation / Electronics (PoC)
## C1) PressureX prototyping BOM (as provided; placeholders preserved)
**Source:** PressureX `hardware/bom.csv` (placeholder part numbers retained).

| Component | Description | Part Number | Supplier | Qty | Notes |
|---|---|---|---|---:|---|
| Pressure Sensor | XYZ123 Pressure Sensor | XYZ123 | ExampleSupplier | 1 | Placeholder; replace with real sensor for leak tests |
| Microcontroller | ESP32 Dev Kit | ESP32-DEVKIT | ESP32-Supplier | 1 | Prototyping controller |
| Power Supply | 5V regulated supply | PS-5V | Generic | 1 | Stable supply for PoC bench |
| Wires | Jumper wires | — | Generic | Various | Prototyping wiring |
| Breadboard | Solderless breadboard | BB-830 | Generic | 1 | Prototype only |

## C2) PVDF waveform driver options (as referenced in legacy doc)
**Source:** `hardware/PVDF_Waveform_Driver.md` (explicit option names retained).

- **Option 1:** Arduino Nano + AD9833 waveform module
- **Option 2:** Teensy 4.1 + DAC + AudioShield
- **Pico-based driver (explicitly referenced in pinout section):**
  - Raspberry Pi Pico
  - MCP4725 DAC
  - Op-amp buffer stage
  - Frequency selector (DIP switch or logic)
  - Wave select switch (tactile)
  - 5V buck converter (logic power)
  - PCB or breadboard + headers/wiring

**Electrical envelope (legacy-stated):**
- Supply: 3.3V or 5V (Power_Interface.md)
- Current: ~25–40 mA (legacy note; depends on size and gain)
- Safety note: do not exceed the PVDF drive envelope stated in legacy driver notes unless independently validated.

---

# D) Test Equipment (explicitly implied by protocols)
AHIS inherits the test discipline from the repo docs. If you claim a test, you must have the equipment.

## D1) Impact / shock (T-IMP-010 / T-IMP-011)
- Repeatable impact method (drop rig or actuator) with documented striker geometry
- DAQ capable of sampling required bandwidth
- Strain gauge(s) and/or accelerometer(s)
- Fixture to control boundary conditions (clamps, plates, torque method)

## D2) Thermal cycling (T-THM-030)
- Thermal chamber (or equivalent controlled setup)
- Temperature logging at the coupon/fixture
- Pre/post baseline capture for drift tracking

## D3) Vibration (T-VIB-040)
- Shaker or controlled vibration setup
- Accelerometers + mounting methods
- Pre/post inspection and continuity checks

## D4) Pressure/leak (T-PRS-050)
- Sealed fixture/test volume method
- Pressure sensor/logger (calibrated)
- Clearly defined leak onset rule and leak rate computation

## D5) EMI/ESD (T-EMI-070)
- ESD-safe handling and logging at minimum
- If equipment available: ESD simulator and/or EMI exposure environment

---

# E) Procurement and qualification gates (mandatory discipline)
Before any operational claims:
- Material compatibility screening (temperature, vacuum/outgassing if relevant, moisture if relevant)
- Bondline and edge sealing durability under cycling
- SHM baseline drift characterization vs environment
- Actuator authority / stability margins for Mode E (if used)

---

# Change log
- v0.1: Initial consolidated AHIS BOM derived strictly from legacy repos; placeholders preserved.
