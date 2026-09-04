#!/usr/bin/env python3
"""Fit actual-agent P1 pump delivery rates from measured volumetric trials."""
from __future__ import annotations

import csv
from hashlib import sha256
import json
from pathlib import Path
import statistics
import sys

MAX_RATE_CV = 0.10


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: python scripts/p1_pump_calibration.py <trials.csv> <calibration.json>", file=sys.stderr)
        return 2
    inp, out = Path(argv[1]), Path(argv[2])
    rows = list(csv.DictReader(inp.read_text(encoding="utf-8").splitlines()))
    rates: dict[str, list[float]] = {"A": [], "B": []}
    for row in rows:
        channel = row["channel"].strip().upper()
        if channel not in rates:
            raise ValueError(f"unknown channel {channel}")
        runtime = float(row["runtime_s"])
        volume = float(row["delivered_volume_ml"])
        if runtime <= 0 or volume <= 0:
            raise ValueError("runtime and delivered volume must be positive")
        rates[channel].append(volume / runtime)
    if any(len(v) < 3 for v in rates.values()):
        raise ValueError("at least three measured trials are required for each pump")
    mean_a = statistics.mean(rates["A"])
    mean_b = statistics.mean(rates["B"])
    cv_a = statistics.stdev(rates["A"]) / mean_a
    cv_b = statistics.stdev(rates["B"]) / mean_b
    if cv_a > MAX_RATE_CV or cv_b > MAX_RATE_CV:
        raise ValueError(f"pump calibration CV exceeds {MAX_RATE_CV:.2f}: A={cv_a:.4f}, B={cv_b:.4f}")
    artifact = {
        "schema_version": "1.0",
        "source_kind": "PHYSICAL_CALIBRATION",
        "method": "volumetric delivery of assigned P1 agents through installed tubing/nozzles",
        "pump_a_ml_s": mean_a,
        "pump_b_ml_s": mean_b,
        "pump_a_cv": cv_a,
        "pump_b_cv": cv_b,
        "maximum_allowed_cv": MAX_RATE_CV,
        "trial_count_a": len(rates["A"]),
        "trial_count_b": len(rates["B"]),
    }
    encoded = json.dumps(artifact, sort_keys=True, separators=(",", ":")).encode("utf-8")
    artifact["calibration_sha256"] = sha256(encoded).hexdigest()
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
