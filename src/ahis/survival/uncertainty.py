"""Finite declared uncertainty set, evaluated without reoptimizing commands."""

import numpy as np
from .numeric import finite


def scenarios(rows):
    if not rows or len(rows) > 256:
        raise ValueError("uncertainty set must contain 1 to 256 scenarios")
    ids = []
    result = []
    for row in rows:
        if set(row) != {"id", "gain", "bias"} or not isinstance(row["id"], str) or not row["id"].strip():
            raise ValueError("invalid uncertainty scenario")
        gain, bias = finite(row["gain"], (4,)), finite(row["bias"], (4,))
        if np.any(gain <= 0) or np.any(gain > 2):
            raise ValueError("gain outside synthetic model domain")
        ids.append(row["id"])
        result.append((row["id"], gain, bias))
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate uncertainty scenario")
    return result


def campaign(basis, envelope, command, rows):
    results = []
    for name, gain, bias in scenarios(rows):
        y = basis.predict(command, gain, bias)
        results.append({"id": name, "state": y.tolist(), "violations": envelope.violations(y)})
    return {
        "all_pass": all(not r["violations"] for r in results),
        "scenarios": results,
        "scope": "DECLARED_FINITE_SET_ONLY",
        "fixed_command": finite(command).tolist(),
    }


def response_bounds(basis, command, rows):
    """Expected response band for one executed command over the declared finite uncertainty set.

    This is model consistency only. It does not include a physical sensor-noise model.
    """
    states = []
    scenario_ids = []
    for name, gain, bias in scenarios(rows):
        states.append(basis.predict(command, gain, bias))
        scenario_ids.append(name)
    matrix = np.vstack(states)
    return {
        "lower": np.min(matrix, axis=0).tolist(),
        "upper": np.max(matrix, axis=0).tolist(),
        "scenario_ids": scenario_ids,
        "scope": "DECLARED_FINITE_SET_ONLY",
        "measurement_noise_included": False,
    }
