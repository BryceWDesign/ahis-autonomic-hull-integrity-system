# AHIS v4.0.2 full handoff

The archive contains the complete repository, retained P1 hardware package, both campaigns, validation records and an installable Python wheel. Begin in the `AHIS-v4.0.2` directory. The repository has no included `.git` directory and does not overwrite your existing Git history.

## Windows PowerShell

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-validation.txt
.\.venv\Scripts\python.exe -m pip install --no-build-isolation -e .
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe check_green.py
```

Use `py -3.12` or `py -3.11` if that is your installed supported Python. Activation is optional; the commands use the interpreter directly.

## Linux/macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-validation.txt
.venv/bin/python -m pip install --no-build-isolation -e .
.venv/bin/python -m pip check
.venv/bin/python check_green.py
```

## Run and audit the reference

Run generated work outside the release tree so the integrity manifest continues to describe only release files:

```powershell
.\.venv\Scripts\python.exe -m ahis decide configs/survival_reference.json --out ../nominal-evidence.json
.\.venv\Scripts\python.exe -m ahis audit ../nominal-evidence.json
.\.venv\Scripts\python.exe -m ahis campaign --config configs/survival_reference.json --out ../my-survival-campaign
```

`decide` returns 0 for RECOVERED_LIMITED, 2 for an isolated/rejected decision, and 1 for invalid input. `audit` and `campaign` return nonzero on a failed check. These commands perform no hardware dispatch. A digest printed by `decide` can be retained separately and supplied to `audit --trusted-digest`.

## Updating an existing Git checkout

Create an upgrade branch in your existing clone. Copy the contents of `AHIS-v4.0.2` into that clone, preserving its `.git` directory. The v3 workflow is replaced by `.github/workflows/quality.yml`; remove any remaining duplicate v3 release workflow. Review `git diff --stat`, run the gate, then commit and push the branch. Do not reinitialize an existing repository or force-push.

The evaluation license and Bryce Lovell contact are retained. No patent freedom-to-operate guarantee or operational approval is supplied. Read `VALIDATION_REPORT.md` for what was actually run locally, and `docs/claims_v4.json` for implemented versus screened versus unimplemented capabilities.
