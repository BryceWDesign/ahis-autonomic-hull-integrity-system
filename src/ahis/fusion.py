"""Transparent multimodal damage-evidence fusion.

This intentionally avoids opaque ML.  Each modality contributes a bounded score and
quality weight.  The output preserves disagreement instead of hiding it.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvidenceChannel:
    name: str
    damage_score: float
    quality: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("evidence channel name required")
        if not 0 <= self.damage_score <= 1 or not 0 <= self.quality <= 1:
            raise ValueError("damage_score and quality must be in [0,1]")


@dataclass(frozen=True, slots=True)
class FusionResult:
    fused_damage_score: float
    effective_weight: float
    disagreement: float
    accepted: bool
    reason: str


def fuse_evidence(channels: list[EvidenceChannel], *, threshold: float = 0.6, min_effective_weight: float = 1.5) -> FusionResult:
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be in [0,1]")
    if min_effective_weight <= 0:
        raise ValueError("min_effective_weight must be positive")
    usable = [c for c in channels if c.quality > 0]
    total = sum(c.quality for c in usable)
    if total < min_effective_weight:
        return FusionResult(0.0, total, 1.0, False, "insufficient independent evidence quality")
    mean = sum(c.damage_score * c.quality for c in usable) / total
    disagreement = sum(c.quality * abs(c.damage_score - mean) for c in usable) / total
    # Penalize strong inter-modality disagreement without silently discarding channels.
    fused = max(0.0, min(1.0, mean * (1.0 - 0.5 * disagreement)))
    accepted = fused >= threshold
    return FusionResult(
        fused_damage_score=fused,
        effective_weight=total,
        disagreement=disagreement,
        accepted=accepted,
        reason="multimodal evidence accepted" if accepted else "fused evidence below acceptance threshold",
    )
