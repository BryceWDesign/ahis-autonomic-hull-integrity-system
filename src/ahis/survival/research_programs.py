"""Program-specific record completeness gate, never automatic physical promotion."""

from .numeric import scalar


def screen_record(program, record):
    required = {
        "program_id",
        "evidence_class",
        "specimen_id",
        "calibration_ids",
        "measurements",
        "test_groups",
        "reviewer",
        "raw_data_sha256",
    }
    if set(record) != required or record["program_id"] != program["id"]:
        raise ValueError("research record schema/program mismatch")
    reasons = []
    if record["evidence_class"] != "PHYSICAL":
        reasons.append("PHYSICAL_MEASUREMENTS_REQUIRED")
    if program["id"] == "R10":
        reasons.append("PROGRAM_NOT_IMPLEMENTED")
    if not record["specimen_id"] or not record["calibration_ids"] or not record["reviewer"]:
        reasons.append("TRACEABILITY_INCOMPLETE")
    digest = record["raw_data_sha256"]
    if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        reasons.append("RAW_DATA_DIGEST_INVALID")
    missing = set(program["required_measurements"]) - set(record["measurements"])
    if missing:
        reasons.append("MEASUREMENTS_MISSING:" + ",".join(sorted(missing)))
    if set(program["required_test_groups"]) - set(record["test_groups"]):
        reasons.append("TEST_GROUPS_MISSING")
    for metric, row in record["measurements"].items():
        if set(row) != {"value", "lower", "upper", "unit"}:
            raise ValueError("invalid research measurement")
        lo = scalar(row["lower"])
        hi = scalar(row["upper"])
        value = scalar(row["value"])
        if lo > hi or not row["unit"]:
            raise ValueError("invalid research measurement limits/unit")
        if not lo <= value <= hi:
            reasons.append("MEASUREMENT_LIMIT:" + metric)
    return {
        "eligible_for_human_review": not reasons,
        "reasons": reasons,
        "physical_credit": False,
        "operational_return_to_service_authorized": False,
        "scope": "RECORD_COMPLETENESS_ONLY__AUTHENTICITY_AND_QUALIFICATION_REQUIRE_HUMAN_REVIEW",
    }
