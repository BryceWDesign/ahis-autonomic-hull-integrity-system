# Third-Party Notices

AHIS v3 runtime code is written against the Python standard library and does not vendor
third-party Python packages. `pytest` is a development/test dependency. `pyserial` is
an optional host-side dependency for direct communication with the P1 Pico 2 article.

The reference build names commercially available components from their manufacturers.
Manufacturer names and product marks belong to their respective owners. Product links
are procurement/traceability references, not endorsements or bundled third-party code.

Research papers, standards, NASA technical material, and manufacturer data sheets are
cited by reference only. Their text, drawings, and data sheets are not redistributed
inside this repository unless the applicable terms expressly permit redistribution.

Historical AHIS releases were distributed under Apache License 2.0. The historical
license text is retained in `LICENSES/Apache-2.0-historical.txt` solely to preserve the
version boundary.


## v4 numerical and validation dependencies

NumPy and SciPy are runtime dependencies. Pytest, Ruff, build and setuptools plus their recorded supporting distributions are validation/build dependencies. Their own distribution notices govern them; see `BOM/SOFTWARE_BOM_V4.json` and `BOM/third_party_notices/`. The AHIS evaluation license does not restrict those distributions.

IX-SymmetryLock supplied design context for established control mathematics. The AHIS implementation is documented in `provenance/UPGRADE_V4.json`; no fusion-field implementation is bundled into AHIS.
