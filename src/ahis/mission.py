"""Autonomic integrity decision state machine.

The state machine deliberately prevents a heal command from becoming a safety claim.
Detection, containment, repair attempt, and verification are separate gates.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .barriers import BarrierAssessment
from .damage import DamageEstimate
from .healing import HealingDecision


class IntegrityState(str, Enum):
    NOMINAL = "nominal"
    SUSPECT = "suspect"
    DAMAGED = "damaged"
    CONTAINED = "contained"
    HEALING = "healing"
    VERIFY = "verify"
    RECOVERED_LIMITED = "recovered_limited"
    DEGRADED_SAFE = "degraded_safe"


@dataclass(frozen=True, slots=True)
class MissionDecision:
    state: IntegrityState
    isolate: tuple[str, ...]
    activate_healing: bool
    require_ndt: bool
    return_to_service_allowed: bool
    reason: str


class AutonomicIntegrityManager:
    def decide(
        self,
        *,
        damage: DamageEstimate,
        barriers: BarrierAssessment,
        healing: HealingDecision,
        post_heal_verification_passed: bool | None,
    ) -> MissionDecision:
        if not barriers.containment_intact:
            return MissionDecision(
                state=IntegrityState.DEGRADED_SAFE,
                isolate=barriers.isolate_barriers,
                activate_healing=False,
                require_ndt=True,
                return_to_service_allowed=False,
                reason="containment or observability is insufficient; fail closed",
            )
        if not damage.detected:
            if barriers.unobservable_barriers:
                return MissionDecision(
                    state=IntegrityState.SUSPECT,
                    isolate=barriers.isolate_barriers,
                    activate_healing=False,
                    require_ndt=True,
                    return_to_service_allowed=False,
                    reason="no localized damage, but monitoring redundancy is degraded",
                )
            return MissionDecision(
                state=IntegrityState.NOMINAL,
                isolate=(),
                activate_healing=False,
                require_ndt=False,
                return_to_service_allowed=True,
                reason="no accepted damage event and containment monitors are healthy",
            )

        if not healing.eligible:
            return MissionDecision(
                state=IntegrityState.DEGRADED_SAFE,
                isolate=barriers.isolate_barriers,
                activate_healing=False,
                require_ndt=True,
                return_to_service_allowed=False,
                reason="damage detected outside autonomous healing envelope",
            )

        if post_heal_verification_passed is None:
            return MissionDecision(
                state=IntegrityState.HEALING,
                isolate=barriers.isolate_barriers,
                activate_healing=True,
                require_ndt=True,
                return_to_service_allowed=False,
                reason="eligible repair response selected; verification gate remains open",
            )
        if not post_heal_verification_passed:
            return MissionDecision(
                state=IntegrityState.DEGRADED_SAFE,
                isolate=barriers.isolate_barriers,
                activate_healing=False,
                require_ndt=True,
                return_to_service_allowed=False,
                reason="post-heal verification failed; no restoration credit granted",
            )
        return MissionDecision(
            state=IntegrityState.RECOVERED_LIMITED,
            isolate=barriers.isolate_barriers,
            activate_healing=False,
            require_ndt=True,
            return_to_service_allowed=False,
            reason="repair response verified at PoC level; operational load-capacity return remains externally gated",
        )
