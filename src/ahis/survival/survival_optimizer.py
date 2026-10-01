"""Bounded joint resource optimization with independent post-solve constraint checks."""

import numpy as np
from scipy.optimize import minimize
from .numeric import finite, scalar
from .uncertainty import scenarios, campaign


def solve(basis, envelope, budget, uncertainty, *, margin=1e-5, max_iterations=300, protected=None):
    budget = finite(budget, (len(basis.resource_names),))
    margin = scalar(margin, lower=0, upper=0.1)
    if np.any(budget < 0) or type(max_iterations) is not int or not 1 <= max_iterations <= 10000:
        raise ValueError("invalid budget or iteration limit")
    rows = scenarios(uncertainty)
    c = np.empty((0, 4)) if protected is None else finite(protected)
    if c.ndim != 2 or c.shape[1] != 4:
        raise ValueError("invalid exact preservation matrix")
    active = np.flatnonzero(basis.upper > 0)
    zero = np.zeros(4)
    lo = envelope.lower + margin * envelope.scales
    hi = envelope.upper - margin * envelope.scales
    if np.any(lo >= hi):
        raise ValueError("margin empties survival envelope")

    def expand(x):
        u = zero.copy()
        u[active] = x * basis.upper[active]
        return u

    def constraints(x):
        u = expand(x)
        values = [(budget - basis.resources @ u) / np.maximum(budget, 1)]
        for _, gain, bias in rows:
            y = basis.predict(u, gain, bias)
            values.extend([(y - lo) / envelope.scales, (hi - y) / envelope.scales])
        return np.concatenate(values)

    if not len(active):
        x = np.zeros(0)
        success = bool(np.all(constraints(x) >= 0))
        message = "no surviving action"
        nit = 0
    else:
        result = minimize(
            lambda x: float(basis.cost @ expand(x)),
            np.zeros(len(active)),
            method="SLSQP",
            bounds=[(0, 1)] * len(active),
            constraints=[{"type": "ineq", "fun": constraints}]
            + ([{"type": "eq", "fun": lambda x: c @ expand(x)}] if len(c) else []),
            options={"maxiter": max_iterations, "ftol": 1e-11},
        )
        x, success, message, nit = result.x, bool(result.success), str(result.message), int(result.nit)
    u = expand(x)
    reasons = []
    if not success:
        reasons.append("SOLVER_DID_NOT_CONVERGE")
    if not np.all(np.isfinite(u)):
        reasons.append("NONFINITE_PROPOSAL")
        u = zero.copy()  # Never serialize a nonfinite proposal into evidence.
    robust = campaign(basis, envelope, u, uncertainty) if np.all(np.isfinite(u)) else None
    if robust is None or not robust["all_pass"]:
        reasons.append("SURVIVAL_ENVELOPE_UNSATISFIED")
    demand = basis.resources @ u
    if np.any(demand > budget + 1e-7):
        reasons.append("RESOURCE_LIMIT")
    if np.any(np.abs(c @ u) > 1e-7):
        reasons.append("EXACT_PRESERVATION_LIMIT")
    if np.any(u < -1e-9) or np.any(u > basis.upper + 1e-7):
        reasons.append("ACTION_BOUND")
    return {
        "accepted": not reasons,
        "proposal": u.tolist(),
        "authorized_command": u.tolist() if not reasons else [0.0] * 4,
        "resource_demand": demand.tolist(),
        "resource_remaining": (budget - demand).tolist() if not reasons else budget.tolist(),
        "objective": float(basis.cost @ u),
        "solver_success": success,
        "solver_message": message,
        "iterations": nit,
        "reasons": reasons,
        "robustness": robust,
        "hardware_authority": False,
        "optimality_scope": "LOCAL_CONSTRAINED_SOLUTION__NO_GLOBAL_OPTIMUM_CLAIM",
    }
