# Contributing to AHIS v3

AHIS v3 is source-available evaluation software, not an open-source project. Contributions are accepted only under terms compatible with the repository's `LICENSE`.

## Before submitting

- Open an issue or contact Bryce Lovell before substantial work.
- Do not submit proprietary third-party material, confidential data or content you do not have the right to contribute.
- Do not add simulated data that can be mistaken for physical evidence.
- Do not weaken `PHYSICAL_STATUS.json`, claim boundaries, hardware interlocks or evidence provenance.
- New physical-performance statements require actual measured evidence and must remain explicitly scoped.

## Code requirements

Run:

```bash
python -m pip install -e '.[dev]'
python check_green.py
```

A contribution must preserve the authoritative release gate, deterministic campaign behavior and physical-evidence firewall.

## Contribution license

Unless Bryce Lovell agrees otherwise in writing before submission, by intentionally submitting a contribution you represent that you have the right to submit it and agree that the contribution may be incorporated into AHIS and distributed by Bryce Lovell under the AHIS Evaluation License 1.0 and under separate commercial or other licenses offered by Bryce Lovell.

Submitting a contribution does not grant you commercial, operational, manufacturing, redistribution or sublicensing rights to AHIS beyond the rights in the repository license.
