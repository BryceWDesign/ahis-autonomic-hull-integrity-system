"""Uncertainty-bounded fatigue screening.

This is a relative maintenance/prognostic screen, not a certified life prediction.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FatigueState:
    cumulative_damage: float
    mean_damage_per_cycle: float
    relative_uncertainty: float

    def __post_init__(self) -> None:
        if self.cumulative_damage < 0 or self.mean_damage_per_cycle <= 0:
            raise ValueError("invalid fatigue state")
        if not 0 <= self.relative_uncertainty < 1:
            raise ValueError("relative_uncertainty must be in [0,1)")


@dataclass(frozen=True, slots=True)
class RULScreen:
    lower_cycles: int
    nominal_cycles: int
    upper_cycles: int
    status: str


def screen_remaining_cycles(state: FatigueState, *, damage_limit: float = 1.0) -> RULScreen:
    if damage_limit <= 0:
        raise ValueError("damage_limit must be positive")
    remaining = max(0.0, damage_limit - state.cumulative_damage)
    nominal = remaining / state.mean_damage_per_cycle
    high_rate = state.mean_damage_per_cycle * (1.0 + state.relative_uncertainty)
    low_rate = state.mean_damage_per_cycle * (1.0 - state.relative_uncertainty)
    lower = remaining / high_rate
    upper = remaining / max(low_rate, 1e-15)
    status = "EXHAUSTED" if remaining <= 0 else "SCREEN_ONLY_UNCERTIFIED"
    return RULScreen(int(lower), int(nominal), int(upper), status)
