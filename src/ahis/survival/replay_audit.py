"""Input/source binding plus recomputation of the entire archived decision.

SHA-256 is tamper evidence relative to a trusted external digest, not authentication.
Cross-platform scientific values use a declared tolerance; byte integrity is exact.
"""

import hashlib
import importlib.metadata
from pathlib import Path
from . import SCHEMA, AUTHORITY
from .numeric import digest
from .controller import decide


def software_identity():
    root = Path(__file__).resolve().parents[1]
    files = {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*.py"))
    }
    return {
        "source_sha256": digest(files),
        "files": files,
        "dependencies": {k: importlib.metadata.version(k) for k in ("numpy", "scipy")},
    }


def record(request):
    bundle = {
        "schema": SCHEMA,
        "authority": AUTHORITY,
        "software": software_identity(),
        "request": request,
        "result": decide(request),
    }
    bundle["sha256"] = digest(bundle)
    return bundle


NON_AUTHORITATIVE_REPLAY_PATHS = {"result.plan.iterations", "result.plan.solver_message"}


def differences(a, b, path="result"):
    if path in NON_AUTHORITATIVE_REPLAY_PATHS:
        return []
    if isinstance(a, dict) and isinstance(b, dict):
        if a.keys() != b.keys():
            return [path + ":keys"]
        return [d for k in a for d in differences(a[k], b[k], path + "." + k)]
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return [path + ":length"]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in differences(x, y, path + "." + str(i))]
    if type(a) is float and type(b) is float:
        if abs(a - b) <= 1e-7 + 1e-6 * max(abs(a), abs(b)):
            return []
    if type(a) is not type(b):
        return [path + ":type"]
    if a == b:
        return []
    return [path]


def audit(bundle, *, trusted_digest=None):
    expected = {"schema", "authority", "software", "request", "result", "sha256"}
    if set(bundle) != expected:
        return {"passed": False, "errors": ["BUNDLE_SCHEMA"]}
    errors = []
    payload = {k: v for k, v in bundle.items() if k != "sha256"}
    if digest(payload) != bundle["sha256"]:
        errors.append("BUNDLE_DIGEST")
    if trusted_digest is not None and bundle["sha256"] != trusted_digest:
        errors.append("TRUSTED_DIGEST_MISMATCH")
    if bundle["schema"] != SCHEMA or bundle["authority"] != AUTHORITY:
        errors.append("CLAIM_BOUNDARY")
    current = software_identity()
    if (
        bundle["software"]["source_sha256"] != current["source_sha256"]
        or bundle["software"]["files"] != current["files"]
    ):
        errors.append("SOFTWARE_IDENTITY")
    # Dependency mismatch is visible but source-equivalent numerical replay can pass.
    try:
        replay = decide(bundle["request"])
        errors.extend(differences(bundle["result"], replay))
    except (ValueError, TypeError, KeyError, OverflowError) as exc:
        errors.append("REPLAY_INVALID:" + str(exc))
    return {
        "passed": not errors,
        "errors": errors,
        "dependency_match": bundle["software"]["dependencies"] == current["dependencies"],
        "authentication": "EXTERNAL_TRUST_REQUIRED",
        "physical_credit": False,
    }
