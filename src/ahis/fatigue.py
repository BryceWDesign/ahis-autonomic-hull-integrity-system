"""Cumulative-damage screening utilities.

These functions encode standard engineering screening relationships, but require
material/test parameters as inputs. AHIS does not ship universal fatigue constants.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SNBlock:
    cycles_applied: float
    cycles_to_failure: float


@dataclass(frozen=True, slots=True)
class FatigueState:
    miner_damage_fraction: float
    screen_exceeded: bool


def miners_rule(blocks: list[SNBlock], *, prior_damage_fraction: float = 0.0) -> FatigueState:
    if not 0.0 <= prior_damage_fraction:
        raise ValueError("prior_damage_fraction must be non-negative")
    total = prior_damage_fraction
    for block in blocks:
        if block.cycles_applied < 0:
            raise ValueError("cycles_applied must be non-negative")
        if block.cycles_to_failure <= 0:
            raise ValueError("cycles_to_failure must be positive")
        total += block.cycles_applied / block.cycles_to_failure
    return FatigueState(total, total >= 1.0)


def paris_crack_growth_per_cycle(*, delta_k_mpa_sqrt_m: float, c: float, m: float) -> float:
    """Return da/dN in units implied by C for a user-supplied Paris-law calibration."""
    if delta_k_mpa_sqrt_m < 0:
        raise ValueError("delta_k_mpa_sqrt_m must be non-negative")
    if c < 0 or m <= 0:
        raise ValueError("Paris-law C must be non-negative and m must be positive")
    return c * delta_k_mpa_sqrt_m**m


def project_paris_growth(
    *,
    initial_crack_m: float,
    cycles: int,
    delta_k_mpa_sqrt_m: float,
    c: float,
    m: float,
) -> float:
    if initial_crack_m < 0:
        raise ValueError("initial_crack_m must be non-negative")
    if cycles < 0:
        raise ValueError("cycles must be non-negative")
    growth = paris_crack_growth_per_cycle(
        delta_k_mpa_sqrt_m=delta_k_mpa_sqrt_m,
        c=c,
        m=m,
    )
    return initial_crack_m + cycles * growth
