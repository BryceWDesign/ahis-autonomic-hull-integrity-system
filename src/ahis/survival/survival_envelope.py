"""Two-sided, unit-aware survival constraints supplied by the experiment policy."""

from dataclasses import dataclass
import numpy as np
from .numeric import finite


@dataclass(frozen=True)
class Envelope:
    names: tuple
    units: tuple
    lower: np.ndarray
    upper: np.ndarray
    scales: np.ndarray

    @classmethod
    def from_dict(cls, data):
        if set(data) != {"names", "units", "lower", "upper", "scales"}:
            raise ValueError("envelope fields disagree with schema")
        names, units = tuple(data["names"]), tuple(data["units"])
        n = len(names)
        lo, hi, scale = (finite(data[k], (n,)).copy() for k in ("lower", "upper", "scales"))
        if (
            not n
            or len(set(names)) != n
            or len(units) != n
            or any(not isinstance(v, str) or not v.strip() for v in names + units)
        ):
            raise ValueError("envelope identifiers/units must be unique and explicit")
        if np.any(lo >= hi) or np.any(scale <= 0):
            raise ValueError("invalid interval or normalization")
        return cls(names, units, lo, hi, scale)

    def violations(self, state, tolerance=1e-7):
        y = finite(state, self.upper.shape)
        return [
            name
            for i, name in enumerate(self.names)
            if y[i] < self.lower[i] - tolerance * self.scales[i]
            or y[i] > self.upper[i] + tolerance * self.scales[i]
        ]
