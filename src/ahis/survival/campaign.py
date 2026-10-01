"""End-to-end manufactured HIL cases and adversarial negative controls.

A surrogate independently generates observations after planning. These observations
are manufactured, not physical measurements or an independent physics model.
"""

from copy import deepcopy
from pathlib import Path
import numpy as np
from .influence_basis import InfluenceBasis, COORDINATES
from .survival_envelope import Envelope
from .survival_optimizer import solve
from .numeric import write_json, digest
from .replay_audit import record, audit
from . import AUTHORITY


def synthetic_response(template, *, gain=None, bias=None):
    r = deepcopy(template)
    basis = InfluenceBasis(r["basis"])
    envelope = Envelope.from_dict(r["envelope"])
    protected = r["exact_protected_matrix"] or None
    plan = solve(
        basis, envelope, r["budget"]["resources"], r["uncertainty"], protected=protected, **r["optimizer"]
    )
    u = plan["authorized_command"]
    y = basis.predict(u, gain, bias)
    consumed = basis.resources @ np.array(u)
    r["response"]["executed_command"] = u
    r["response"]["consumed_resources"] = consumed.tolist()
    r["verification_channels"] = [
        {
            "id": "V-" + name,
            "coordinate": name,
            "unit": envelope.units[i],
            "group": "heldout-" + name,
            "value": float(value),
            "lower": float(lo),
            "upper": float(hi),
            "healthy": True,
            "required": True,
        }
        for i, (name, value, lo, hi) in enumerate(zip(COORDINATES, y, envelope.lower, envelope.upper))
    ]
    accounts = {}
    for i, name in enumerate(("agent_a_g", "agent_b_g", "electrical_j")):
        scale = r["response"]["agent_density_g_ml"][i] if i < 2 else 1.0
        initial = r["budget"]["resources"][i] * scale
        used = float(consumed[i] * scale)
        terms = {
            "delivered" if i < 2 else "consumed": used,
            "remaining": initial - used,
            "measured_loss": 0.0,
        }
        accounts[name] = {
            "incoming": initial,
            "terms": terms,
            "absolute_tolerance": 1e-6,
            "relative_tolerance": 1e-6,
        }
    accounts["impact_j"] = {
        "incoming": 1000.0,
        "terms": {
            "bumper_deformation": 200.0,
            "thermal": 150.0,
            "fracture": 250.0,
            "transmitted": 300.0,
            "residual_debris": 100.0,
        },
        "absolute_tolerance": 1.0,
        "relative_tolerance": 0.001,
    }
    r["accounting"] = accounts
    return r


def cases(template):
    base = synthetic_response(template)
    rows = [("nominal", base, "RECOVERED_LIMITED")]

    def add(name, change, state="ISOLATED", source=None):
        r = deepcopy(base if source is None else source)
        r["event_id"] = name
        change(r)
        for i, c in enumerate(r["verification_channels"]):
            c["lower"] = r["envelope"]["lower"][i]
            c["upper"] = r["envelope"]["upper"][i]
        rows.append((name, r, state))

    add("estop_open", lambda r: r["frame"].update(estop_closed=False))
    add("overpressure", lambda r: r["frame"].update(pressure_kpa=9.0))
    add("planning_sensor_failed", lambda r: r["planning_channels"][0].update(healthy=False))
    add("arrival_network_failed", lambda r: [c.update(quality=0.0) for c in r["localization"]["arrivals"]])
    add("fusion_insufficient", lambda r: [c.update(quality=0.1) for c in r["fusion"]["channels"]])
    add("containment_unconfirmed", lambda r: r.update(containment_confirmed=False))
    add("barrier_failure", lambda r: r["propagation"].update(closed_barriers=[]))
    add("seal_actuator_lost", lambda r: r["basis"]["available"].__setitem__(0, False))
    add("damping_actuator_lost", lambda r: r["basis"]["available"].__setitem__(1, False))
    add("all_actuators_lost", lambda r: r["basis"].update(available=[False] * 4))
    add("agent_depleted", lambda r: r["budget"].update(resources=[2.0, 2.0, 500.0]))
    add("electrical_depleted", lambda r: r["budget"].update(resources=[50.0, 50.0, 10.0]))
    add("cycles_depleted", lambda r: r["budget"].update(cycles_remaining=1))
    add("no_safe_heater", lambda r: r["envelope"]["upper"].__setitem__(2, 26.0))
    add("exact_lock_blocks_repair", lambda r: r.update(exact_protected_matrix=[[0.0, 0.0, 1.0, 0.0]]))
    add(
        "robustness_failure",
        lambda r: r["uncertainty"].append(
            {"id": "severely_weak", "gain": [0.4] * 4, "bias": [0.05, 0.1, 5.0, 0.05]}
        ),
    )
    add("solver_iteration_limit", lambda r: r["optimizer"].update(max_iterations=1))
    add("heldout_failed", lambda r: r["verification_channels"][0].update(value=0.8))
    add("heldout_unavailable", lambda r: r["verification_channels"][0].update(healthy=False))
    add(
        "heldout_reuses_planning_sensor",
        lambda r: r["verification_channels"][0].update(id=r["planning_channels"][0]["id"]),
    )
    add(
        "heldout_reuses_acquisition_group",
        lambda r: r["verification_channels"][0].update(group=r["planning_channels"][0]["group"]),
    )
    add("mass_nonclosure", lambda r: r["accounting"]["agent_a_g"]["terms"].update(remaining=0.0))
    add("energy_nonclosure", lambda r: r["accounting"]["impact_j"]["terms"].update(transmitted=0.0))
    add("executed_command_mismatch", lambda r: r["response"]["executed_command"].__setitem__(0, 1.0))
    add("consumption_mismatch", lambda r: r["response"]["consumed_resources"].__setitem__(0, 1.0))
    add("resource_overdraw", lambda r: r["response"]["consumed_resources"].__setitem__(0, 100.0))
    # Available isolation can substitute for a lost sealing actuator in this toy model.
    alternative = deepcopy(template)
    alternative["basis"]["available"] = [False, True, True, True]
    rows.append(("isolation_substitutes_for_seal", synthetic_response(alternative), "RECOVERED_LIMITED"))
    rows.append(
        (
            "heldout_weak_response",
            synthetic_response(template, gain=[0.9] * 4, bias=[0.005, 0.005, 1.0, 0.005]),
            "RECOVERED_LIMITED",
        )
    )
    return rows


def run_campaign(template, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    result = []
    for name, r, expected in cases(template):
        bundle = record(r)
        verdict = audit(bundle)
        write_json(out / (name + ".json"), bundle)
        state = bundle["result"]["state"]
        result.append(
            {
                "case": name,
                "expected": expected,
                "actual": state,
                "passed": state == expected and verdict["passed"],
                "audit_pass": verdict["passed"],
                "digest": bundle["sha256"],
                "reasons": bundle["result"]["reasons"],
            }
        )
    tampered = deepcopy(bundle)
    tampered["result"]["physical_credit"] = True
    tamper_rejected = not audit(tampered)["passed"]
    # Rehashing an altered decision must still fail recomputation.
    tampered["sha256"] = digest({k: v for k, v in tampered.items() if k != "sha256"})
    rehash_rejected = not audit(tampered)["passed"]
    summary = {
        "authority": AUTHORITY,
        "cases": result,
        "tamper_rejected": tamper_rejected,
        "rehash_rejected": rehash_rejected,
        "all_pass": all(r["passed"] for r in result) and tamper_rejected and rehash_rejected,
        "physical_credit": False,
    }
    write_json(out / "campaign.json", summary)
    return summary
