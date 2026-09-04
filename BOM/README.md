# AHIS-P1 Procurement BOM

`AHIS-P1-procurement.csv` is the canonical procurement list for the v3 low-energy
reference article. Each row is either an exact manufacturer part or an exact functional
stock specification. There are no unresolved procurement fields in the canonical P1
build.

Vendor-neutral stock is intentional where manufacturer identity does not affect the
reference article. Performance-critical electronics and chemistry use named parts.
Any substitution must be recorded in the build traveler and is a **variant article**
until the relevant calibration and acceptance steps are repeated.

The P1 BOM is not a full-scale hull BOM. It constructs the low-energy autonomous
leak-seal research article described in `docs/03_P1_Reference_Design.md`.
