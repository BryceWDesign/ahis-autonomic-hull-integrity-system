"""Integrated raw-evidence-to-survival decision, with zero device dispatch capability."""

from dataclasses import asdict
import numpy as np
from ahis.hardware import SensorFrame, InterlockLimits, assess_interlocks
from ahis.fusion import EvidenceChannel, fuse_evidence
from ahis.localization_v3 import ArrivalObservation, AnisotropicPropagation, localize_anisotropic
from ahis.history import StructuralHistory
from . import AUTHORITY, SCHEMA
from .numeric import finite, scalar, digest
from .survival_envelope import Envelope
from .influence_basis import InfluenceBasis, COORDINATES, ACTIONS
from .controllability import decompose
from .survival_optimizer import solve
from .adaptive_state import SurvivalMachine
from .active_sensing import advise, arrival_jacobian
from .propagation import trace_hazards
from .accounting import closure
from .independent_verify import verify
from .protection_stack import stack_screen, protective_phase, rank_architectures


def decide(request):
    required = {
        "schema",
        "event_id",
        "timestamp_utc",
        "frame",
        "interlock_limits",
        "localization",
        "fusion",
        "planning_channels",
        "basis",
        "envelope",
        "budget",
        "uncertainty",
        "exact_protected_matrix",
        "optimizer",
        "sensing",
        "propagation",
        "containment_confirmed",
        "verification_channels",
        "accounting",
        "protection",
        "response",
        "calibration_identities",
    }
    if set(request) != required or request["schema"] != SCHEMA:
        raise ValueError("unsupported or incomplete survival request schema")
    if (
        not request["event_id"]
        or not request["timestamp_utc"]
        or type(request["containment_confirmed"]) is not bool
    ):
        raise ValueError("event/containment identity invalid")
    calibration = request["calibration_identities"]
    if (
        set(calibration)
        != {"evidence_class", "localization", "influence", "mass_density", "measurement_noise"}
        or calibration["evidence_class"] != "SYNTHETIC"
    ):
        raise ValueError("reference calibration identities must be explicit and synthetic")
    if any(not isinstance(v, str) or not v.strip() for v in calibration.values()):
        raise ValueError("calibration identity missing")
    if calibration["influence"] != request["basis"]["id"]:
        raise ValueError("influence calibration identity mismatch")
    basis = InfluenceBasis(request["basis"])
    envelope = Envelope.from_dict(request["envelope"])
    if envelope.names != COORDINATES or envelope.units != ("ratio", "ratio", "degC", "ratio"):
        raise ValueError("reference coordinates/units mismatch")
    budget = request["budget"]
    if (
        set(budget) != {"resources", "cycles_remaining"}
        or type(budget["cycles_remaining"]) is not int
        or budget["cycles_remaining"] < 0
    ):
        raise ValueError("invalid resource budget")
    if basis.resource_names != ("agent_a_ml", "agent_b_ml", "electrical_j"):
        raise ValueError("reference resource units/order mismatch")
    resources = finite(budget["resources"], (len(basis.resource_names),))
    if np.any(resources < 0):
        raise ValueError("negative resource inventory")
    channels = request["planning_channels"]
    if len(channels) != 4:
        raise ValueError("four declared state channels required")
    ids = []
    groups = []
    state = []
    for index, c in enumerate(channels):
        if (
            set(c) != {"id", "group", "coordinate", "unit", "value", "healthy"}
            or type(c["healthy"]) is not bool
            or not c["id"]
            or not c["group"]
        ):
            raise ValueError("invalid planning channel")
        if c["coordinate"] != COORDINATES[index] or c["unit"] != envelope.units[index]:
            raise ValueError("planning channel unit/order mismatch")
        ids.append(c["id"])
        groups.append(c["group"])
        state.append(scalar(c["value"]))
    if len(set(ids)) != 4 or not np.array_equal(state, basis.state):
        raise ValueError("duplicate planning identity or model state not derived from raw channels")
    loc = request["localization"]
    observations = [ArrivalObservation(**c) for c in loc["arrivals"]]
    if len({o.sensor_id for o in observations}) != len(observations):
        raise ValueError("duplicate arrival sensor")
    for o in observations:
        finite([o.x_m, o.y_m, o.arrival_s, o.quality])
    if type(loc["grid_points"]) is not int or not 9 <= loc["grid_points"] <= 501:
        raise ValueError("localization grid outside reference bounds")
    scalar(loc["max_rms_s"], lower=1e-15)
    finite(loc["bounds_m"], (4,))
    model = AnisotropicPropagation(**loc["model"])
    finite(list(loc["model"].values()))
    localization = localize_anisotropic(
        observations,
        model=model,
        bounds_m=tuple(loc["bounds_m"]),
        grid_points_per_axis=loc["grid_points"],
        max_weighted_rms_s=loc["max_rms_s"],
    )
    fusion_rows = request["fusion"]["channels"]
    if len({c["name"] for c in fusion_rows}) != len(fusion_rows):
        raise ValueError("duplicate fusion identity")
    fusion = fuse_evidence(
        [EvidenceChannel(**c) for c in fusion_rows],
        threshold=request["fusion"]["threshold"],
        min_effective_weight=request["fusion"]["minimum_weight"],
    )
    frame = request["frame"]
    if any(type(frame[k]) is not bool for k in ("estop_closed", "sensor_valid")):
        raise ValueError("invalid hardware boolean")
    for x in request["interlock_limits"].values():
        scalar(x, lower=0)
    interlock = assess_interlocks(SensorFrame(**frame), InterlockLimits(**request["interlock_limits"]))
    protected = finite(request["exact_protected_matrix"])
    if protected.size == 0:
        protected = np.empty((0, 4))
    if protected.ndim != 2 or protected.shape[1] != 4:
        raise ValueError("invalid exact preservation matrix")
    residual = np.maximum(basis.state - envelope.upper, 0) + np.minimum(basis.state - envelope.lower, 0)
    objective_mask = np.abs(residual) > 1e-14
    actuator_mask = basis.upper > 0
    authority = decompose(
        basis.jacobian()[objective_mask][:, actuator_mask],
        residual[objective_mask],
        scales=envelope.scales[objective_mask],
        protected=protected[:, actuator_mask],
    )
    authority["assessed_objectives"] = [name for name, active in zip(COORDINATES, objective_mask) if active]
    authority["available_actions"] = [name for name, active in zip(ACTIONS, actuator_mask) if active]
    sensing = request["sensing"]
    prior = finite(sensing["prior_information"], (3, 3))
    advise(prior, [])  # Validate the prior before adding any observation information.
    sigma = scalar(sensing["timing_noise_std_s"], lower=1e-15)
    # A failed localization cannot provide a credible measurement-selection location.
    advisor = {"recommended": None, "ranking": [], "hardware_authority": False}
    if localization.accepted:
        position = [localization.x_m, localization.y_m]
        information = prior.copy()
        for o in observations:
            if o.quality > 0:
                gradient = finite(arrival_jacobian(position, [o.x_m, o.y_m], model), (3,))
                information += o.quality * np.outer(gradient, gradient) / (sigma * sigma)
        candidates = []
        for c in sensing["candidates"]:
            if set(c) != {"id", "x_m", "y_m", "healthy", "hardware_present", "noise_std"}:
                raise ValueError("invalid sensing geometry")
            candidates.append(
                {k: c[k] for k in ("id", "healthy", "hardware_present", "noise_std")}
                | {"jacobian": arrival_jacobian(position, [c["x_m"], c["y_m"]], model)}
            )
        advisor = advise(information, candidates, used_ids=ids + [o.sensor_id for o in observations])
    propagation = request["propagation"]
    before = trace_hazards(
        propagation["nodes"], propagation["edges"], propagation["origin"], horizon_s=propagation["horizon_s"]
    )
    after = trace_hazards(
        propagation["nodes"],
        propagation["edges"],
        propagation["origin"],
        horizon_s=propagation["horizon_s"],
        closed_barriers=propagation["closed_barriers"] if request["containment_confirmed"] else (),
    )
    critical = set(propagation["critical_nodes"])
    if not critical.issubset(propagation["nodes"]):
        raise ValueError("unknown critical hazard node")
    threatened = critical.intersection(r["node"] for r in after["reachable"])
    protection = request["protection"]
    protection_result = {
        "stack": stack_screen(**protection["stack"]),
        "adaptive_phase": protective_phase(**protection["adaptive_phase"]),
        "architectures": rank_architectures(**protection["architectures"]),
    }
    heldout = request["verification_channels"]
    if len(heldout) != 4:
        raise ValueError("four held-out state channels required")
    for i, c in enumerate(heldout):
        if c.get("coordinate") != COORDINATES[i] or c.get("unit") != envelope.units[i]:
            raise ValueError("held-out coordinate/unit mismatch")
        if (
            c.get("required") is not True
            or c.get("lower") != envelope.lower[i]
            or c.get("upper") != envelope.upper[i]
        ):
            raise ValueError("held-out channel must use the declared survival policy limits")
    accounts = {name: closure(**data) for name, data in request["accounting"].items()}
    if set(accounts) != {"agent_a_g", "agent_b_g", "electrical_j", "impact_j"}:
        raise ValueError("all four conservation accounts required")
    response = request["response"]
    if set(response) != {"executed_command", "consumed_resources", "agent_density_g_ml"}:
        raise ValueError("invalid response evidence")
    executed = finite(response["executed_command"], (4,))
    consumed = finite(response["consumed_resources"], resources.shape)
    density = finite(response["agent_density_g_ml"], (2,))
    for i, key in enumerate(("agent_a_g", "agent_b_g", "electrical_j")):
        sinks = {"delivered" if i < 2 else "consumed", "remaining", "measured_loss"}
        if set(accounts[key]["terms"]) != sinks:
            raise ValueError("resource ledger sink schema mismatch")
    losses = np.array(
        [
            accounts[k]["terms"]["measured_loss"] / (density[i] if i < 2 else 1.0)
            for i, k in enumerate(("agent_a_g", "agent_b_g", "electrical_j"))
        ]
    )
    if np.any(consumed < 0) or np.any(density <= 0):
        raise ValueError("invalid measured consumption/density")
    machine = SurvivalMachine()
    machine.advance("stress")
    plan = None
    verification = None
    reasons = []
    commands = [0.0] * 4
    if not interlock.allowed:
        reasons.extend(interlock.reasons)
        machine.advance("interlock_denied")
    elif not localization.accepted or not fusion.accepted or not all(c["healthy"] for c in channels):
        reasons.append("DAMAGE_EVIDENCE_INSUFFICIENT")
        machine.advance("evidence_failed")
    elif not request["containment_confirmed"] or threatened:
        reasons.append("CONTAINMENT_NOT_ESTABLISHED")
        machine.advance("evidence_failed")
    else:
        machine.advance("containment_confirmed")
        plan = solve(
            basis, envelope, resources, request["uncertainty"], protected=protected, **request["optimizer"]
        )
        cycle_demand = int(np.count_nonzero(np.array(plan["proposal"]) > 1e-7))
        # Paired pumps consume two physical actuator cycles, not one.
        if plan["proposal"][0] > 1e-7:
            cycle_demand += 1
        plan["cycle_demand"] = cycle_demand
        if cycle_demand > budget["cycles_remaining"]:
            plan["accepted"] = False
            plan["reasons"].append("ACTUATOR_CYCLE_LIMIT")
        if not plan["accepted"]:
            plan["authorized_command"] = [0.0] * 4
            plan["resource_remaining"] = resources.tolist()
            reasons.extend(plan["reasons"])
            machine.advance("plan_rejected")
        else:
            machine.advance("plan_accepted")
            commands = plan["authorized_command"]
            machine.advance("response_recorded")
            verification = verify(
                [{k: v for k, v in c.items() if k not in {"coordinate", "unit"}} for c in heldout],
                planning_ids=ids + [o.sensor_id for o in observations] + [r["name"] for r in fusion_rows],
                planning_groups=groups + ["arrival_bus", "fusion_bus"],
            )
            response_errors = []
            if not np.allclose(executed, commands, rtol=1e-6, atol=1e-7):
                response_errors.append("EXECUTED_COMMAND_MISMATCH")
            if np.any(consumed + losses > resources + 1e-7):
                response_errors.append("MEASURED_RESOURCE_OVERDRAW")
            for i, key in enumerate(("agent_a_g", "agent_b_g", "electrical_j")):
                scale = density[i] if i < 2 else 1.0
                row = accounts[key]
                if abs(row["incoming"] - resources[i] * scale) > 1e-6:
                    response_errors.append("ACCOUNT_INITIAL_INVENTORY:" + key)
                sink = "delivered" if i < 2 else "consumed"
                if sink not in row["terms"] or abs(row["terms"][sink] - consumed[i] * scale) > 1e-6:
                    response_errors.append("ACCOUNT_MEASURED_CONSUMPTION:" + key)
            if response_errors:
                reasons.extend(response_errors)
                machine.advance("evidence_failed")
            elif not all(a["accepted"] for a in accounts.values()):
                reasons.append("CONSERVATION_ACCOUNTING_FAILED")
                machine.advance("accounting_failed")
            elif not verification["passed"]:
                reasons.extend(verification["reasons"])
                machine.advance("verification_failed")
            else:
                machine.advance("held_out_pass")
    history = StructuralHistory()
    history.append(
        "raw_evidence",
        request["timestamp_utc"],
        {"event_id": request["event_id"], "request_digest": digest(request)},
    )
    for t in machine.history:
        history.append("survival_transition", request["timestamp_utc"], t)
    history.append("verdict", request["timestamp_utc"], {"state": machine.state.value, "reasons": reasons})
    return {
        "schema": SCHEMA,
        "authority": AUTHORITY,
        "state": machine.state.value,
        "reasons": reasons,
        "localization": asdict(localization),
        "fusion": asdict(fusion),
        "interlock": asdict(interlock),
        "controllability": authority,
        "sensing": advisor,
        "propagation_before": before,
        "propagation_after": after,
        "protection": protection_result,
        "plan": plan,
        "verification": verification,
        "accounting": accounts,
        "commands": dict(zip(ACTIONS, commands)),
        "resource_remaining": np.maximum(resources - consumed - losses, 0).tolist()
        if plan and plan["accepted"]
        else resources.tolist(),
        "inventory_verified": bool(
            plan
            and plan["accepted"]
            and all(a["accepted"] for a in accounts.values())
            and not any(r.startswith(("ACCOUNT_", "MEASURED_")) for r in reasons)
        ),
        "next_repair_allowed": False,
        "cycles_remaining": budget["cycles_remaining"]
        - (plan["cycle_demand"] if plan and plan["accepted"] else 0),
        "transitions": machine.history,
        "history": history.as_records(),
        "hardware_authority": False,
        "physical_credit": False,
        "return_to_service_allowed": False,
    }
