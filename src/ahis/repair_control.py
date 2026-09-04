"""Evidence-gated repair planning and bounded command generation."""
from __future__ import annotations

from dataclasses import dataclass

from .hardware import HardwareCommand, InterlockDecision, PumpChannel, RepairRecipe
from .resources import RepairDemand, RepairResourceBudget, ResourceDecision, reserve_resources


@dataclass(frozen=True, slots=True)
class RepairPlan:
    allowed: bool
    commands: tuple[HardwareCommand, ...]
    resource_decision: ResourceDecision
    reason: str


def plan_two_agent_repair(
    recipe: RepairRecipe,
    *,
    budget: RepairResourceBudget,
    interlock: InterlockDecision,
    pump_a_ml_s: float,
    pump_b_ml_s: float,
    electrical_energy_j: float = 120.0,
) -> RepairPlan:
    if pump_a_ml_s <= 0 or pump_b_ml_s <= 0:
        raise ValueError("pump calibrations must be positive")
    demand = RepairDemand(
        agent_a_ml=recipe.agent_a_ml,
        agent_b_ml=recipe.agent_b_ml,
        electrical_energy_j=electrical_energy_j,
        actuator_cycles=2,
    )
    resource = reserve_resources(budget, demand)
    if not interlock.allowed:
        return RepairPlan(False, (), resource, f"hardware interlock denied: {','.join(interlock.reasons)}")
    if not resource.allowed:
        return RepairPlan(False, (), resource, f"resource deficit: {','.join(resource.deficits)}")
    ta = recipe.agent_a_ml / pump_a_ml_s
    tb = recipe.agent_b_ml / pump_b_ml_s
    if ta > recipe.max_runtime_s or tb > recipe.max_runtime_s:
        return RepairPlan(False, (), resource, "calibrated pump runtime exceeds recipe hard limit")
    return RepairPlan(
        True,
        (HardwareCommand(PumpChannel.AGENT_A, ta), HardwareCommand(PumpChannel.AGENT_B, tb)),
        resource,
        "repair command sequence allowed by resource and hardware gates",
    )
