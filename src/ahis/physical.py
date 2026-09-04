"""AHIS-P1 physical evidence structures and acceptance logic.

Only files explicitly marked source_kind='PHYSICAL_MEASUREMENT' may enter this path.
Synthetic or HIL data is rejected by construction. Physical receipts bind the summary
metrics to the raw telemetry digest and calibration bundle digest.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math


def _require_sha256(name: str, value: str) -> None:
    if len(value) != 64 or any(c not in "0123456789abcdef" for c in value.lower()):
        raise ValueError(f"{name} must be a 64-character SHA-256 hex digest")


@dataclass(frozen=True, slots=True)
class P1RunEvidence:
    run_id: str
    source_kind: str
    baseline_leak_ml_min: float
    post_repair_leak_ml_min: float
    baseline_fit_r_squared: float
    post_fit_r_squared: float
    baseline_sample_count: int
    post_sample_count: int
    max_head_mm: float
    max_pressure_kpa: float
    estop_violation: bool
    unintended_fixture_leak: bool
    calibration_sha256: str
    telemetry_sha256: str

    def __post_init__(self) -> None:
        if self.source_kind != "PHYSICAL_MEASUREMENT":
            raise ValueError("P1 physical evidence rejects non-physical source_kind")
        if not self.run_id.strip():
            raise ValueError("run_id required")
        numeric = (
            self.baseline_leak_ml_min,
            self.post_repair_leak_ml_min,
            self.baseline_fit_r_squared,
            self.post_fit_r_squared,
            self.max_head_mm,
            self.max_pressure_kpa,
        )
        if any(not math.isfinite(v) for v in numeric):
            raise ValueError("physical evidence values must be finite")
        if min(self.baseline_leak_ml_min, self.post_repair_leak_ml_min, self.max_head_mm, self.max_pressure_kpa) < 0:
            raise ValueError("physical magnitudes must be non-negative")
        if not (0.0 <= self.baseline_fit_r_squared <= 1.0 and 0.0 <= self.post_fit_r_squared <= 1.0):
            raise ValueError("R-squared values must be between zero and one")
        if self.baseline_sample_count < 1 or self.post_sample_count < 1:
            raise ValueError("sample counts must be positive")
        _require_sha256("calibration_sha256", self.calibration_sha256)
        _require_sha256("telemetry_sha256", self.telemetry_sha256)


@dataclass(frozen=True, slots=True)
class P1RunAssessment:
    passed: bool
    leak_reduction_fraction: float
    conditions: dict[str, bool]


def assess_p1_run(run: P1RunEvidence) -> P1RunAssessment:
    reduction = 0.0 if run.baseline_leak_ml_min <= 0 else 1.0 - run.post_repair_leak_ml_min / run.baseline_leak_ml_min
    conditions = {
        "baseline_leak_at_least_20_ml_min": run.baseline_leak_ml_min >= 20.0,
        "leak_reduction_at_least_80_percent": reduction >= 0.80,
        "baseline_fit_r_squared_at_least_0_95": run.baseline_fit_r_squared >= 0.95,
        "post_fit_r_squared_at_least_0_95": run.post_fit_r_squared >= 0.95,
        "baseline_at_least_20_samples": run.baseline_sample_count >= 20,
        "post_at_least_20_samples": run.post_sample_count >= 20,
        "gravity_head_within_800_mm": run.max_head_mm <= 800.0,
        "pressure_within_8_kpa": run.max_pressure_kpa <= 8.0,
        "no_estop_violation": not run.estop_violation,
        "no_unintended_fixture_leak": not run.unintended_fixture_leak,
    }
    return P1RunAssessment(all(conditions.values()), reduction, conditions)


def assess_p1_campaign(runs: list[P1RunEvidence]) -> dict[str, object]:
    if len(runs) != 3:
        raise ValueError("canonical P1 campaign requires exactly three independent runs")
    assessments = [assess_p1_run(r) for r in runs]
    pass_count = sum(a.passed for a in assessments)
    return {
        "physical_demonstration": pass_count >= 2,
        "pass_count": pass_count,
        "required_pass_count": 2,
        "run_results": [
            a.conditions | {"passed": a.passed, "leak_reduction_fraction": a.leak_reduction_fraction}
            for a in assessments
        ],
    }


def physical_run_receipt(run: P1RunEvidence) -> str:
    payload = {
        name: getattr(run, name)
        for name in run.__dataclass_fields__
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(raw).hexdigest()
