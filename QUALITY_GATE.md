# AHIS v3.0.0 Quality Gate

The authoritative command is:

```bash
python check_green.py
```

A GREEN result requires all of the following in the delivered tree:

- Python compilation;
- exactly 112 passing repository tests for this release;
- deterministic v3 software/HIL campaign with all pass conditions true;
- unchanged software/HIL-only campaign authority and canonical receipt;
- explicit AHIS Evaluation License 1.0 boundary and Bryce Lovell licensing contact;
- all physical demonstration/certification flags false;
- complete P1 procurement/build/control/CAD package;
- generated P1 CAD envelopes matching the registered dimensions;
- no unresolved release markers, symlinks or runtime cache junk;
- complete SHA-256 manifest with no missing, modified or unmanifested released files.

GREEN is a repository/software release status. `PHYSICAL_STATUS.json` remains the independent physical-claim authority.
