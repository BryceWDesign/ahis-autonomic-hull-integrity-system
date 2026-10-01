"""Held-out channel and acquisition-group verification; no physical promotion."""

from .numeric import scalar


def verify(channels, *, planning_ids, planning_groups, minimum_channels=2):
    if type(minimum_channels) is not int or minimum_channels < 1:
        raise ValueError("invalid quorum")
    ids = [c["id"] for c in channels]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate verification channel")
    reasons = []
    groups = set()
    count = 0
    for c in channels:
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
    if count < minimum_channels or len(groups) < minimum_channels:
        reasons.append("INDEPENDENT_QUORUM_NOT_MET")
    return {
        "passed": not reasons,
        "reasons": reasons,
        "healthy_channels": count,
        "independent_groups": len(groups),
        "physical_credit": False,
        "return_to_service_allowed": False,
    }
