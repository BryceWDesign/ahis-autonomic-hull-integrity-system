"""Finite numerical inputs and strict, portable evidence encoding."""

import hashlib
import json
import numpy as np


def finite(value, shape=None):
    a = np.asarray(value, dtype=float)
    if not np.all(np.isfinite(a)) or (shape is not None and a.shape != shape):
        raise ValueError("nonfinite input or dimension mismatch")
    return a


def scalar(value, *, lower=None, upper=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("numeric scalar required")
    x = float(value)
    if not np.isfinite(x) or (lower is not None and x < lower) or (upper is not None and x > upper):
        raise ValueError("scalar outside finite allowed range")
    return x


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def load_json(path):
    def reject(value):
        raise ValueError("nonfinite JSON token: " + value)

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs, parse_constant=reject)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8"))
