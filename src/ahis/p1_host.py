"""Host-side physical-run utilities for the AHIS-P1 bench article.

This module contains only deterministic calculations and protocol orchestration helpers.
It never fabricates physical evidence; callers must supply live device measurements.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Iterable


@dataclass(frozen=True, slots=True)
class MassSample:
    elapsed_s: float
    mass_g: float


@dataclass(frozen=True, slots=True)
class LeakEstimate:
    leak_ml_min: float
    slope_g_s: float
    r_squared: float
    sample_count: int


def estimate_leak_rate(samples: Iterable[MassSample], *, water_density_g_ml: float) -> LeakEstimate:
    pts = list(samples)
    if len(pts) < 5:
        raise ValueError("at least five mass samples are required")
    if water_density_g_ml <= 0:
        raise ValueError("water density must be positive")
    xs = [p.elapsed_s for p in pts]
    ys = [p.mass_g for p in pts]
    if any(not math.isfinite(v) for v in xs + ys):
        raise ValueError("samples must be finite")
    if any(b <= a for a, b in zip(xs, xs[1:])):
        raise ValueError("sample times must be strictly increasing")
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    denom = sum((x - xbar) ** 2 for x in xs)
    if denom <= 0:
        raise ValueError("sample times must span a nonzero interval")
    slope = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / denom
    intercept = ybar - slope * xbar
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - ybar) ** 2 for y in ys)
    r2 = 1.0 if ss_tot == 0 and ss_res == 0 else (0.0 if ss_tot == 0 else 1.0 - ss_res / ss_tot)
    leak = max(0.0, slope) * 60.0 / water_density_g_ml
    return LeakEstimate(leak, slope, r2, len(pts))


def paired_runtime_ms(*, target_a_ml: float, target_b_ml: float, pump_a_ml_s: float, pump_b_ml_s: float, hard_limit_ms: int = 30_000) -> tuple[int, int]:
    values = (target_a_ml, target_b_ml, pump_a_ml_s, pump_b_ml_s)
    if any(not math.isfinite(v) or v <= 0 for v in values):
        raise ValueError("targets and calibrated rates must be finite and positive")
    if hard_limit_ms <= 0:
        raise ValueError("hard_limit_ms must be positive")
    a = math.ceil(target_a_ml / pump_a_ml_s * 1000.0)
    b = math.ceil(target_b_ml / pump_b_ml_s * 1000.0)
    if a > hard_limit_ms or b > hard_limit_ms:
        raise ValueError("calibrated runtime exceeds firmware hard limit")
    return a, b


def calibration_bundle_sha256(sensor_calibration_sha256: str, pump_calibration_sha256: str) -> str:
    for value in (sensor_calibration_sha256, pump_calibration_sha256):
        if len(value) != 64 or any(c not in "0123456789abcdef" for c in value.lower()):
            raise ValueError("calibration digests must be 64-character hexadecimal SHA-256 values")
    payload = {
        "pump_calibration_sha256": pump_calibration_sha256.lower(),
        "sensor_calibration_sha256": sensor_calibration_sha256.lower(),
    }
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
