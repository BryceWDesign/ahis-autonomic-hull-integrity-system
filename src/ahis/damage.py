"""Damage-event fusion and bounded time-of-arrival localization.

This module is intentionally model-level. It does not claim that a particular hull,
sensor spacing, or wave speed is qualified. It provides deterministic algorithms that
can be exercised against synthetic data now and replaced with calibrated parameters
from coupon/panel testing later.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import hypot, sqrt
from statistics import median
from typing import Iterable


@dataclass(frozen=True, slots=True)
class SensorReading:
    sensor_id: str
    x_m: float
    y_m: float
    arrival_s: float
    amplitude: float
    healthy: bool = True


@dataclass(frozen=True, slots=True)
class DamageEstimate:
    detected: bool
    x_m: float | None
    y_m: float | None
    event_time_s: float | None
    residual_rms_s: float | None
    healthy_sensor_count: int
    confidence: float
    reason: str


def _validate(readings: list[SensorReading], wave_speed_m_s: float) -> None:
    if wave_speed_m_s <= 0:
        raise ValueError("wave_speed_m_s must be positive")
    ids = [r.sensor_id for r in readings]
    if len(ids) != len(set(ids)):
        raise ValueError("sensor ids must be unique")
    if any(r.arrival_s < 0 for r in readings):
        raise ValueError("arrival times must be non-negative")
    if any(r.amplitude < 0 for r in readings):
        raise ValueError("amplitudes must be non-negative magnitudes")


def localize_event(
    readings: Iterable[SensorReading],
    *,
    wave_speed_m_s: float,
    panel_bounds_m: tuple[float, float, float, float],
    amplitude_threshold: float,
    min_sensors: int = 4,
    grid_points_per_axis: int = 61,
    max_residual_s: float = 6.0e-5,
) -> DamageEstimate:
    """Fuse healthy sensor arrivals and localize with a bounded grid search.

    For each candidate (x,y), the unknown source time is estimated as the median of
    t_i - distance_i / c. The candidate minimizing arrival-time residual RMS wins.
    This is deliberately simple and auditable. A real deployment must replace the
    scalar wave speed with a calibrated anisotropic/dispersive propagation model.
    """
    rows = list(readings)
    _validate(rows, wave_speed_m_s)
    xmin, xmax, ymin, ymax = panel_bounds_m
    if not (xmin < xmax and ymin < ymax):
        raise ValueError("invalid panel bounds")
    if amplitude_threshold < 0:
        raise ValueError("amplitude_threshold must be non-negative")
    if min_sensors < 3:
        raise ValueError("min_sensors must be >= 3")
    if grid_points_per_axis < 5:
        raise ValueError("grid_points_per_axis must be >= 5")

    active = [r for r in rows if r.healthy and r.amplitude >= amplitude_threshold]
    if len(active) < min_sensors:
        return DamageEstimate(
            detected=False,
            x_m=None,
            y_m=None,
            event_time_s=None,
            residual_rms_s=None,
            healthy_sensor_count=len(active),
            confidence=0.0,
            reason="insufficient healthy above-threshold sensor quorum",
        )

    best: tuple[float, float, float, float] | None = None
    nx = grid_points_per_axis
    ny = grid_points_per_axis
    for ix in range(nx):
        x = xmin + (xmax - xmin) * ix / (nx - 1)
        for iy in range(ny):
            y = ymin + (ymax - ymin) * iy / (ny - 1)
            inferred_t0 = [
                r.arrival_s - hypot(x - r.x_m, y - r.y_m) / wave_speed_m_s for r in active
            ]
            t0 = median(inferred_t0)
            residuals = [
                r.arrival_s - (t0 + hypot(x - r.x_m, y - r.y_m) / wave_speed_m_s)
                for r in active
            ]
            rms = sqrt(sum(v * v for v in residuals) / len(residuals))
            candidate = (rms, x, y, t0)
            if best is None or candidate < best:
                best = candidate

    assert best is not None
    rms, x, y, t0 = best
    geometry_span = max(xmax - xmin, ymax - ymin)
    if geometry_span <= 0:
        geometry_span = 1.0
    residual_score = max(0.0, 1.0 - rms / max(max_residual_s, 1.0e-15))
    quorum_score = min(1.0, len(active) / max(float(min_sensors + 2), 1.0))
    confidence = max(0.0, min(1.0, 0.75 * residual_score + 0.25 * quorum_score))
    detected = rms <= max_residual_s
    return DamageEstimate(
        detected=detected,
        x_m=x if detected else None,
        y_m=y if detected else None,
        event_time_s=t0 if detected else None,
        residual_rms_s=rms,
        healthy_sensor_count=len(active),
        confidence=confidence if detected else 0.0,
        reason=(
            "localized by bounded time-of-arrival fusion"
            if detected
            else "arrival-time residual exceeds calibrated acceptance bound"
        ),
    )
