"""Canonical evidence and manifest utilities."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def digest_json(value: Any) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(root: Path, *, exclude: set[str] | None = None) -> list[tuple[str, str]]:
    excluded = exclude or set()
    rows: list[tuple[str, str]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        parts = path.relative_to(root).parts
        if (
            rel in excluded
            or rel.startswith(".git/")
            or "__pycache__" in parts
            or ".pytest_cache" in parts
            or ".ruff_cache" in parts
            or ".mypy_cache" in parts
            or ".venv" in parts
            or any(part.endswith(".egg-info") for part in parts)
        ):
            continue
        rows.append((sha256_file(path), rel))
    return rows


def write_manifest(root: Path, out: Path) -> None:
    rows = build_manifest(root, exclude={out.relative_to(root).as_posix()})
    out.write_bytes("".join(f"{digest}  {rel}\n" for digest, rel in rows).encode("utf-8"))


def verify_manifest(root: Path, manifest: Path) -> tuple[str, ...]:
    errors: list[str] = []
    declared: dict[str, str] = {}
    for line_no, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            expected, rel = line.split("  ", 1)
        except ValueError:
            errors.append(f"line {line_no}: malformed manifest row")
            continue
        if rel in declared:
            errors.append(f"line {line_no}: duplicate manifest path: {rel}")
            continue
        declared[rel] = expected
        path = root / rel
        if not path.is_file():
            errors.append(f"missing file: {rel}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            errors.append(f"hash mismatch: {rel}")
    actual_paths = {rel for _, rel in build_manifest(root, exclude={manifest.relative_to(root).as_posix()})}
    for rel in sorted(actual_paths - set(declared)):
        errors.append(f"unmanifested file: {rel}")
    for rel in sorted(set(declared) - actual_paths):
        if (root / rel).is_file():
            errors.append(f"manifest path excluded from canonical file set: {rel}")
    return tuple(errors)
