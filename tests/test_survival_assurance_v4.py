from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import os
import math
import pytest
from ahis.survival.numeric import load_json, digest
from ahis.survival.campaign import cases, synthetic_response
from ahis.survival.controller import decide
from ahis.survival.replay_audit import record, audit
from ahis.survival.accounting import closure, impact_energy, agent_mass
from ahis.survival.propagation import trace_hazards
from ahis.survival.adaptive_state import SurvivalMachine, State
from ahis.survival.protection_stack import protective_phase, stack_screen

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = load_json(ROOT / "configs/survival_reference.json")
CASES = cases(TEMPLATE)


@pytest.mark.parametrize("name,evidence,expected", CASES, ids=[c[0] for c in CASES])
def test_end_to_end_negative_controls(name, evidence, expected):
    r = decide(evidence)
    assert r["state"] == expected
    assert not r["physical_credit"] and not r["hardware_authority"] and not r["return_to_service_allowed"]
    if r["plan"] and not r["plan"]["accepted"]:
        assert (
            list(r["commands"].values()) == [0] * 4
            and r["resource_remaining"] == evidence["budget"]["resources"]
        )
    if expected == "RECOVERED_LIMITED":
        assert r["verification"]["passed"] and r["plan"]["robustness"]["all_pass"]
        assert [t["to"] for t in r["transitions"]] == [
            "PRESERVATION",
            "CONTAINED",
            "REPAIRING",
            "VERIFYING",
            "RECOVERED_LIMITED",
        ]


def test_nominal_consumes_two_pump_cycles_and_tracks_measured_inventory():
    request = synthetic_response(TEMPLATE)
    r = decide(request)
    assert r["plan"]["cycle_demand"] == 4
    assert r["controllability"]["safe_mode_count"] == 3
    assert r["controllability"]["unreachable_fraction"] < 1e-10
    for initial, used, remaining in zip(
        request["budget"]["resources"], request["response"]["consumed_resources"], r["resource_remaining"]
    ):
        assert remaining == pytest.approx(initial - used)


def test_rejected_plan_cannot_consume_an_inventory():
    r = deepcopy(CASES[0][1])
    r["frame"]["estop_closed"] = False
    result = decide(r)
    assert list(result["commands"].values()) == [0] * 4
    assert result["resource_remaining"] == r["budget"]["resources"]


def test_failed_post_response_verification_retains_consumption():
    by_name = {name: evidence for name, evidence, _ in CASES}

    single = deepcopy(by_name["heldout_model_inconsistent"])
    single_result = decide(single)
    assert single_result["state"] == "ISOLATED"
    assert "RESPONSE_MODEL_INCONSISTENT:V-leak_ratio" in single_result["reasons"]
    assert single_result["resource_remaining"][0] < single["budget"]["resources"][0]

    mixed = deepcopy(by_name["heldout_scenario_inconsistent"])
    assert all(c["lower"] <= c["value"] <= c["upper"] for c in mixed["verification_channels"])
    mixed_result = decide(mixed)
    assert mixed_result["state"] == "ISOLATED"
    assert "RESPONSE_SCENARIO_INCONSISTENT" in mixed_result["reasons"]
    assert not any(reason.startswith("RESPONSE_MODEL_INCONSISTENT:") for reason in mixed_result["reasons"])
    assert mixed_result["resource_remaining"][0] < mixed["budget"]["resources"][0]


def test_replay_survives_json_roundtrip():
    b = record(CASES[0][1])
    b = json.loads(json.dumps(b))
    assert audit(b, trusted_digest=b["sha256"])["passed"]

    # Optimizer diagnostics may vary across supported numerical platforms
    # without changing the authorized decision or safety evidence.
    b["result"]["plan"]["iterations"] += 1
    b["result"]["plan"]["solver_message"] = "platform-specific solver diagnostic"
    b["sha256"] = digest({k: v for k, v in b.items() if k != "sha256"})
    assert audit(b)["passed"]


@pytest.mark.parametrize("field", ["state", "physical_credit", "commands", "history", "controllability"])
def test_rehashed_result_tampering_still_fails_replay(field):
    b = record(CASES[0][1])
    b["result"][field] = "FORGED"
    b["sha256"] = digest({k: v for k, v in b.items() if k != "sha256"})
    assert not audit(b)["passed"]


def test_source_identity_is_required_for_audit():
    b = record(CASES[0][1])
    b["software"]["source_sha256"] = "0" * 64
    b["sha256"] = digest({k: v for k, v in b.items() if k != "sha256"})
    assert "SOFTWARE_IDENTITY" in audit(b)["errors"]


def test_external_trust_detects_fully_replaced_bundle():
    original = record(CASES[0][1])
    altered = deepcopy(CASES[0][1])
    altered["event_id"] = "OTHER"
    forged = record(altered)
    assert "TRUSTED_DIGEST_MISMATCH" in audit(forged, trusted_digest=original["sha256"])["errors"]


def test_duplicate_json_keys_rejected(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text('{"a":1,"a":2}')
    with pytest.raises(ValueError):
        load_json(p)


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_nonfinite_json_tokens_rejected(tmp_path, token):
    p = tmp_path / "bad.json"
    p.write_text('{"a":' + token + "}")
    with pytest.raises(ValueError):
        load_json(p)


@pytest.mark.parametrize(
    "mutation",
    [
        "units",
        "identity",
        "model_state",
        "nonfinite_arrival",
        "duplicate_fusion",
        "physical_basis",
        "wrong_boolean",
    ],
)
def test_malformed_evidence_cannot_produce_a_decision(mutation):
    r = deepcopy(CASES[0][1])
    if mutation == "units":
        r["planning_channels"][0]["unit"] = "mL"
    elif mutation == "identity":
        r["planning_channels"][1]["id"] = r["planning_channels"][0]["id"]
    elif mutation == "model_state":
        r["basis"]["state"][0] = 0.1
    elif mutation == "nonfinite_arrival":
        r["localization"]["arrivals"][0]["arrival_s"] = float("nan")
    elif mutation == "duplicate_fusion":
        r["fusion"]["channels"].append(r["fusion"]["channels"][0])
    elif mutation == "physical_basis":
        r["basis"]["evidence_class"] = "PHYSICAL"
    else:
        r["frame"]["estop_closed"] = "true"
    with pytest.raises(ValueError):
        decide(r)


def test_agent_conservation_independent_from_energy():
    assert agent_mass(50, 14, 35, 1, absolute_tolerance=0, relative_tolerance=0)["accepted"]
    assert not agent_mass(50, 14, 35, 0, absolute_tolerance=0, relative_tolerance=0)["accepted"]
    assert impact_energy(
        0.02, 100, {"thermal": 30, "deformation": 70}, absolute_tolerance=0, relative_tolerance=0
    )["accepted"]


@pytest.mark.parametrize("terms", [{"unexplained": 450.0}, {"impossible": 1500.0}])
def test_missing_or_created_energy_is_rejected(terms):
    assert not closure(1000, terms, absolute_tolerance=1, relative_tolerance=0.01)["accepted"]


def test_negative_ledger_sink_not_permitted():
    with pytest.raises(ValueError):
        closure(10, {"sink": -10}, absolute_tolerance=0, relative_tolerance=0)


def test_hazard_cycles_terminate_and_closed_barrier_blocks_reachability():
    edges = [
        {"from": "A", "to": "B", "kind": "leak", "delay_s": 1, "barrier": "V"},
        {"from": "B", "to": "A", "kind": "thermal", "delay_s": 1, "barrier": "T"},
    ]
    r = trace_hazards(["A", "B"], edges, "A", horizon_s=100)
    assert len(r["reachable"]) == 2
    r = trace_hazards(["A", "B"], edges, "A", horizon_s=100, closed_barriers=["V"])
    assert [r["node"] for r in r["reachable"]] == ["A"]


def test_state_cannot_skip_verification_or_restart_after_isolation():
    m = SurvivalMachine()
    with pytest.raises(ValueError):
        m.advance("held_out_pass")
    m.advance("stress")
    m.advance("plan_rejected")
    assert m.state == State.ISOLATED
    with pytest.raises(ValueError):
        m.advance("plan_accepted")


def test_reversible_phase_is_bounded_and_has_declared_hysteresis():
    params = {"on_threshold": 1.0, "off_threshold": 0.5, "response_time_s": 0.1, "dt_s": 0.1}
    p = protective_phase(0.0, 2.0, **params)["phase"]
    assert p == pytest.approx(1 - math.exp(-1))
    assert protective_phase(p, 0.75, **params)["phase"] == pytest.approx(p)
    assert protective_phase(p, 0.0, **params)["phase"] == pytest.approx(p * math.exp(-1))
    assert 0 < protective_phase(p, 2.0, **params)["phase"] < 1


def test_stack_mass_screen_gives_no_impact_credit():
    r = stack_screen(
        [{"role": "rearwall", "density_kg_m3": 1000, "thickness_m": 0.01, "status": "DESIGN_ONLY"}],
        max_areal_mass_kg_m2=9,
    )
    assert r["areal_mass_kg_m2"] == 10 and not r["mass_budget_pass"] and not r["physical_protection_credit"]


def test_cli_failure_exits_nonzero_and_emits_no_authority(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text('{"schema":"unknown"}')
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    proc = subprocess.run(
        [sys.executable, "-m", "ahis", "decide", str(p), "--out", str(tmp_path / "out.json")],
        env=env,
        text=True,
        capture_output=True,
    )
    assert proc.returncode == 1 and '"hardware_authority": false' in proc.stdout
    assert not (tmp_path / "out.json").exists()


def test_held_out_thresholds_cannot_be_relaxed():
    r = deepcopy(CASES[0][1])
    r["verification_channels"][0]["upper"] = 1.0
    with pytest.raises(ValueError):
        decide(r)


def test_measured_losses_are_removed_from_inventory():
    r = deepcopy(CASES[0][1])
    r["accounting"]["agent_a_g"]["terms"]["measured_loss"] = 1.0
    r["accounting"]["agent_a_g"]["terms"]["remaining"] -= 1.0
    result = decide(r)
    assert result["state"] == "RECOVERED_LIMITED" and result["inventory_verified"]
    assert result["resource_remaining"][0] == pytest.approx(
        r["budget"]["resources"][0] - r["response"]["consumed_resources"][0] - 1.0
    )


def test_nonboolean_claim_field_fails_audit_even_when_rehashed():
    b = record(CASES[0][1])
    b["result"]["physical_credit"] = 0
    b["sha256"] = digest({k: v for k, v in b.items() if k != "sha256"})
    assert not audit(b)["passed"]


@pytest.mark.parametrize("program_id", ["R" + str(i) for i in range(1, 11)])
def test_no_research_program_grants_credit_from_synthetic_records(program_id):
    from ahis.survival.research_programs import screen_record

    registry = load_json(ROOT / "configs/research_programs.json")
    program = next(p for p in registry["programs"] if p["id"] == program_id)
    record = {
        "program_id": program_id,
        "evidence_class": "SYNTHETIC",
        "specimen_id": "manufactured-fixture",
        "calibration_ids": ["synthetic"],
        "measurements": {},
        "test_groups": [],
        "reviewer": "test-harness",
        "raw_data_sha256": "0" * 64,
    }
    r = screen_record(program, record)
    assert not r["eligible_for_human_review"] and not r["physical_credit"]


def test_complete_research_record_is_only_eligible_for_human_review():
    from ahis.survival.research_programs import screen_record

    program = load_json(ROOT / "configs/research_programs.json")["programs"][5]
    r = {
        "program_id": "R6",
        "evidence_class": "PHYSICAL",
        "specimen_id": "manufactured-test-record",
        "calibration_ids": ["manufactured"],
        "reviewer": "test-harness",
        "raw_data_sha256": "0" * 64,
        "test_groups": program["required_test_groups"],
        "measurements": {
            k: {"value": 1.0, "lower": 0.0, "upper": 2.0, "unit": "test_unit"}
            for k in program["required_measurements"]
        },
    }
    result = screen_record(program, r)
    assert result["eligible_for_human_review"] and not result["physical_credit"]
