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


## v4 scope

The 54-row P1 procurement BOM and P1 build records are retained. They are complete for that low-energy reference article, not for a hypothetical flight hull or new material stack. No new physical apparatus is required for v4's software/HIL campaign.

`SOFTWARE_BOM_V4.json` and `.csv` enumerate the pinned local runtime and validation/build distributions. Distribution license notices are retained under `third_party_notices/`, including bundled numerical-library notices where supplied by the distributions. Windows-only transitive packages can differ; the validation dependency pins and CI matrix identify the intended reproducibility environment.

R6-R9 need formulation, geometry, instrumentation and procurement selection after an actual test article is defined. The stack density/thickness registry is a design screen, not an orderable qualified material BOM. R10 has no procurement or construction package because it is not implemented.
