"""Evidence-gated healing/sealing mechanism selection.

The repository distinguishes four things that marketing often collapses together:
1) hole sealing, 2) crack closure, 3) matrix/interfacial property recovery, and
4) restoration of certified structural load capacity. AHIS v2 grants no physical
load-capacity credit without test evidence for the exact material/process/geometry.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class HealingMechanism(str, Enum):
    IONOMER_PUNCTURE_SEAL = "ionomer_puncture_seal"
    MICROVASCULAR_MATRIX_REPAIR = "microvascular_matrix_repair"
    VITRIMER_THERMAL_REPAIR = "vitrimer_thermal_repair"
    SMA_LIQUID_ASSISTED_METAL_REPAIR = "sma_liquid_assisted_metal_repair"
    NONE = "none"


@dataclass(frozen=True, slots=True)
class DamageCase:
    damage_kind: str
    opening_mm: float
    affected_area_mm2: float
    through_thickness: bool
    substrate_family: str
    temperature_c: float
    available_activation_temp_c: float | None
    vascular_agent_available: bool
    healing_cycles_used: int = 0


@dataclass(frozen=True, slots=True)
class HealingDecision:
    mechanism: HealingMechanism
    eligible: bool
    seal_credit: bool
    structural_restoration_credit: float
    requires_verification: bool
    reason: str


def _base_validation(d: DamageCase) -> None:
    if d.opening_mm < 0 or d.affected_area_mm2 < 0:
        raise ValueError("damage dimensions must be non-negative")
    if d.healing_cycles_used < 0:
        raise ValueError("healing_cycles_used must be non-negative")


def select_healing_response(d: DamageCase) -> HealingDecision:
    """Select a conservative research mechanism from declared conditions.

    Thresholds here are *software campaign bounds*, not material allowables. They are
    intentionally modest and exist to test control logic. Physical promotion requires
    coupon/panel data for the exact material and manufacturing route.
    """
    _base_validation(d)
    family = d.substrate_family.strip().lower()
    kind = d.damage_kind.strip().lower()

    # Fast puncture-seal lane. This represents an ionomeric secondary sealing layer,
    # not the primary structural pressure wall.
    if d.through_thickness and kind in {"puncture", "small_perforation"}:
        if d.opening_mm <= 4.0 and family in {"polymer_liner", "hybrid_laminate", "composite_liner"}:
            return HealingDecision(
                mechanism=HealingMechanism.IONOMER_PUNCTURE_SEAL,
                eligible=True,
                seal_credit=True,
                structural_restoration_credit=0.0,
                requires_verification=True,
                reason="secondary ionomeric liner lane can be commanded/observed as a sealing response; structural strength remains uncredited",
            )

    # Replenishable vascular lane for matrix/interface cracks. Multiple events are
    # possible only while the reservoir/network remains available.
    if kind in {"matrix_crack", "delamination_edge", "bondline_crack"}:
        if d.opening_mm <= 0.75 and d.affected_area_mm2 <= 2500 and d.vascular_agent_available and d.healing_cycles_used < 3:
            return HealingDecision(
                mechanism=HealingMechanism.MICROVASCULAR_MATRIX_REPAIR,
                eligible=True,
                seal_credit=False,
                structural_restoration_credit=0.0,
                requires_verification=True,
                reason="damage lies inside the software campaign envelope for a replenishability-aware vascular repair lane",
            )

    # Intrinsic dynamic-covalent network lane. Heat is an explicit resource and can
    # be denied by environment/thermal-budget logic.
    if family in {"vitrimer_composite", "vitrimer_bondline"} and kind in {"matrix_crack", "bondline_crack", "microcrack"}:
        if d.opening_mm <= 0.50 and d.available_activation_temp_c is not None and d.available_activation_temp_c >= 120.0:
            return HealingDecision(
                mechanism=HealingMechanism.VITRIMER_THERMAL_REPAIR,
                eligible=True,
                seal_credit=False,
                structural_restoration_credit=0.0,
                requires_verification=True,
                reason="intrinsic thermal repair lane is available; exact temperature/time/strength recovery must come from material qualification",
            )

    # NASA-inspired metal-matrix lane. The model never treats this as instant or
    # universally applicable. It requires a compatible engineered MMC and heat cycle.
    if family == "sma_liquid_assisted_mmc" and kind in {"fatigue_crack", "metal_crack"}:
        if d.opening_mm <= 2.0 and d.available_activation_temp_c is not None and d.available_activation_temp_c >= 140.0:
            return HealingDecision(
                mechanism=HealingMechanism.SMA_LIQUID_ASSISTED_METAL_REPAIR,
                eligible=True,
                seal_credit=False,
                structural_restoration_credit=0.0,
                requires_verification=True,
                reason="heat-activated crack-closure/fill lane is logically available for a specifically engineered MMC; no generic hull-strength credit is granted",
            )

    return HealingDecision(
        mechanism=HealingMechanism.NONE,
        eligible=False,
        seal_credit=False,
        structural_restoration_credit=0.0,
        requires_verification=True,
        reason="damage falls outside every declared healing/sealing envelope; isolate and remain degraded",
    )
