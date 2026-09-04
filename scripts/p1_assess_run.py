#!/usr/bin/env python3
"""Assess one measured P1 run JSON and emit an evidence receipt."""
from __future__ import annotations

from dataclasses import asdict, fields
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ahis.physical import P1RunEvidence, assess_p1_run, physical_run_receipt


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python scripts/p1_assess_run.py <physical-run.json>", file=sys.stderr)
        return 2
    path = Path(argv[1]).resolve()
    raw = json.loads(path.read_text(encoding="utf-8"))
    allowed = {f.name for f in fields(P1RunEvidence)}
    missing = allowed - set(raw)
    if missing:
        raise ValueError(f"physical run missing fields: {sorted(missing)}")
    run = P1RunEvidence(**{name: raw[name] for name in allowed})
    assessment = assess_p1_run(run)
    result = {
        "run": raw,
        "assessment": asdict(assessment),
        "receipt_sha256": physical_run_receipt(run),
        "claim_boundary": "P1_LOW_ENERGY_LEAK_SEAL_ONLY__NO_STRUCTURAL_STRENGTH_OR_HULL_SURVIVABILITY_CREDIT",
    }
    out = path.with_suffix(".assessment.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out)
    return 0 if assessment.passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
