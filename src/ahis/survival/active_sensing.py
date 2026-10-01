"""D-optimal advisory over surviving sensors; no invented replacement hardware."""

import numpy as np
from .numeric import finite, scalar


def arrival_jacobian(position, sensor, model, step=1e-5):
    p, s = finite(position, (2,)), finite(sensor, (2,))

    def travel(x):
        d = x - s
        return np.linalg.norm(d) / model.speed(*d)

    gradient = []
    for k in range(2):
        delta = np.zeros(2)
        delta[k] = step
        gradient.append((travel(p + delta) - travel(p - delta)) / (2 * step))
    return [*gradient, 1.0]  # event time is an estimated nuisance parameter


def advise(information, candidates, *, used_ids=()):
    info = finite(information)
    if (
        info.ndim != 2
        or info.shape[0] != info.shape[1]
        or not np.allclose(info, info.T, rtol=1e-10, atol=1e-12)
    ):
        raise ValueError("information matrix must be symmetric")
    try:
        np.linalg.cholesky(info)
    except np.linalg.LinAlgError as exc:
        raise ValueError("information matrix must be positive definite") from exc
    ids = [r["id"] for r in candidates]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate sensing candidate")
    ranked = []
    for row in candidates:
        if (
            set(row) != {"id", "healthy", "jacobian", "noise_std", "hardware_present"}
            or type(row["healthy"]) is not bool
            or type(row["hardware_present"]) is not bool
        ):
            raise ValueError("invalid sensing candidate")
        a = finite(row["jacobian"], (info.shape[0],)) / scalar(row["noise_std"], lower=1e-15)
        if not row["healthy"] or not row["hardware_present"] or row["id"] in used_ids:
            continue
        gain = float(np.log1p(a @ np.linalg.solve(info, a)))
        ranked.append(
            {"id": row["id"], "logdet_gain": gain, "covariance_determinant_ratio": float(np.exp(-gain))}
        )
    ranked.sort(key=lambda r: (-r["logdet_gain"], r["id"]))
    return {
        "recommended": ranked[0]["id"] if ranked else None,
        "ranking": ranked,
        "hardware_authority": False,
    }
