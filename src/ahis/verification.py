"""Post-repair verification fusion.

A repair attempt is accepted only when enough independent evidence channels pass.
Thresholds are supplied by the test program, never invented by this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class VerificationVerdict(str, Enum):
    PASS_POC = "pass_poc"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class VerificationChannel:
    channel_id: str
    value: float
    maximum_allowed: float
    healthy: bool = True
    required: bool = True

    @property
    def passed(self) -> bool:
        return self.healthy and self.value <= self.maximum_allowed


@dataclass(frozen=True, slots=True)
class VerificationResult:
    verdict: VerificationVerdict
    healthy_channel_count: int
    failed_channels: tuple[str, ...]
    unavailable_required_channels: tuple[str, ...]
    reason: str


def verify_repair(
    channels: Iterable[VerificationChannel],
    *,
    minimum_independent_channels: int = 3,
) -> VerificationResult:
    rows = tuple(channels)
    if minimum_independent_channels < 1:
        raise ValueError("minimum_independent_channels must be positive")
    ids = [row.channel_id for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("verification channel ids must be unique")
    if any(row.maximum_allowed < 0 for row in rows):
        raise ValueError("maximum_allowed must be non-negative")

    unavailable = tuple(row.channel_id for row in rows if row.required and not row.healthy)
    healthy = tuple(row for row in rows if row.healthy)
    failed = tuple(row.channel_id for row in healthy if not row.passed)

    if unavailable:
        return VerificationResult(
            VerificationVerdict.INCONCLUSIVE,
            len(healthy),
            failed,
            unavailable,
            "required verification evidence is unavailable",
        )
    if failed:
        return VerificationResult(
            VerificationVerdict.FAIL,
            len(healthy),
            failed,
            (),
            "one or more healthy verification channels exceed their acceptance bounds",
        )
    if len(healthy) < minimum_independent_channels:
        return VerificationResult(
            VerificationVerdict.INCONCLUSIVE,
            len(healthy),
            (),
            (),
            "independent verification quorum not met",
        )
    return VerificationResult(
        VerificationVerdict.PASS_POC,
        len(healthy),
        (),
        (),
        "all required channels pass and independent verification quorum is met",
    )
