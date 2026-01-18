#!/usr/bin/env python3
"""
AHIS PoC Analysis — Delta Report Generator (One-Page Engineering Summary)

Purpose
-------
Generate a concise, engineer-readable delta summary from:
1) impact peak group stats (baseline vs ahis) from impact_peak_metrics.py
2) normalized panel metrics (kg/m^2, thickness mm) from normalization_utils.py
3) optional leak onset/leak rate summaries from leak_rate_metrics.py

This script produces:
- processed/DELTA_REPORT.md  (one-page Markdown summary)
- processed/delta_report_values.csv (machine-readable key values)

Strictness / No Guessing
------------------------
- You must provide explicit paths to inputs.
- Group names must be explicitly provided (default expected: "baseline" and "ahis").
- If required files are missing or groups are absent, the script errors out.

Inputs
------
A) Impact grouped stats CSV (required for impact portion):
   impact_peak_group_stats.csv with columns:
   group,metric,n,mean_peak_abs,std_peak_abs_sample

B) Normalized panel metrics CSV (required for mass/thickness normalization):
   normalized_panel_metrics.csv with columns:
   coupon_id,config,group,mass_kg,area_m2,thickness_mm,areal_density_kg_m2,notes

C) Leak summaries (optional):
   leak_onset_summary.csv and leak_rate_summary.csv

Usage Example
-------------
python3 delta_report_generator.py \
  --impact-stats results/T-IMP-010/RUN_x/processed/impact_peak_group_stats.csv \
  --panel-metrics results/T-IMP-010/RUN_x/processed/normalized_panel_metrics.csv \
  --out-dir results/T-IMP-010/RUN_x/processed \
  --baseline-group baseline \
  --ahis-group ahis

Optional leak inputs:
  --leak-onset results/T-PRS-050/RUN_y/processed/leak_onset_summary.csv \
  --leak-rate  results/T-PRS-050/RUN_y/processed/leak_rate_summary.csv
"""

from __future__ import annotations

import argparse
import csv
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ImpactGroupStat:
    group: str
    metric: str
    n: int
    mean_peak_abs: float
    std_peak_abs_sample: float


@dataclass(frozen=True)
class PanelGroupAgg:
    group: str
    n: int
    mean_areal_density_kg_m2: float
    mean_thickness_mm: float


def _read_csv(path: str) -> Tuple[List[str], List[Dict[str, str]]]:
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header row: {path}")
        rows = list(reader)
        if not rows:
            raise ValueError(f"No data rows in {path}")
        return reader.fieldnames, rows


def _parse_float(value: str, *, path: str, col: str, row_idx: int) -> float:
    try:
        return float(value)
    except Exception as e:
        raise ValueError(
            f"Non-numeric value in {path} at row {row_idx+2} col '{col}': {value!r}"
        ) from e


def _parse_int(value: str, *, path: str, col: str, row_idx: int) -> int:
    try:
        return int(value)
    except Exception as e:
        raise ValueError(
            f"Non-integer value in {path} at row {row_idx+2} col '{col}': {value!r}"
        ) from e


def _load_impact_stats(path: str) -> List[ImpactGroupStat]:
    headers, rows = _read_csv(path)
    required = {"group", "metric", "n", "mean_peak_abs", "std_peak_abs_sample"}
    missing = required - set(headers)
    if missing:
        raise ValueError(f"Missing required columns in {path}: {sorted(missing)}")

    out: List[ImpactGroupStat] = []
    for i, r in enumerate(rows):
        out.append(
            ImpactGroupStat(
                group=(r["group"] or "").strip(),
                metric=(r["metric"] or "").strip(),
                n=_parse_int(r["n"], path=path, col="n", row_idx=i),
                mean_peak_abs=_parse_float(r["mean_peak_abs"], path=path, col="mean_peak_abs", row_idx=i),
                std_peak_abs_sample=_parse_float(r["std_peak_abs_sample"], path=path, col="std_peak_abs_sample", row_idx=i),
            )
        )
    return out


def _mean(xs: List[float]) -> float:
    if not xs:
        raise ValueError("Cannot compute mean of empty list")
    return sum(xs) / float(len(xs))


def _load_panel_metrics(path: str) -> Dict[str, PanelGroupAgg]:
    headers, rows = _read_csv(path)
    required = {"group", "areal_density_kg_m2", "thickness_mm"}
    missing = required - set(headers)
    if missing:
        raise ValueError(f"Missing required columns in {path}: {sorted(missing)}")

    by_group: Dict[str, Dict[str, List[float]]] = {}
    for i, r in enumerate(rows):
        grp = (r.get("group") or "").strip()
        if not grp:
            raise ValueError(f"Empty group in {path} at row {i+2}")
        ad = _parse_float(r["areal_density_kg_m2"], path=path, col="areal_density_kg_m2", row_idx=i)
        th = _parse_float(r["thickness_mm"], path=path, col="thickness_mm", row_idx=i)
        if ad <= 0:
            raise ValueError(f"areal_density_kg_m2 must be > 0 in {path} row {i+2}")
        if th <= 0:
            raise ValueError(f"thickness_mm must be > 0 in {path} row {i+2}")

        by_group.setdefault(grp, {"ad": [], "th": []})
        by_group[grp]["ad"].append(ad)
        by_group[grp]["th"].append(th)

    aggs: Dict[str, PanelGroupAgg] = {}
    for grp, vals in by_group.items():
        aggs[grp] = PanelGroupAgg(
            group=grp,
            n=len(vals["ad"]),
            mean_areal_density_kg_m2=_mean(vals["ad"]),
            mean_thickness_mm=_mean(vals["th"]),
        )
    return aggs


def _find_stat(stats: List[ImpactGroupStat], group: str, metric: str) -> ImpactGroupStat:
    matches = [s for s in stats if s.group == group and s.metric == metric]
    if not matches:
        raise ValueError(f"Missing impact stats for group='{group}' metric='{metric}'.")
    if len(matches) > 1:
        raise ValueError(f"Duplicate impact stats rows for group='{group}' metric='{metric}'.")
    return matches[0]


def _load_optional_single_row(path: str, required_cols: List[str]) -> Dict[str, str]:
    headers, rows = _read_csv(path)
    missing = set(required_cols) - set(headers)
    if missing:
        raise ValueError(f"Missing required columns in {path}: {sorted(missing)}")
    if len(rows) != 1:
        raise ValueError(f"Expected exactly 1 data row in {path}, found {len(rows)}")
    return rows[0]


def _write_csv_kv(out_path: str, kv: List[Tuple[str, str]]) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["key", "value"])
        for k, v in kv:
            w.writerow([k, v])


def _write_md(out_path: str, text: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate AHIS one-page delta report from processed PoC metrics.")
    ap.add_argument("--impact-stats", required=True, help="Path to impact_peak_group_stats.csv (processed).")
    ap.add_argument("--panel-metrics", required=True, help="Path to normalized_panel_metrics.csv (processed).")
    ap.add_argument("--out-dir", required=True, help="Directory to write DELTA_REPORT.md and CSV values.")
    ap.add_argument("--baseline-group", default="baseline", help="Group label for baseline. Default: baseline")
    ap.add_argument("--ahis-group", default="ahis", help="Group label for AHIS. Default: ahis")
    ap.add_argument(
        "--impact-metric",
        action="append",
        required=True,
        help="Metric name from impact stats to include (e.g., strain_ue, accel_g). Can be repeated.",
    )
    ap.add_argument("--leak-onset", default=None, help="Optional path to leak_onset_summary.csv (processed).")
    ap.add_argument("--leak-rate", default=None, help="Optional path to leak_rate_summary.csv (processed).")

    args = ap.parse_args()

    stats = _load_impact_stats(args.impact_stats)
    panel_aggs = _load_panel_metrics(args.panel_metrics)

    if args.baseline_group not in panel_aggs:
        raise ValueError(f"Baseline group '{args.baseline_group}' not found in panel metrics.")
    if args.ahis_group not in panel_aggs:
        raise ValueError(f"AHIS group '{args.ahis_group}' not found in panel metrics.")

    base_panel = panel_aggs[args.baseline_group]
    ahis_panel = panel_aggs[args.ahis_group]

    lines: List[str] = []
    kv: List[Tuple[str, str]] = []

    lines.append("# AHIS — Delta Report (PoC)\n")
    lines.append("**Status:** Proof-of-Concept summary generated from processed datasets. Not flight-qualified. Not crew-rated.\n")

    # Mass/thickness summary
    lines.append("## Panel Normalization (Measured)\n")
    lines.append(f"- Baseline group: n={base_panel.n}, mean areal density={base_panel.mean_areal_density_kg_m2:.6g} kg/m², mean thickness={base_panel.mean_thickness_mm:.6g} mm\n")
    lines.append(f"- AHIS group: n={ahis_panel.n}, mean areal density={ahis_panel.mean_areal_density_kg_m2:.6g} kg/m², mean thickness={ahis_panel.mean_thickness_mm:.6g} mm\n")

    kv.extend([
        ("baseline_mean_areal_density_kg_m2", f"{base_panel.mean_areal_density_kg_m2}"),
        ("baseline_mean_thickness_mm", f"{base_panel.mean_thickness_mm}"),
        ("ahis_mean_areal_density_kg_m2", f"{ahis_panel.mean_areal_density_kg_m2}"),
        ("ahis_mean_thickness_mm", f"{ahis_panel.mean_thickness_mm}"),
    ])

    # Impact deltas
    lines.append("\n## Impact Peaks (Magnitude) — Baseline vs AHIS\n")
    for metric in args.impact_metric:
        b = _find_stat(stats, args.baseline_group, metric)
        a = _find_stat(stats, args.ahis_group, metric)

        delta = a.mean_peak_abs - b.mean_peak_abs
        # Normalize by AHIS mean areal density and thickness (explicit choice; reviewer can change).
        delta_per_kgm2 = delta / ahis_panel.mean_areal_density_kg_m2
        delta_per_mm = delta / ahis_panel.mean_thickness_mm

        lines.append(f"### Metric: `{metric}`\n")
        lines.append(f"- Baseline: n={b.n}, mean|peak|={b.mean_peak_abs:.6g}, std={b.std_peak_abs_sample:.6g}\n")
        lines.append(f"- AHIS: n={a.n}, mean|peak|={a.mean_peak_abs:.6g}, std={a.std_peak_abs_sample:.6g}\n")
        lines.append(f"- Δ(mean|peak|) = {delta:.6g} (AHIS − Baseline)\n")
        lines.append(f"- Normalized Δ per AHIS areal density = {delta_per_kgm2:.6g} / (kg/m²)\n")
        lines.append(f"- Normalized Δ per AHIS thickness = {delta_per_mm:.6g} / mm\n")

        kv.extend([
            (f"{metric}_baseline_mean_abs_peak", f"{b.mean_peak_abs}"),
            (f"{metric}_ahis_mean_abs_peak", f"{a.mean_peak_abs}"),
            (f"{metric}_delta_mean_abs_peak", f"{delta}"),
            (f"{metric}_delta_per_ahis_areal_density", f"{delta_per_kgm2}"),
            (f"{metric}_delta_per_ahis_thickness_mm", f"{delta_per_mm}"),
        ])

    # Optional leak section
    if args.leak_onset or args.leak_rate:
        lines.append("\n## Pressure/Leak (Optional Inputs)\n")
        if args.leak_onset:
            onset = _load_optional_single_row(args.leak_onset, ["onset_index", "onset_time_s", "rate_threshold_pos_per_s", "window_seconds"])
            lines.append(f"- Leak onset time (s): {onset['onset_time_s']} (threshold={onset['rate_threshold_pos_per_s']} per s, window={onset['window_seconds']} s)\n")
            kv.extend([
                ("leak_onset_time_s", onset["onset_time_s"]),
                ("leak_onset_rate_threshold_pos_per_s", onset["rate_threshold_pos_per_s"]),
                ("leak_onset_window_seconds", onset["window_seconds"]),
            ])
        if args.leak_rate:
            lr = _load_optional_single_row(args.leak_rate, ["window_start_time_s", "window_end_time_s", "n_samples", "mean_dp_dt_per_s", "median_dp_dt_per_s"])
            lines.append(f"- Mean dP/dt over onset window: {lr['mean_dp_dt_per_s']} per s\n")
            lines.append(f"- Median dP/dt over onset window: {lr['median_dp_dt_per_s']} per s\n")
            kv.extend([
                ("leak_mean_dp_dt_per_s", lr["mean_dp_dt_per_s"]),
                ("leak_median_dp_dt_per_s", lr["median_dp_dt_per_s"]),
            ])

    # Closing discipline
    lines.append("\n## Interpretation Discipline\n")
    lines.append("- This report summarizes processed datasets only; it does not certify safety or mission readiness.\n")
    lines.append("- Any confounders (fixture changes, temperature drift, insufficient repeats) must be stated in the run package README.\n")

    out_dir = args.out_dir
    _write_md(os.path.join(out_dir, "DELTA_REPORT.md"), "".join(lines))
    _write_csv_kv(os.path.join(out_dir, "delta_report_values.csv"), kv)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
