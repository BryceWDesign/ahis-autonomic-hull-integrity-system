"""Layer bookkeeping and low-order engineering screens, no ballistic protection claim."""

import math
from .numeric import scalar


def stack_screen(layers, *, max_areal_mass_kg_m2):
    cap = scalar(max_areal_mass_kg_m2, lower=0)
    roles = [r["role"] for r in layers]
    if len(set(roles)) != len(roles) or not layers:
        raise ValueError("unique stack roles required")
    mass = 0.0
    for r in layers:
        if set(r) != {"role", "density_kg_m3", "thickness_m", "status"} or r["status"] != "DESIGN_ONLY":
            raise ValueError("stack layers must be design-only")
        mass += scalar(r["density_kg_m3"], lower=0) * scalar(r["thickness_m"], lower=0)
    return {
        "areal_mass_kg_m2": mass,
        "mass_budget_pass": mass <= cap,
        "layer_roles": roles,
        "physical_protection_credit": False,
        "hypervelocity_model_implemented": False,
    }


def protective_phase(phase, stress, *, on_threshold, off_threshold, response_time_s, dt_s):
    phase = scalar(phase, lower=0, upper=1)
    stress = scalar(stress, lower=0)
    on = scalar(on_threshold, lower=0)
    off = scalar(off_threshold, lower=0)
    tau = scalar(response_time_s, lower=1e-12)
    dt = scalar(dt_s, lower=0)
    if off >= on:
        raise ValueError("hysteresis thresholds invalid")
    target = 1.0 if stress >= on else (0.0 if stress <= off else phase)
    return {
        "phase": target + (phase - target) * math.exp(-dt / tau),
        "scope": "PHENOMENOLOGICAL_SCREEN_ONLY",
        "physical_credit": False,
    }


def rank_architectures(candidates, *, mass_cap, minimum_stiffness):
    mass_cap = scalar(mass_cap, lower=0)
    minimum_stiffness = scalar(minimum_stiffness, lower=0)
    rows = []
    ids = [c["id"] for c in candidates]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate architecture candidate")
    for c in candidates:
        mass = scalar(c["areal_mass_kg_m2"], lower=0)
        stiffness = scalar(c["relative_stiffness"], lower=0)
        utility = scalar(c["declared_utility"], lower=0)
        rows.append(
            {
                "id": c["id"],
                "eligible": mass <= mass_cap and stiffness >= minimum_stiffness,
                "declared_utility": utility,
                "physical_credit": False,
            }
        )
    rows.sort(key=lambda r: (not r["eligible"], -r["declared_utility"], r["id"]))
    return {"ranking": rows, "scope": "SUPPLIED_SURROGATE_CO_DESIGN__NOT_MATERIAL_DISCOVERY"}
