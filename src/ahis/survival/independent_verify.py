"""Held-out channel and acquisition-group verification; no physical promotion."""

from .numeric import finite, scalar

NUMERICAL_RELATIVE_TOLERANCE = 1e-9


def verify(channels, *, planning_ids, planning_groups, response_bounds, minimum_channels=2):
    if type(minimum_channels) is not int or minimum_channels < 1:
        raise ValueError("invalid quorum")
    if (
        set(response_bounds) != {"lower", "upper", "scenario_ids", "scope", "measurement_noise_included"}
        or response_bounds["scope"] != "DECLARED_FINITE_SET_ONLY"
        or response_bounds["measurement_noise_included"] is not False
    ):
        raise ValueError("invalid response-consistency bounds")

    scenario_ids = response_bounds["scenario_ids"]
    if (
        not isinstance(scenario_ids, list)
        or not scenario_ids
        or any(not isinstance(v, str) or not v.strip() for v in scenario_ids)
        or len(scenario_ids) != len(set(scenario_ids))
    ):
        raise ValueError("invalid response-consistency scenarios")

    expected_lower = finite(response_bounds["lower"], (len(channels),))
    expected_upper = finite(response_bounds["upper"], (len(channels),))
    if any(lo > hi for lo, hi in zip(expected_lower, expected_upper)):
        raise ValueError("invalid response-consistency interval")

    ids = [c["id"] for c in channels]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate verification channel")

    reasons = []
    groups = set()
    count = 0

    for i, c in enumerate(channels):
        if (
            set(c) != {"id", "group", "value", "lower", "upper", "healthy", "required"}
            or type(c["healthy"]) is not bool
            or type(c["required"]) is not bool
        ):
            raise ValueError("invalid held-out channel")

        lo = scalar(c["lower"])
        hi = scalar(c["upper"])
        value = scalar(c["value"])

        if lo >= hi or not c["id"] or not c["group"]:
            raise ValueError("invalid channel interval/identity")

        if c["id"] in planning_ids or c["group"] in planning_groups:
            reasons.append("PLANNING_EVIDENCE_REUSED:" + c["id"])
            continue

        if not c["healthy"]:
            if c["required"]:
                reasons.append("REQUIRED_UNAVAILABLE:" + c["id"])
            continue

        count += 1
        groups.add(c["group"])

        if not lo <= value <= hi:
            reasons.append("HELD_OUT_LIMIT:" + c["id"])

        model_lo = float(expected_lower[i])
        model_hi = float(expected_upper[i])
        tolerance = NUMERICAL_RELATIVE_TOLERANCE * max(1.0, abs(value), abs(model_lo), abs(model_hi))

        if value < model_lo - tolerance or value > model_hi + tolerance:
            reasons.append("RESPONSE_MODEL_INCONSISTENT:" + c["id"])

    if count < minimum_channels or len(groups) < minimum_channels:
        reasons.append("INDEPENDENT_QUORUM_NOT_MET")

    return {
        "passed": not reasons,
        "reasons": reasons,
        "healthy_channels": count,
        "independent_groups": len(groups),
        "response_consistency": {
            "lower": expected_lower.tolist(),
            "upper": expected_upper.tolist(),
            "scenario_ids": scenario_ids,
            "scope": response_bounds["scope"],
            "measurement_noise_included": False,
            "numerical_relative_tolerance": NUMERICAL_RELATIVE_TOLERANCE,
        },
        "physical_credit": False,
        "return_to_service_allowed": False,
    }
