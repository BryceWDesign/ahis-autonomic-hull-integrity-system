#!/usr/bin/env python3
"""
AHIS PoC Analysis — Leak Rate Metrics (T-PRS-050)

Purpose
-------
Compute leak-rate metrics from a pressure vs time log (CSV) and determine leak onset
based on an explicit, user-defined rule. This script does not guess units.

Supported leak onset definitions (choose one):
1) Decay-rate threshold: leak onset occurs when dP/dt <= -RATE_THRESHOLD
   for at least WINDOW_SECONDS continuously.

You must supply:
- time column name (seconds) and pressure column name (Pa or any consistent unit)
- RATE_THRESHOLD (in pressure-units per second)
- WINDOW_SECONDS (seconds)

Outputs
-------
- processed/leak_rate_timeseries.csv  (time, pressure, dp_dt)
- processed/leak_onset_summary.csv    (onset_time_s, onset_index, rate_threshold, window_seconds)
- processed/leak_rate_summary.csv     (mean_dp_dt_over_window, median_dp_dt_over_window, etc.)

Notes
-----
- If your time base is not seconds, convert before using this script.
- If your pressure is not Pascals, that's fine — but thresholds must match your units.
- This script is strict about monotonic time and numeric parsing.

Usage Example
-------------
python3 leak_rate_metrics.py \
  --input results/T-PRS-050/RUN_YYYY-MM-DD_XYZ/raw/pressure_log.csv \
  --output results/T-PRS-050/RUN_YYYY-MM-DD_XYZ/processed \
  --time-col time_s \
  --pressure-col pressure_pa \
  --rate-threshold 5.0 \
  --window-seconds 2.0

Interpretation: leak onset when pressure decay rate <= -5 Pa/s for >= 2 seconds.
"""

from __future__ import annotations

import argparse
import csv
import os
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class SeriesPoint:
    t: float
    p: float


def _parse_float(value: str, *, path: str, col: str, row_idx: int) -> float:
    try:
        return float(value)
    except Exception as e:
        raise ValueError(
            f"Non-numeric value in {path} at row {row_idx+2} col '{col}': {value!r}"
        ) from e


def _read_pressure_series(path: str, time_col: str, pressure_col: str) -> List[SeriesPoint]:
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header row: {path}")
        headers = reader.fieldnames
        if time_col not in headers:
            raise ValueError(f"Missing time column '{time_col}' in {path}. Found: {headers}")
        if pressure_col not in headers:
            raise ValueError(f"Missing pressure column '{pressure_col}' in {path}. Found: {headers}")

        points: List[SeriesPoint] = []
        for i, row in enumerate(reader):
            t = _parse_float(row[time_col], path=path, col=time_col, row_idx=i)
            p = _parse_float(row[pressure_col], path=path, col=pressure_col, row_idx=i)
            points.append(SeriesPoint(t=t, p=p))

    if len(points) < 3:
        raise ValueError(f"Need at least 3 rows to compute derivatives: {path}")

    # Strict monotonic time check
    for i in range(1, len(points)):
        if points[i].t <= points[i - 1].t:
            raise ValueError(
                f"Time column must be strictly increasing. "
                f"Found non-increasing at index {i} (t={points[i].t} <= {points[i-1].t}) in {path}"
            )
    return points


def _compute_dp_dt(points: List[SeriesPoint]) -> List[float]:
    """
    Compute dp/dt using central differences for interior points,
    forward/backward for endpoints. Returns list aligned with points.
    """
    n = len(points)
    dpdt = [0.0] * n

    # forward difference at 0
    dt0 = points[1].t - points[0].t
    dpdt[0] = (points[1].p - points[0].p) / dt0

    # central differences
    for i in range(1, n - 1):
        dt = points[i + 1].t - points[i - 1].t
        dpdt[i] = (points[i + 1].p - points[i - 1].p) / dt

    # backward difference at n-1
    dtn = points[n - 1].t - points[n - 2].t
    dpdt[n - 1] = (points[n - 1].p - points[n - 2].p) / dtn

    return dpdt


def _find_onset_index_by_rate_window(
    points: List[SeriesPoint],
    dpdt: List[float],
    rate_threshold_pos: float,
    window_seconds: float,
) -> int:
    """
    Leak onset definition:
    Find the earliest index i such that dp/dt <= -rate_threshold_pos for a continuous
    time span >= window_seconds starting at i (using sample times).

    rate_threshold_pos is a positive number in pressure-units per second.
    """
    if rate_threshold_pos <= 0:
        raise ValueError("--rate-threshold must be positive (it is applied as a negative decay threshold).")
    if window_seconds <= 0:
        raise ValueError("--window-seconds must be positive.")

    n = len(points)
    i = 0
    while i < n:
        if dpdt[i] <= -rate_threshold_pos:
            start_t = points[i].t
            j = i
            # advance while condition holds
            while j < n and dpdt[j] <= -rate_threshold_pos:
                if points[j].t - start_t >= window_seconds:
                    return i
                j += 1
            # jump i to j to avoid O(n^2) on long failing segments
            i = j
        else:
            i += 1

    raise ValueError(
        "No leak onset found using the provided threshold/window. "
        "Adjust --rate-threshold and/or --window-seconds or verify units."
    )


def _mean(xs: List[float]) -> float:
    if not xs:
        raise ValueError("Cannot compute mean of empty list")
    return sum(xs) / float(len(xs))


def _median(xs: List[float]) -> float:
    if not xs:
        raise ValueError("Cannot compute median of empty list")
    ys = sorted(xs)
    n = len(ys)
    mid = n // 2
    if n % 2 == 1:
        return ys[mid]
    return 0.5 * (ys[mid - 1] + ys[mid])


def _write_timeseries(out_path: str, points: List[SeriesPoint], dpdt: List[float]) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["time_s", "pressure", "dp_dt_per_s"])
        for pt, d in zip(points, dpdt):
            w.writerow([pt.t, pt.p, d])


def _write_onset_summary(out_path: str, onset_idx: int, points: List[SeriesPoint], rate_thr: float, window_s: float) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["onset_index", "onset_time_s", "rate_threshold_pos_per_s", "window_seconds"])
        w.writerow([onset_idx, points[onset_idx].t, rate_thr, window_s])


def _write_leak_rate_summary(out_path: str, onset_idx: int, points: List[SeriesPoint], dpdt: List[float], window_s: float) -> None:
    """
    Summarize leak behavior over the onset window (from onset_idx until onset_idx+window_s).
    """
    start_t = points[onset_idx].t
    end_t = start_t + window_s

    window_vals: List[float] = []
    for pt, d in zip(points[onset_idx:], dpdt[onset_idx:]):
        if pt.t <= end_t:
            window_vals.append(d)
        else:
            break

    if not window_vals:
        raise ValueError("Internal error: onset window contained no samples.")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["window_start_time_s", "window_end_time_s", "n_samples", "mean_dp_dt_per_s", "median_dp_dt_per_s"])
        w.writerow([start_t, end_t, len(window_vals), _mean(window_vals), _median(window_vals)])


def main() -> int:
    ap = argparse.ArgumentParser(description="Compute AHIS T-PRS-050 leak rate metrics from pressure log CSV.")
    ap.add_argument("--input", required=True, help="Path to pressure log CSV (raw).")
    ap.add_argument("--output", required=True, help="Directory where processed outputs will be written.")
    ap.add_argument("--time-col", default="time_s", help="Name of the time column (seconds). Default: time_s")
    ap.add_argument("--pressure-col", default="pressure_pa", help="Name of the pressure column. Default: pressure_pa")
    ap.add_argument(
        "--rate-threshold",
        required=True,
        type=float,
        help="Positive decay-rate threshold (pressure-units per second). Leak onset when dp/dt <= -threshold.",
    )
    ap.add_argument(
        "--window-seconds",
        required=True,
        type=float,
        help="Continuous duration (seconds) that dp/dt must stay below -threshold to declare onset.",
    )

    args = ap.parse_args()

    points = _read_pressure_series(args.input, time_col=args.time_col, pressure_col=args.pressure_col)
    dpdt = _compute_dp_dt(points)

    onset_idx = _find_onset_index_by_rate_window(
        points=points,
        dpdt=dpdt,
        rate_threshold_pos=args.rate_threshold,
        window_seconds=args.window_seconds,
    )

    out_dir = args.output
    _write_timeseries(os.path.join(out_dir, "leak_rate_timeseries.csv"), points, dpdt)
    _write_onset_summary(os.path.join(out_dir, "leak_onset_summary.csv"), onset_idx, points, args.rate_threshold, args.window_seconds)
    _write_leak_rate_summary(os.path.join(out_dir, "leak_rate_summary.csv"), onset_idx, points, dpdt, args.window_seconds)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
