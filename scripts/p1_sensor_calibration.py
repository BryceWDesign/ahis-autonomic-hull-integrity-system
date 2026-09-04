#!/usr/bin/env python3
"""Fit P1 pressure and load-cell calibration from measured physical reference points."""
from __future__ import annotations

import csv
from hashlib import sha256
import json
from pathlib import Path
import sys

KPA_PER_MM_WATER = 0.00980665
MAX_PRESSURE_FIT_RESIDUAL_KPA = 0.15
MAX_LOADCELL_FIT_RESIDUAL_G = 2.0


def fit(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    if len(xs) != len(ys) or len(xs) < 3:
        raise ValueError("at least three paired calibration points are required")
    xbar, ybar = sum(xs) / len(xs), sum(ys) / len(ys)
    denom = sum((x - xbar) ** 2 for x in xs)
    if denom <= 0:
        raise ValueError("calibration reference values must span a range")
    slope = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / denom
    intercept = ybar - slope * xbar
    max_residual = max(abs((slope * x + intercept) - y) for x, y in zip(xs, ys))
    return slope, intercept, max_residual


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: python scripts/p1_sensor_calibration.py <pressure.csv> <loadcell.csv> <out.json>", file=sys.stderr)
        return 2
    pressure_rows = list(csv.DictReader(Path(argv[1]).read_text(encoding="utf-8").splitlines()))
    load_rows = list(csv.DictReader(Path(argv[2]).read_text(encoding="utf-8").splitlines()))
    if len(pressure_rows) < 4:
        raise ValueError("pressure calibration requires at least four measured head points")
    if len(load_rows) < 4:
        raise ValueError("load-cell calibration requires at least four measured masses")
    adc = [float(r["adc_fraction"]) for r in pressure_rows]
    if any(not 0.0 <= v <= 1.0 for v in adc):
        raise ValueError("adc_fraction must be between zero and one")
    kpa = [float(r["reference_head_mm"]) * KPA_PER_MM_WATER for r in pressure_rows]
    p_slope, p_intercept, p_resid = fit(adc, kpa)
    if p_slope <= 0:
        raise ValueError("pressure calibration slope must be positive")
    if p_resid > MAX_PRESSURE_FIT_RESIDUAL_KPA:
        raise ValueError(f"pressure calibration residual {p_resid:.6f} kPa exceeds {MAX_PRESSURE_FIT_RESIDUAL_KPA} kPa")

    masses = [float(r["reference_mass_g"]) for r in load_rows]
    counts = [float(r["hx711_counts"]) for r in load_rows]
    c_per_g, zero_counts, count_resid = fit(masses, counts)
    if c_per_g == 0:
        raise ValueError("load-cell calibration slope cannot be zero")
    mass_resid_g = abs(count_resid / c_per_g)
    if mass_resid_g > MAX_LOADCELL_FIT_RESIDUAL_G:
        raise ValueError(f"load-cell calibration residual {mass_resid_g:.6f} g exceeds {MAX_LOADCELL_FIT_RESIDUAL_G} g")

    artifact = {
        "schema_version": "1.0",
        "source_kind": "PHYSICAL_CALIBRATION",
        "pressure_kpa_per_adc_fraction": p_slope,
        "pressure_offset_kpa": p_intercept,
        "pressure_max_fit_residual_kpa": p_resid,
        "loadcell_counts_per_g": c_per_g,
        "loadcell_zero_counts": zero_counts,
        "loadcell_max_fit_residual_g": mass_resid_g,
        "pressure_point_count": len(pressure_rows),
        "loadcell_point_count": len(load_rows),
        "acceptance_limits": {
            "pressure_max_fit_residual_kpa": MAX_PRESSURE_FIT_RESIDUAL_KPA,
            "loadcell_max_fit_residual_g": MAX_LOADCELL_FIT_RESIDUAL_G
        }
    }
    digest = sha256(json.dumps(artifact, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    artifact["calibration_sha256"] = digest
    Path(argv[3]).write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(argv[3])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
