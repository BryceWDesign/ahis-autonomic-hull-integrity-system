"""Scaled local authority decomposition, independently expressed from SVD mathematics.

The result is a tangent-space diagnostic, never proof of bounded nonlinear feasibility.
"""

import numpy as np
from .numeric import finite, scalar


def safe_modes(protected_jacobian, actuator_count, rtol=1e-8):
    rtol = scalar(rtol, lower=1e-15, upper=0.1)
    c = finite(protected_jacobian)
    if c.ndim != 2 or c.shape[1] != actuator_count:
        raise ValueError("protected/actuator dimension mismatch")
    if c.shape[0] == 0:
        return np.eye(actuator_count), 0
    _, s, vh = np.linalg.svd(c, full_matrices=True)
    cutoff = s[0] * rtol if len(s) else 0
    rank = int(np.count_nonzero(s > cutoff))
    return vh[rank:].T, rank


def decompose(jacobian, residual, *, scales, protected=None, rtol=1e-8):
    j, r, scale = finite(jacobian), finite(residual), finite(scales)
    rtol = scalar(rtol, lower=1e-15, upper=0.1)
    if j.ndim != 2 or r.shape != (j.shape[0],) or scale.shape != r.shape or np.any(scale <= 0):
        raise ValueError("invalid scaled authority problem")
    z, lock_rank = safe_modes(np.empty((0, j.shape[1])) if protected is None else protected, j.shape[1], rtol)
    a = (j / scale[:, None]) @ z
    b = r / scale
    u, s, _ = np.linalg.svd(a, full_matrices=False)
    rank = int(np.count_nonzero(s > (s[0] * rtol if len(s) else 0)))
    reachable = u[:, :rank] @ (u[:, :rank].T @ b)
    unreachable = b - reachable
    norm = np.linalg.norm(b)
    return {
        "rank": rank,
        "protected_rank": lock_rank,
        "safe_mode_count": z.shape[1],
        "singular_values": s.tolist(),
        "reachable_scaled": reachable.tolist(),
        "unreachable_scaled": unreachable.tolist(),
        "unreachable_fraction": float(np.linalg.norm(unreachable) / norm) if norm > 1e-14 else 0.0,
        "scope": "LOCAL_LINEAR_UNBOUNDED_DIAGNOSTIC",
    }
