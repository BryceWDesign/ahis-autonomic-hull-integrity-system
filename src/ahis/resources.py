"""Finite repair-resource accounting for AHIS v3.

The controller treats repair agent, electrical energy, thermal headroom and actuator
life as consumable resources.  No repair recipe is eligible if any required resource
would cross a declared floor.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RepairResourceBudget:
    agent_a_ml: float
    agent_b_ml: float
    electrical_energy_j: float
    thermal_headroom_c: float
    actuator_cycles_remaining: int

    def __post_init__(self) -> None:
        if min(self.agent_a_ml, self.agent_b_ml, self.electrical_energy_j, self.thermal_headroom_c) < 0:
            raise ValueError("resource values must be non-negative")
        if self.actuator_cycles_remaining < 0:
            raise ValueError("actuator_cycles_remaining must be non-negative")


@dataclass(frozen=True, slots=True)
class RepairDemand:
    agent_a_ml: float = 0.0
    agent_b_ml: float = 0.0
    electrical_energy_j: float = 0.0
    thermal_headroom_c: float = 0.0
    actuator_cycles: int = 1

    def __post_init__(self) -> None:
        if min(self.agent_a_ml, self.agent_b_ml, self.electrical_energy_j, self.thermal_headroom_c) < 0:
            raise ValueError("repair demand must be non-negative")
        if self.actuator_cycles < 0:
            raise ValueError("actuator_cycles must be non-negative")


@dataclass(frozen=True, slots=True)
class ResourceDecision:
    allowed: bool
    deficits: tuple[str, ...]
    remaining: RepairResourceBudget


def reserve_resources(budget: RepairResourceBudget, demand: RepairDemand) -> ResourceDecision:
    deficits: list[str] = []
    if budget.agent_a_ml < demand.agent_a_ml:
        deficits.append("agent_a_ml")
    if budget.agent_b_ml < demand.agent_b_ml:
        deficits.append("agent_b_ml")
    if budget.electrical_energy_j < demand.electrical_energy_j:
        deficits.append("electrical_energy_j")
    if budget.thermal_headroom_c < demand.thermal_headroom_c:
        deficits.append("thermal_headroom_c")
    if budget.actuator_cycles_remaining < demand.actuator_cycles:
        deficits.append("actuator_cycles_remaining")
    if deficits:
        return ResourceDecision(False, tuple(deficits), budget)
    return ResourceDecision(
        True,
        (),
        RepairResourceBudget(
            agent_a_ml=budget.agent_a_ml - demand.agent_a_ml,
            agent_b_ml=budget.agent_b_ml - demand.agent_b_ml,
            electrical_energy_j=budget.electrical_energy_j - demand.electrical_energy_j,
            thermal_headroom_c=budget.thermal_headroom_c - demand.thermal_headroom_c,
            actuator_cycles_remaining=budget.actuator_cycles_remaining - demand.actuator_cycles,
        ),
    )
