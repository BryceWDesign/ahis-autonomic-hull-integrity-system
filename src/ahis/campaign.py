"""Deterministic AHIS v2 software-only extreme campaign."""
from __future__ import annotations

from dataclasses import asdict
from math import hypot
from typing import Any

from .barriers import Barrier, BarrierNetwork, BoundaryObservation
from .damage import SensorReading, localize_event
from .healing import DamageCase, select_healing_response
from .mission import AutonomicIntegrityManager


def _synthetic_arrivals(*, x: float, y: float, t0: float, speed: float, failed: set[str] | None = None) -> list[SensorReading]:
    coords = {
        "S1": (0.0, 0.0),
        "S2": (1.0, 0.0),
        "S3": (1.0, 1.0),
        "S4": (0.0, 1.0),
        "S5": (0.5, 0.0),
        "S6": (0.5, 1.0),
    }
    failed = failed or set()
    rows: list[SensorReading] = []
    for sid, (sx, sy) in coords.items():
        arrival = t0 + hypot(x - sx, y - sy) / speed
        rows.append(SensorReading(sid, sx, sy, arrival, 1.0, sid not in failed))
    return rows


def run_campaign() -> dict[str, Any]:
    speed = 2400.0
    damage = localize_event(
        _synthetic_arrivals(x=0.31, y=0.67, t0=0.020, speed=speed),
        wave_speed_m_s=speed,
        panel_bounds_m=(0.0, 1.0, 0.0, 1.0),
        amplitude_threshold=0.25,
        grid_points_per_axis=81,
        max_residual_s=7.0e-5,
    )
    barriers = BarrierNetwork(
        [
            Barrier("outer_sacrificial", False, True, True),
            Barrier("secondary_seal", True, True, True),
            Barrier("primary_pressure_wall", True, True, False),
            Barrier("inner_catch_skin", True, True, True),
        ]
    )
    barrier_nominal = barriers.assess(
        [
            BoundaryObservation("outer_sacrificial", 0.0, 1.0),
            BoundaryObservation("secondary_seal", 2.0, 1.0),
            BoundaryObservation("primary_pressure_wall", 0.0, 1.0),
            BoundaryObservation("inner_catch_skin", 0.0, 1.0),
        ]
    )
    healable = DamageCase(
        damage_kind="puncture",
        opening_mm=2.0,
        affected_area_mm2=30.0,
        through_thickness=True,
        substrate_family="hybrid_laminate",
        temperature_c=25.0,
        available_activation_temp_c=None,
        vascular_agent_available=True,
    )
    heal_decision = select_healing_response(healable)
    manager = AutonomicIntegrityManager()
    pre_verify = manager.decide(
        damage=damage,
        barriers=barrier_nominal,
        healing=heal_decision,
        post_heal_verification_passed=None,
    )
    post_verify = manager.decide(
        damage=damage,
        barriers=barrier_nominal,
        healing=heal_decision,
        post_heal_verification_passed=True,
    )

    wide_crack = select_healing_response(
        DamageCase(
            damage_kind="matrix_crack",
            opening_mm=3.0,
            affected_area_mm2=5000.0,
            through_thickness=False,
            substrate_family="vitrimer_composite",
            temperature_c=25.0,
            available_activation_temp_c=150.0,
            vascular_agent_available=True,
        )
    )
    dual_monitor_loss = barriers.assess(
        [
            BoundaryObservation("outer_sacrificial", 0.0, 1.0),
            BoundaryObservation("secondary_seal", 0.0, 1.0, sensor_healthy=False),
            BoundaryObservation("primary_pressure_wall", 0.0, 1.0, sensor_healthy=False),
            BoundaryObservation("inner_catch_skin", 0.0, 1.0),
        ]
    )
    degraded = manager.decide(
        damage=damage,
        barriers=dual_monitor_loss,
        healing=heal_decision,
        post_heal_verification_passed=None,
    )

    localization_error_m = None
    if damage.detected and damage.x_m is not None and damage.y_m is not None:
        localization_error_m = hypot(damage.x_m - 0.31, damage.y_m - 0.67)

    return {
        "schema_version": "2.0.0",
        "campaign": "AHIS-V2-EXTREME-SYNTHETIC-LOGIC-CAMPAIGN",
        "authority": "SOFTWARE_ONLY_SYNTHETIC_CONTROL_AND_EVIDENCE_LOGIC__NO_PHYSICAL_SURVIVAL_OR_HEALING_CREDIT",
        "positive_case": {
            "damage_estimate": asdict(damage),
            "localization_error_m": localization_error_m,
            "barrier_assessment": asdict(barrier_nominal),
            "healing_decision": asdict(heal_decision),
            "decision_before_verification": asdict(pre_verify),
            "decision_after_verification": asdict(post_verify),
        },
        "negative_controls": {
            "oversize_damage": asdict(wide_crack),
            "monitoring_redundancy_loss": asdict(dual_monitor_loss),
            "degraded_decision": asdict(degraded),
        },
        "pass_conditions": {
            "localization_within_30_mm": localization_error_m is not None and localization_error_m <= 0.03,
            "repair_not_equal_structural_restoration": heal_decision.structural_restoration_credit == 0.0,
            "recovery_requires_verification": not pre_verify.return_to_service_allowed,
            "post_verify_still_external_gate": not post_verify.return_to_service_allowed,
            "oversize_damage_rejected": not wide_crack.eligible,
            "monitor_loss_fails_closed": not dual_monitor_loss.containment_intact and not degraded.return_to_service_allowed,
        },
    }
