"""Independent barrier and monitored-interspace containment logic."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Barrier:
    barrier_id: str
    structural: bool
    independent_monitor: bool
    can_isolate: bool


@dataclass(frozen=True, slots=True)
class BoundaryObservation:
    barrier_id: str
    leak_rate: float
    leak_alarm_threshold: float
    sensor_healthy: bool = True

    @property
    def alarm(self) -> bool:
        return self.sensor_healthy and self.leak_rate >= self.leak_alarm_threshold


@dataclass(frozen=True, slots=True)
class BarrierAssessment:
    containment_intact: bool
    isolate_barriers: tuple[str, ...]
    unobservable_barriers: tuple[str, ...]
    structural_failures: tuple[str, ...]
    reason: str


class BarrierNetwork:
    def __init__(self, barriers: Iterable[Barrier]) -> None:
        rows = tuple(barriers)
        if len(rows) < 2:
            raise ValueError("at least two independent barriers are required")
        ids = [b.barrier_id for b in rows]
        if len(ids) != len(set(ids)):
            raise ValueError("barrier ids must be unique")
        self.barriers = rows
        self._by_id = {b.barrier_id: b for b in rows}

    def assess(self, observations: Iterable[BoundaryObservation]) -> BarrierAssessment:
        obs = tuple(observations)
        if set(o.barrier_id for o in obs) - set(self._by_id):
            raise ValueError("observation references unknown barrier")
        by_id = {o.barrier_id: o for o in obs}
        unobservable = tuple(
            b.barrier_id
            for b in self.barriers
            if b.independent_monitor and (b.barrier_id not in by_id or not by_id[b.barrier_id].sensor_healthy)
        )
        failed = tuple(
            b.barrier_id
            for b in self.barriers
            if b.structural and b.barrier_id in by_id and by_id[b.barrier_id].alarm
        )
        isolate = tuple(
            bid for bid in failed if self._by_id[bid].can_isolate
        )
        # Fail closed if a structural barrier is both unobservable and not backed by
        # enough other monitored structural boundaries.
        structural_total = sum(1 for b in self.barriers if b.structural)
        structural_observable = sum(
            1
            for b in self.barriers
            if b.structural and b.barrier_id not in unobservable
        )
        containment_intact = len(failed) < structural_total and structural_observable >= 2
        reason = (
            "remaining independent monitored boundaries preserve containment logic"
            if containment_intact
            else "containment cannot be asserted; structural redundancy or observability is insufficient"
        )
        return BarrierAssessment(
            containment_intact=containment_intact,
            isolate_barriers=isolate,
            unobservable_barriers=unobservable,
            structural_failures=failed,
            reason=reason,
        )
