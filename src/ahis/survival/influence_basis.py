"""Explicit synthetic influence basis linked to legacy AHIS leak and modal models.

No empirical calibration is inferred. All actions are proposals in native units.
"""

import numpy as np
from ahis.hardware import HILRig
from ahis.control import resonant_transmissibility
from .numeric import finite, scalar

COORDINATES = ("leak_ratio", "vibration_ratio", "temperature_c", "strain_ratio")
ACTIONS = ("paired_agent_ml", "damping_delta_zeta", "heater_fraction", "isolation_fraction")


class InfluenceBasis:
    def __init__(self, data):
        required = {
            "id",
            "evidence_class",
            "state",
            "available",
            "upper",
            "resource_names",
            "resource_matrix",
            "cost",
            "response_scale_ml",
            "baseline_zeta",
        }
        if set(data) != required or data["evidence_class"] != "SYNTHETIC" or not str(data["id"]).strip():
            raise ValueError("only an identified SYNTHETIC reference basis is executable")
        self.data = data
        self.state = finite(data["state"], (4,)).copy()
        if np.any(self.state[[0, 1, 3]] < 0):
            raise ValueError("negative normalized damage magnitude")
        if len(data["available"]) != 4 or any(type(v) is not bool for v in data["available"]):
            raise ValueError("availability must contain four booleans")
        self.available = np.array(data["available"], dtype=bool)
        self.upper = finite(data["upper"], (4,)).copy()
        if np.any(self.upper < 0) or self.upper[1] >= 0.8 or np.any(self.upper[2:] > 1):
            raise ValueError("invalid action bounds")
        self.upper[~self.available] = 0
        self.resource_names = tuple(data["resource_names"])
        if len(set(self.resource_names)) != len(self.resource_names) or any(
            not isinstance(v, str) or not v.strip() for v in self.resource_names
        ):
            raise ValueError("invalid resource identifiers")
        self.resources = finite(data["resource_matrix"], (len(self.resource_names), 4))
        self.cost = finite(data["cost"], (4,))
        if np.any(self.resources < 0) or np.any(self.cost <= 0):
            raise ValueError("resource/cost coefficients invalid")
        self.scale = scalar(data["response_scale_ml"], lower=1e-9)
        self.zeta = scalar(data["baseline_zeta"], lower=1e-6, upper=0.19)
        if self.zeta + self.upper[1] >= 1:
            raise ValueError("damping bound outside legacy model")

    def predict(self, command, gain=None, bias=None):
        u = finite(command, (4,))
        g = np.ones(4) if gain is None else finite(gain, (4,))
        b = np.zeros(4) if bias is None else finite(bias, (4,))
        if np.any(g <= 0) or np.any(g > 2) or np.any(u < -1e-9) or np.any(u > self.upper + 1e-7):
            raise ValueError("command or actuator gain outside reference domain")
        a = u * g
        # Paired coordinate consumes this volume in EACH reservoir.
        rig = HILRig(initial_leak_ml_min=self.state[0], response_scale_ml=self.scale)
        leak = rig.frame(0, a[0], a[0]).leak_ml_min * (1 - 0.9 * a[3])
        vib = (
            self.state[1] * resonant_transmissibility(self.zeta + a[1]) / resonant_transmissibility(self.zeta)
        )
        return np.array([leak, vib, self.state[2] + 30 * a[2] + 8 * a[1], self.state[3] - 0.6 * a[2]]) + b

    def jacobian(self):
        y0 = self.predict(np.zeros(4))
        j = np.zeros((4, 4))
        for k in range(4):
            if self.upper[k] > 0:
                h = min(self.upper[k], max(1e-7, self.upper[k] * 1e-5))
                u = np.zeros(4)
                u[k] = h
                j[:, k] = (self.predict(u) - y0) / h
        return j
