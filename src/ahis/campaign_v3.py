"""Deterministic AHIS v3 software/HIL qualification campaign."""
from __future__ import annotations

from dataclasses import asdict
from math import hypot
from typing import Any

from .digital_twin import TwinBaseline, TwinObservation, assess_twin
from .fusion import EvidenceChannel, fuse_evidence
from .hardware import HILRig, InterlockLimits, RepairRecipe, assess_interlocks
from .history import StructuralHistory
from .localization_v3 import AnisotropicPropagation, ArrivalObservation, localize_anisotropic
from .prognostics import FatigueState, screen_remaining_cycles
from .repair_control import plan_two_agent_repair
from .resources import RepairResourceBudget

AUTHORITY = "SOFTWARE_AND_HIL_ONLY__NO_PHYSICAL_HEALING_OR_HULL_SURVIVABILITY_CREDIT"


def _arrivals(x: float, y: float, t0: float, model: AnisotropicPropagation) -> list[ArrivalObservation]:
    coords = {
        "A1": (0.0, 0.0),
        "A2": (1.0, 0.0),
        "A3": (1.0, 1.0),
        "A4": (0.0, 1.0),
        "A5": (0.5, 0.0),
        "A6": (0.5, 1.0),
    }
    out: list[ArrivalObservation] = []
    for sid, (sx, sy) in coords.items():
        dx, dy = x - sx, y - sy
        arrival = t0 + hypot(dx, dy) / model.speed(dx, dy)
        out.append(ArrivalObservation(sid, sx, sy, arrival, 1.0))
    return out


def run_campaign() -> dict[str, Any]:
    propagation = AnisotropicPropagation(2450.0, 0.12, 20.0)
    localization = localize_anisotropic(
        _arrivals(0.35, 0.65, 0.02, propagation),
        model=propagation,
        bounds_m=(0.0, 1.0, 0.0, 1.0),
        grid_points_per_axis=81,
        max_weighted_rms_s=6e-5,
    )
    localization_error_m = None
    if localization.accepted and localization.x_m is not None and localization.y_m is not None:
        localization_error_m = hypot(localization.x_m - 0.35, localization.y_m - 0.65)

    fusion = fuse_evidence(
        [
            EvidenceChannel("guided_wave", 0.91, 0.95),
            EvidenceChannel("acoustic_emission", 0.86, 0.90),
            EvidenceChannel("pressure_leak", 0.96, 1.00),
            EvidenceChannel("strain", 0.72, 0.75),
        ],
        threshold=0.65,
        min_effective_weight=2.5,
    )

    rig = HILRig(initial_leak_ml_min=60.0, response_scale_ml=8.0)
    frame0 = rig.frame(0.0)
    interlock = assess_interlocks(frame0, InterlockLimits())
    recipe = RepairRecipe("P1-HIL-TWO-AGENT", 14.0, 14.0, 30.0, 0.80)
    budget = RepairResourceBudget(50.0, 50.0, 5000.0, 40.0, 20)
    plan = plan_two_agent_repair(
        recipe,
        budget=budget,
        interlock=interlock,
        pump_a_ml_s=rig.pump_a_ml_s,
        pump_b_ml_s=rig.pump_b_ml_s,
        electrical_energy_j=500.0,
    )
    delivered_a = rig.delivered_volume(plan.commands[0]) if plan.allowed else 0.0
    delivered_b = rig.delivered_volume(plan.commands[1]) if plan.allowed else 0.0
    post = rig.frame(40.0, delivered_a, delivered_b)
    hil_reduction = 1.0 - post.leak_ml_min / frame0.leak_ml_min

    estop_rig = HILRig(estop_closed=False)
    estop_denial = assess_interlocks(estop_rig.frame(0.0), InterlockLimits())
    overpressure_rig = HILRig(injected_pressure_kpa=9.0)
    overpressure_denial = assess_interlocks(overpressure_rig.frame(0.0), InterlockLimits())
    depleted = plan_two_agent_repair(
        recipe,
        budget=RepairResourceBudget(2.0, 2.0, 100.0, 10.0, 1),
        interlock=interlock,
        pump_a_ml_s=rig.pump_a_ml_s,
        pump_b_ml_s=rig.pump_b_ml_s,
    )

    twin_nominal = assess_twin(
        TwinBaseline((120.0, 248.0, 390.0), 500.0, 0.5),
        TwinObservation((119.5, 247.0, 389.0), 510.0, 1.0),
    )
    twin_damage = assess_twin(
        TwinBaseline((120.0, 248.0, 390.0), 500.0, 0.5),
        TwinObservation((110.0, 230.0, 360.0), 590.0, 12.0),
    )
    rul = screen_remaining_cycles(FatigueState(0.42, 1.5e-5, 0.25))

    history = StructuralHistory()
    history.append("damage_detected", "2026-09-03T18:00:00Z", {"score": round(fusion.fused_damage_score, 6)})
    history.append("repair_commanded", "2026-09-03T18:00:01Z", {"recipe": recipe.recipe_id})
    history.append("hil_verified", "2026-09-03T18:00:40Z", {"leak_reduction_fraction": round(hil_reduction, 6)})

    conditions = {
        "anisotropic_localization_accepted": localization.accepted,
        "localization_within_20_mm": localization_error_m is not None and localization_error_m <= 0.02,
        "uncertainty_reported": localization.confidence_radius_m is not None,
        "multimodal_fusion_accepted": fusion.accepted,
        "repair_plan_allowed_when_safe": plan.allowed,
        "finite_resources_consumed": plan.resource_decision.allowed and plan.resource_decision.remaining.agent_a_ml < budget.agent_a_ml,
        "hil_response_exceeds_recipe_target": hil_reduction >= recipe.target_leak_reduction_fraction,
        "estop_fails_closed": not estop_denial.allowed,
        "overpressure_fails_closed": not overpressure_denial.allowed,
        "depleted_resources_fail_closed": not depleted.allowed,
        "twin_nominal_accepted": twin_nominal.accepted,
        "twin_damage_detected": not twin_damage.accepted,
        "rul_has_uncertainty_bounds": rul.lower_cycles <= rul.nominal_cycles <= rul.upper_cycles,
        "history_chain_valid": not history.verify(),
        "physical_credit_remains_zero": True,
    }

    return {
        "schema_version": "3.0.0",
        "campaign": "AHIS-V3-AUTONOMIC-REPAIR-SOFTWARE-HIL-CAMPAIGN",
        "authority": AUTHORITY,
        "localization": asdict(localization) | {"error_m": localization_error_m},
        "fusion": asdict(fusion),
        "repair_plan": {
            "allowed": plan.allowed,
            "commands": [asdict(c) for c in plan.commands],
            "remaining_resources": asdict(plan.resource_decision.remaining),
            "reason": plan.reason,
        },
        "hil": {
            "baseline_frame": asdict(frame0),
            "post_frame": asdict(post),
            "delivered_a_ml": delivered_a,
            "delivered_b_ml": delivered_b,
            "leak_reduction_fraction": hil_reduction,
        },
        "negative_controls": {
            "estop": asdict(estop_denial),
            "overpressure": asdict(overpressure_denial),
            "resource_depletion": {"allowed": depleted.allowed, "reason": depleted.reason},
            "damaged_twin": asdict(twin_damage),
        },
        "prognostics": asdict(rul),
        "structural_history": history.as_records(),
        "pass_conditions": conditions,
    }
