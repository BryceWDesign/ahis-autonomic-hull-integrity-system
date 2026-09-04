"""Small auditable digital-twin discrepancy screen."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TwinBaseline:
    modal_hz: tuple[float, ...]
    static_strain_microstrain: float
    leak_ml_min: float


@dataclass(frozen=True, slots=True)
class TwinObservation:
    modal_hz: tuple[float, ...]
    static_strain_microstrain: float
    leak_ml_min: float


@dataclass(frozen=True, slots=True)
class TwinTolerance:
    modal_fraction: float = 0.03
    strain_fraction: float = 0.08
    leak_absolute_ml_min: float = 2.0


@dataclass(frozen=True, slots=True)
class TwinAssessment:
    accepted: bool
    modal_max_fraction_error: float
    strain_fraction_error: float
    leak_absolute_error_ml_min: float
    failed_channels: tuple[str, ...]


def assess_twin(baseline: TwinBaseline, observation: TwinObservation, tolerance: TwinTolerance = TwinTolerance()) -> TwinAssessment:
    if len(baseline.modal_hz) != len(observation.modal_hz) or not baseline.modal_hz:
        raise ValueError("modal vectors must be non-empty and equal length")
    modal_errors = [abs(o - b) / max(abs(b), 1e-12) for b, o in zip(baseline.modal_hz, observation.modal_hz)]
    strain_error = abs(observation.static_strain_microstrain - baseline.static_strain_microstrain) / max(abs(baseline.static_strain_microstrain), 1e-12)
    leak_error = abs(observation.leak_ml_min - baseline.leak_ml_min)
    failed: list[str] = []
    if max(modal_errors) > tolerance.modal_fraction:
        failed.append("modal")
    if strain_error > tolerance.strain_fraction:
        failed.append("strain")
    if leak_error > tolerance.leak_absolute_ml_min:
        failed.append("leak")
    return TwinAssessment(not failed, max(modal_errors), strain_error, leak_error, tuple(failed))
