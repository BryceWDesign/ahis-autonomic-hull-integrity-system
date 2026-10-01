# AHIS v4.0.2 quality gate

Run `python check_green.py` from the repository root after installing the pinned validation dependencies.

GREEN requires exactly 224 passing release tests; compilation; v4 lint/format; the retained v3 campaign and canonical digest; 31 fresh v4 case outcomes and archived replay; successful tamper negative controls; machine-readable claim/test mapping; all R1-R10 physical flags false; evaluation licensing; P1's 54-row procurement/build/control package; six CAD envelopes; release hygiene; and a complete unchanged manifest.

Lint and format gates cover the new survival package, CLI entry and v4 tests. They do not claim a new whole-repository lint certification for inherited source. The entire tree is compiled and its complete tests run.

The gate does not silently repair a release, refresh its manifest or promote a physical claim. `scripts/run_v4_campaign.py` and `scripts/make_manifest.py` are explicit developer regeneration tools, not a way to override a failure without investigation.

A GREEN local gate is not evidence that GitHub Actions ran. The included matrix targets Linux Python 3.11/3.12 and Windows Python 3.13. Check its actual run after pushing.
