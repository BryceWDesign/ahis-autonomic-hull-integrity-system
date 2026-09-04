"""Uncertainty-aware anisotropic time-of-arrival localization."""
from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, hypot, pi, sqrt
from statistics import median


@dataclass(frozen=True, slots=True)
class ArrivalObservation:
    sensor_id: str
    x_m: float
    y_m: float
    arrival_s: float
    quality: float = 1.0

    def __post_init__(self) -> None:
        if not self.sensor_id.strip() or self.arrival_s < 0:
            raise ValueError("invalid arrival observation")
        if not 0 <= self.quality <= 1:
            raise ValueError("quality must be in [0,1]")


@dataclass(frozen=True, slots=True)
class AnisotropicPropagation:
    base_speed_m_s: float
    anisotropy_fraction: float = 0.0
    principal_axis_deg: float = 0.0

    def __post_init__(self) -> None:
        if self.base_speed_m_s <= 0:
            raise ValueError("base_speed_m_s must be positive")
        if not 0 <= self.anisotropy_fraction < 0.8:
            raise ValueError("anisotropy_fraction must be in [0,0.8)")

    def speed(self, dx: float, dy: float) -> float:
        theta = atan2(dy, dx)
        axis = self.principal_axis_deg * pi / 180.0
        return self.base_speed_m_s * (1.0 + self.anisotropy_fraction * cos(2.0 * (theta - axis)))


@dataclass(frozen=True, slots=True)
class LocalizationResult:
    accepted: bool
    x_m: float | None
    y_m: float | None
    event_time_s: float | None
    weighted_rms_s: float | None
    confidence_radius_m: float | None
    effective_sensor_weight: float
    reason: str


def localize_anisotropic(
    observations: list[ArrivalObservation],
    *,
    model: AnisotropicPropagation,
    bounds_m: tuple[float, float, float, float],
    grid_points_per_axis: int = 61,
    max_weighted_rms_s: float = 8e-5,
    min_effective_weight: float = 3.0,
) -> LocalizationResult:
    xmin, xmax, ymin, ymax = bounds_m
    if not xmin < xmax or not ymin < ymax:
        raise ValueError("invalid bounds")
    if grid_points_per_axis < 9:
        raise ValueError("grid_points_per_axis must be >= 9")
    usable = [o for o in observations if o.quality > 0]
    total_w = sum(o.quality for o in usable)
    if total_w < min_effective_weight:
        return LocalizationResult(False, None, None, None, None, None, total_w, "insufficient sensor quality")

    candidates: list[tuple[float, float, float, float]] = []
    for ix in range(grid_points_per_axis):
        x = xmin + (xmax - xmin) * ix / (grid_points_per_axis - 1)
        for iy in range(grid_points_per_axis):
            y = ymin + (ymax - ymin) * iy / (grid_points_per_axis - 1)
            inferred = []
            for o in usable:
                dx, dy = x - o.x_m, y - o.y_m
                inferred.append(o.arrival_s - hypot(dx, dy) / model.speed(dx, dy))
            t0 = median(inferred)
            weighted_sq = 0.0
            for o in usable:
                dx, dy = x - o.x_m, y - o.y_m
                pred = t0 + hypot(dx, dy) / model.speed(dx, dy)
                weighted_sq += o.quality * (o.arrival_s - pred) ** 2
            rms = sqrt(weighted_sq / total_w)
            candidates.append((rms, x, y, t0))
    candidates.sort()
    rms, x, y, t0 = candidates[0]
    if rms > max_weighted_rms_s:
        return LocalizationResult(False, None, None, None, rms, None, total_w, "residual exceeds calibrated bound")

    # Near-optimal set defines an explicit grid-level uncertainty region.  The 1.5x
    # residual envelope is deterministic and must be calibrated on real panels before
    # operational use.
    threshold = max(rms * 1.5, rms + 1e-12)
    near = [(cx, cy) for cr, cx, cy, _ in candidates if cr <= threshold]
    radius = max((hypot(cx - x, cy - y) for cx, cy in near), default=0.0)
    return LocalizationResult(True, x, y, t0, rms, radius, total_w, "accepted anisotropic grid solution")
