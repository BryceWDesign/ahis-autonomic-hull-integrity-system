"""Bounded repair hardware model and deterministic hardware-in-the-loop emulator.

Nothing in this module is physical evidence.  HIL exists to prove control invariants,
fault handling and evidence plumbing before hardware is connected.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import exp, isfinite


class PumpChannel(str, Enum):
    AGENT_A = "agent_a"
    AGENT_B = "agent_b"


@dataclass(frozen=True, slots=True)
class SensorFrame:
    timestamp_s: float
    head_mm: float
    pressure_kpa: float
    leak_ml_min: float
    supply_v: float
    estop_closed: bool
    sensor_valid: bool = True

    def __post_init__(self) -> None:
        values = (self.timestamp_s, self.head_mm, self.pressure_kpa, self.leak_ml_min, self.supply_v)
        if not all(isfinite(v) for v in values):
            raise ValueError("sensor frame contains non-finite value")
        if self.timestamp_s < 0 or self.head_mm < 0 or self.pressure_kpa < 0 or self.leak_ml_min < 0 or self.supply_v < 0:
            raise ValueError("sensor frame contains negative physical magnitude")


@dataclass(frozen=True, slots=True)
class InterlockLimits:
    max_head_mm: float = 800.0
    max_pressure_kpa: float = 8.0
    max_supply_v: float = 13.0


@dataclass(frozen=True, slots=True)
class InterlockDecision:
    allowed: bool
    reasons: tuple[str, ...]


def assess_interlocks(frame: SensorFrame, limits: InterlockLimits) -> InterlockDecision:
    reasons: list[str] = []
    if not frame.estop_closed:
        reasons.append("estop_open")
    if not frame.sensor_valid:
        reasons.append("sensor_invalid")
    if frame.head_mm > limits.max_head_mm:
        reasons.append("head_limit_exceeded")
    if frame.pressure_kpa > limits.max_pressure_kpa:
        reasons.append("pressure_limit_exceeded")
    if frame.supply_v > limits.max_supply_v:
        reasons.append("supply_limit_exceeded")
    return InterlockDecision(not reasons, tuple(reasons))


@dataclass(frozen=True, slots=True)
class RepairRecipe:
    recipe_id: str
    agent_a_ml: float
    agent_b_ml: float
    max_runtime_s: float
    target_leak_reduction_fraction: float

    def __post_init__(self) -> None:
        if not self.recipe_id.strip():
            raise ValueError("recipe_id is required")
        if self.agent_a_ml < 0 or self.agent_b_ml < 0 or self.max_runtime_s <= 0:
            raise ValueError("invalid recipe quantities")
        if not 0 < self.target_leak_reduction_fraction <= 1:
            raise ValueError("target reduction must be in (0,1]")


@dataclass(frozen=True, slots=True)
class HardwareCommand:
    channel: PumpChannel
    runtime_s: float

    def __post_init__(self) -> None:
        if self.runtime_s <= 0:
            raise ValueError("runtime_s must be positive")


@dataclass(slots=True)
class HILRig:
    """Deterministic synthetic rig used only for software qualification."""

    initial_leak_ml_min: float = 60.0
    head_mm: float = 500.0
    pressure_kpa: float = 4.9
    supply_v: float = 12.0
    pump_a_ml_s: float = 0.75
    pump_b_ml_s: float = 0.75
    response_scale_ml: float = 8.0
    estop_closed: bool = True
    sensor_valid: bool = True
    injected_pressure_kpa: float | None = None

    def frame(self, timestamp_s: float, delivered_a_ml: float = 0.0, delivered_b_ml: float = 0.0) -> SensorFrame:
        paired = min(max(delivered_a_ml, 0.0), max(delivered_b_ml, 0.0))
        reduction = 1.0 - exp(-paired / max(self.response_scale_ml, 1e-9))
        leak = self.initial_leak_ml_min * max(0.02, 1.0 - reduction)
        return SensorFrame(
            timestamp_s=timestamp_s,
            head_mm=self.head_mm,
            pressure_kpa=self.injected_pressure_kpa if self.injected_pressure_kpa is not None else self.pressure_kpa,
            leak_ml_min=leak,
            supply_v=self.supply_v,
            estop_closed=self.estop_closed,
            sensor_valid=self.sensor_valid,
        )

    def delivered_volume(self, command: HardwareCommand) -> float:
        rate = self.pump_a_ml_s if command.channel is PumpChannel.AGENT_A else self.pump_b_ml_s
        return rate * command.runtime_s
