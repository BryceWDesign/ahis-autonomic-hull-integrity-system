"""Bounded modal-response planner for PVDF/piezo actuation.

The controller uses identified structural modes. No fixed 3/6/9-Hz numerology is used.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True, slots=True)
class ModalTarget:
    frequency_hz: float
    baseline_damping_ratio: float
    target_damping_ratio: float
    modal_weight: float = 1.0


@dataclass(frozen=True, slots=True)
class ModalPlan:
    frequency_hz: float
    requested_delta_zeta: float
    commanded_delta_zeta: float
    authority_utilization: float
    predicted_resonant_transmissibility_before: float
    predicted_resonant_transmissibility_after: float
    saturated: bool


def resonant_transmissibility(zeta: float) -> float:
    if not 0 < zeta < 1:
        raise ValueError("zeta must lie in (0,1)")
    # Base-excited SDOF transmissibility at r=1.
    return sqrt(1.0 + (2.0 * zeta) ** 2) / (2.0 * zeta)


def plan_modal_damping(target: ModalTarget, *, max_delta_zeta: float) -> ModalPlan:
    if target.frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    if target.modal_weight <= 0:
        raise ValueError("modal_weight must be positive")
    if max_delta_zeta <= 0:
        raise ValueError("max_delta_zeta must be positive")
    if not 0 < target.baseline_damping_ratio < 1:
        raise ValueError("baseline damping ratio must lie in (0,1)")
    if not target.baseline_damping_ratio < target.target_damping_ratio < 1:
        raise ValueError("target damping must exceed baseline and remain below 1")

    requested = target.target_damping_ratio - target.baseline_damping_ratio
    commanded = min(requested, max_delta_zeta)
    before = resonant_transmissibility(target.baseline_damping_ratio)
    after = resonant_transmissibility(target.baseline_damping_ratio + commanded)
    return ModalPlan(
        frequency_hz=target.frequency_hz,
        requested_delta_zeta=requested,
        commanded_delta_zeta=commanded,
        authority_utilization=commanded / max_delta_zeta,
        predicted_resonant_transmissibility_before=before,
        predicted_resonant_transmissibility_after=after,
        saturated=commanded < requested,
    )
