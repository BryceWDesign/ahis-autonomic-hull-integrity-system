#!/usr/bin/env python3
"""
AHIS PoC Analysis — Normalization Utilities (Mass/Area/Thickness Discipline)

Purpose
-------
Provide strict, unit-explicit utilities for computing:
- areal density (kg/m^2) from mass and area
- thickness (mm) checks
- added mass fraction (%) relative to baseline
- normalized performance deltas:
    - delta_per_areal_density  (metric_delta / (kg/m^2))
    - delta_per_thickness_mm   (metric_delta / mm)

This script does NOT guess units. You must provide:
- mass in grams (g) OR kilograms (kg) explicitly
- area in square meters (m^2)
- thickness in millimeters (mm)

It also includes a small CLI to compute panel normalization metrics from a metadata CSV.

Input Metadata CSV (required columns)
-------------------------------------
At minimum:
- coupon_id
- config                (A/B/C/D or your declared scheme)
- mass_g                (mass in grams)  OR mass_kg (mass in kilograms)
- area_m2               (area in square meters)
- thickness_mm          (thickness in millimeters)

Optional:
- group                 (e.g., baseline, ahis) for later group comparisons
- notes                 (free text)

Outputs
-------
- normalized_panel_metrics.csv (computed areal_density_kg_m2, etc.)

Usage Example
-------------
python3 normalization_utils.py \
  --input results/T-IMP-010/RUN_YYYY-MM-DD_XYZ/processed/panel_metadata.csv \
  --output results/T-IMP-010/RUN_YYYY-MM-DD_XYZ/processed/normalized_panel_metrics.csv

Where panel_metadata.csv might look like:
coupon_id,config,group,mass_g,area_m2,thickness_mm,notes
AHIS-PANEL-001,A,baseline,123.4,0.0100,2.10,baseline coupon
AHIS-PANEL-002,B,ahis,165.2,0.0100,3.05,passive layer added
"""

from __future__ import annotations

import argparse
import csv
import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class PanelMetrics:
    coupon_id: str
    config: str
    group: str
    mass_kg: float
    area_m2: float
    thickness_mm: float
    areal_density_kg_m2: float
    notes: str


REQUIRED_BASE_COLS = {"coupon_id", "config", "area_m2", "thickness_mm"}
MASS_COL_OPTIONS = ("mass_g", "mass_kg")


def _parse_float(value: str, *, path: str, col: str, row_idx: int) -> float:
    try:
        return float(value)
    except Exception as e:
        raise ValueError(
            f"Non-numeric value in {path} at row {row_idx+2} col '{col}': {value!r}"
        ) from e


def areal_density_kg_m2(*, mass_kg: float, area_m2: float) -> float:
    if mass_kg <= 0:
        raise ValueError("mass_kg must be > 0")
    if area_m2 <= 0:
        raise ValueError("area_m2 must be > 0")
    return mass_kg / area_m2


def added_mass_fraction_percent(*, baseline_mass_kg: float, test_mass_kg: float) -> float:
    if baseline_mass_kg <= 0:
        raise ValueError("baseline_mass_kg must be > 0")
    return ((test_mass_kg - baseline_mass_kg) / baseline_mass_kg) * 100.0


def normalize_delta_per_areal_density(*, metric_delta: float, areal_density_kg_m2_value: float) -> float:
    """
    Returns metric_delta divided by areal density (kg/m^2).
    You must interpret units: (metric units) / (kg/m^2).
    """
    if areal_density_kg_m2_value <= 0:
        raise ValueError("areal_density_kg_m2_value must be > 0")
    return metric_delta / areal_density_kg_m2_value


def normalize_delta_per_thickness_mm(*, metric_delta: float, thickness_mm: float) -> float:
    """
    Returns metric_delta divided by thickness in mm.
    You must interpret units: (metric units) / mm.
    """
    if thickness_mm <= 0:
        raise ValueError("thickness_mm must be > 0")
    return metric_delta / thickness_mm


def _read_panel_rows(path: str) -> List[Dict[str, str]]:
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header row: {path}")
        headers = set(reader.fieldnames)

        missing = REQUIRED_BASE_COLS - headers
        if missing:
            raise ValueError(f"Missing required columns in {path}: {sorted(missing)}")

        if not any(m in headers for m in MASS_COL_OPTIONS):
            raise ValueError(
                f"Missing mass column in {path}. Provide one of: {MASS_COL_OPTIONS}"
            )

        rows: List[Dict[str, str]] = []
        for row in reader:
            rows.append(row)
        if not rows:
            raise ValueError(f"No data rows in {path}")
        return rows


def _row_mass_kg(row: Dict[str, str], *, path: str, row_idx: int) -> float:
    mass_g = (row.get("mass_g") or "").strip()
    mass_kg = (row.get("mass_kg") or "").strip()

    if mass_kg:
        m = _parse_float(mass_kg, path=path, col="mass_kg", row_idx=row_idx)
        if m <= 0:
            raise ValueError(f"mass_kg must be > 0 in {path} row {row_idx+2}")
        return m

    if mass_g:
        mg = _parse_float(mass_g, path=path, col="mass_g", row_idx=row_idx)
        if mg <= 0:
            raise ValueError(f"mass_g must be > 0 in {path} row {row_idx+2}")
        return mg / 1000.0

    raise ValueError(f"Row {row_idx+2} in {path} has neither mass_g nor mass_kg populated.")


def _to_panel_metrics(path: str, rows: List[Dict[str, str]]) -> List[PanelMetrics]:
    out: List[PanelMetrics] = []
    for i, r in enumerate(rows):
        coupon_id = (r.get("coupon_id") or "").strip()
        config = (r.get("config") or "").strip()
        group = (r.get("group") or "").strip() or "unspecified"
        notes = (r.get("notes") or "").strip()

        if not coupon_id:
            raise ValueError(f"Empty coupon_id in {path} at row {i+2}")
        if not config:
            raise ValueError(f"Empty config in {path} at row {i+2}")

        area_m2 = _parse_float((r.get("area_m2") or "").strip(), path=path, col="area_m2", row_idx=i)
        thickness_mm = _parse_float((r.get("thickness_mm") or "").strip(), path=path, col="thickness_mm", row_idx=i)
        if area_m2 <= 0:
            raise ValueError(f"area_m2 must be > 0 in {path} row {i+2}")
        if thickness_mm <= 0:
            raise ValueError(f"thickness_mm must be > 0 in {path} row {i+2}")

        mass_kg = _row_mass_kg(r, path=path, row_idx=i)
        ad = areal_density_kg_m2(mass_kg=mass_kg, area_m2=area_m2)

        out.append(
            PanelMetrics(
                coupon_id=coupon_id,
                config=config,
                group=group,
                mass_kg=mass_kg,
                area_m2=area_m2,
                thickness_mm=thickness_mm,
                areal_density_kg_m2=ad,
                notes=notes,
            )
        )
    return out


def _write_normalized_csv(out_path: str, panels: List[PanelMetrics]) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "coupon_id",
            "config",
            "group",
            "mass_kg",
            "area_m2",
            "thickness_mm",
            "areal_density_kg_m2",
            "notes",
        ])
        for p in panels:
            w.writerow([
                p.coupon_id,
                p.config,
                p.group,
                p.mass_kg,
                p.area_m2,
                p.thickness_mm,
                p.areal_density_kg_m2,
                p.notes,
            ])


def main() -> int:
    ap = argparse.ArgumentParser(description="Compute AHIS normalization metrics from a panel metadata CSV.")
    ap.add_argument("--input", required=True, help="Path to panel metadata CSV (processed).")
    ap.add_argument("--output", required=True, help="Path to write normalized metrics CSV.")

    args = ap.parse_args()
    rows = _read_panel_rows(args.input)
    panels = _to_panel_metrics(args.input, rows)
    _write_normalized_csv(args.output, panels)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
