#!/usr/bin/env python3
"""Authoritative AHIS v3 repository/software release gate.

GREEN means the delivered repository, deterministic software/HIL campaign and release
integrity checks pass. It does not promote any physical demonstration flag.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ahis.evidence import verify_manifest

EXPECTED_VERSION = "3.0.0"
EXPECTED_AUTHORITY = "SOFTWARE_AND_HIL_ONLY__NO_PHYSICAL_HEALING_OR_HULL_SURVIVABILITY_CREDIT"
EXPECTED_CAMPAIGN_SHA = "1991c991b5fbbc3d9275abfb4e1e8f7d6c610a6ac07714f616dd6df8b5911977"
EXPECTED_TESTS = 112
LICENSE_CONTACT = "https://www.linkedin.com/in/brycewdesign/"


def cleanup_runtime_junk() -> None:
    for path in ROOT.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
    for name in (".pytest_cache", ".ruff_cache", ".mypy_cache"):
        shutil.rmtree(ROOT / name, ignore_errors=True)
    for path in ROOT.rglob("*.egg-info"):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)


def check_campaign() -> tuple[bool, str]:
    campaign_path = ROOT / "results/v3_extreme_campaign/campaign.json"
    receipt_path = ROOT / "results/v3_extreme_campaign/receipt.json"
    if not campaign_path.is_file() or not receipt_path.is_file():
        return False, "v3 campaign artifacts missing"
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    conditions = campaign.get("pass_conditions", {})
    if not conditions or not all(bool(v) for v in conditions.values()):
        return False, "one or more deterministic v3 campaign conditions failed"
    if campaign.get("authority") != EXPECTED_AUTHORITY or receipt.get("authority") != EXPECTED_AUTHORITY:
        return False, "software/HIL claim boundary changed"
    if receipt.get("sha256_canonical_json") != EXPECTED_CAMPAIGN_SHA:
        return False, "campaign canonical digest changed"
    if receipt.get("all_pass_conditions") is not True:
        return False, "campaign receipt does not report all pass conditions"
    return True, "deterministic v3 campaign and authority valid"


def check_license() -> tuple[bool, str]:
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    required = [
        "AHIS EVALUATION LICENSE 1.0",
        "Copyright (c) 2026 Bryce Lovell",
        "It is not an open-source",
        LICENSE_CONTACT,
        "Earlier AHIS releases",
    ]
    missing = [value for value in required if value not in text]
    if missing:
        return False, f"evaluation-license boundary missing: {missing}"
    if "v3.0.0" not in notice or LICENSE_CONTACT not in notice:
        return False, "NOTICE does not carry v3 licensing boundary/contact"
    if not (ROOT / "LICENSES/Apache-2.0-historical.txt").is_file():
        return False, "historical Apache license record missing"
    return True, "evaluation-only v3 licensing boundary explicit"


def check_physical_status() -> tuple[bool, str]:
    raw = json.loads((ROOT / "PHYSICAL_STATUS.json").read_text(encoding="utf-8"))
    if raw.get("version") != EXPECTED_VERSION or raw.get("status") != "AWAITING_PHYSICAL_VALIDATION":
        return False, "physical status header mismatch"
    booleans = {k: v for k, v in raw.items() if isinstance(v, bool)}
    if not booleans or any(booleans.values()):
        return False, "this release must ship with every physical demonstration/certification flag false"
    return True, f"{len(booleans)} physical claim flags remain false"


def check_bom_and_reference_build() -> tuple[bool, str]:
    bom_path = ROOT / "BOM/AHIS-P1-procurement.csv"
    rows = list(csv.DictReader(bom_path.read_text(encoding="utf-8").splitlines()))
    required_cols = {"item_id", "subsystem", "qty", "manufacturer_or_standard", "part_number_or_spec", "description", "required_characteristic", "source_url"}
    if not rows or set(rows[0]) != required_cols:
        return False, "P1 BOM columns invalid"
    mandatory = required_cols - {"source_url"}
    for i, row in enumerate(rows, start=2):
        if any(not str(row.get(col, "")).strip() for col in mandatory):
            return False, f"P1 BOM row {i} has an unresolved required field"
    ids = [r["item_id"] for r in rows]
    if len(ids) != len(set(ids)):
        return False, "P1 BOM contains duplicate item IDs"
    if len(rows) < 50:
        return False, "P1 BOM unexpectedly incomplete"
    required_files = [
        "hardware/P1_BUILD_RECORD.csv", "hardware/P1_WIRING.csv",
        "hardware/firmware/pico2/main.py", "hardware/firmware/pico2/device_calibration.schema.json",
        "hardware/cad/dimensions.json", "hardware/cad/AHIS-P1-front-plate.step",
        "hardware/cad/AHIS-P1-back-plate.step", "hardware/cad/AHIS-P1-spacer.step",
        "hardware/cad/AHIS-P1-gasket.step", "hardware/cad/AHIS-P1-nozzle-bracket.step",
        "hardware/cad/AHIS-P1-estop-panel.step", "scripts/p1_run_controller.py",
        "scripts/p1_assess_campaign.py",
    ]
    missing = [rel for rel in required_files if not (ROOT / rel).is_file()]
    if missing:
        return False, f"P1 reference-build files missing: {missing[:3]}"
    config = json.loads((ROOT / "configs/p1_reference.json").read_text(encoding="utf-8"))
    if config.get("article_id") != "AHIS-P1-LOW-ENERGY-LEAK-SEAL-CELL":
        return False, "P1 config article ID mismatch"
    if config["hydrostatic"].get("compressed_gas_prohibited") is not True:
        return False, "P1 compressed-gas prohibition missing"
    if float(config["measurement"].get("minimum_leak_reduction_fraction", 0)) != 0.8:
        return False, "P1 80% leak-reduction acceptance changed"
    return True, f"P1 reference build complete; {len(rows)} procurement rows"


def stl_bounds(path: Path) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """Return STL bounds for either binary or ASCII STL files.

    Open CASCADE exports binary STL by default, so the release gate must validate
    the delivered geometry without assuming a text representation.
    """
    import struct

    data = path.read_bytes()
    mins = [float("inf")] * 3
    maxs = [float("-inf")] * 3
    count = 0

    if len(data) >= 84:
        triangle_count = struct.unpack_from("<I", data, 80)[0]
        expected_size = 84 + triangle_count * 50
        if expected_size == len(data):
            offset = 84
            for _ in range(triangle_count):
                # 12-byte normal, then three little-endian float32 vertices.
                values = struct.unpack_from("<12fH", data, offset)
                for vertex_start in (3, 6, 9):
                    xyz = values[vertex_start:vertex_start + 3]
                    for i, value in enumerate(xyz):
                        mins[i] = min(mins[i], value)
                        maxs[i] = max(maxs[i], value)
                    count += 1
                offset += 50

    if count == 0:
        text = data.decode("ascii", errors="strict")
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped.startswith("vertex "):
                continue
            xyz = [float(v) for v in stripped.split()[1:4]]
            for i, value in enumerate(xyz):
                mins[i] = min(mins[i], value)
                maxs[i] = max(maxs[i], value)
            count += 1

    if count == 0:
        raise ValueError(f"no STL vertices found in {path.name}")
    return tuple(mins), tuple(maxs)


def check_cad() -> tuple[bool, str]:
    expected = {
        "AHIS-P1-front-plate.stl": ((-75,-75,-3),(75,75,3)),
        "AHIS-P1-back-plate.stl": ((-75,-75,-3),(75,75,3)),
        "AHIS-P1-spacer.stl": ((-75,-75,-5),(75,75,5)),
        "AHIS-P1-gasket.stl": ((-75,-75,-0.75),(75,75,0.75)),
        "AHIS-P1-nozzle-bracket.stl": ((-25,-10,-4),(25,10,4)),
        "AHIS-P1-estop-panel.stl": ((-50,-35,-1.5),(50,35,1.5)),
    }
    for name, target in expected.items():
        path = ROOT / "hardware/cad" / name
        if not path.is_file():
            return False, f"generated CAD missing: {name}"
        bounds = stl_bounds(path)
        for got, want in zip(bounds[0] + bounds[1], target[0] + target[1]):
            if abs(got - want) > 0.02:
                return False, f"CAD envelope mismatch in {name}: {bounds}"
    return True, "six generated P1 STL envelopes match dimensional registry"


def check_no_unfinished_or_junk() -> tuple[bool, str]:
    marker_parts = ("T" + "BD", "TO" + "DO", "FIX" + "ME", "PLACE" + "HOLDER", "COPY_FROM_" + "GENERATED")
    text_suffixes = {".md", ".py", ".json", ".csv", ".toml", ".yml", ".yaml", ".txt"}
    skip = {"LICENSES/Apache-2.0-historical.txt", "MANIFEST.sha256"}
    hits: list[str] = []
    symlinks: list[str] = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            symlinks.append(rel)
        if not path.is_file() or rel in skip or path.suffix.lower() not in text_suffixes:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if any(marker in text.upper() for marker in marker_parts):
            hits.append(rel)
    junk = [rel for rel in (".pytest_cache", ".ruff_cache", ".mypy_cache") if (ROOT / rel).exists()]
    pycache = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("__pycache__")]
    if hits:
        return False, f"unfinished marker found in active release: {hits[:3]}"
    if symlinks:
        return False, f"symlinks prohibited in release: {symlinks[:3]}"
    if junk or pycache:
        return False, f"runtime cache/junk present: {(junk + pycache)[:3]}"
    return True, "no unresolved markers, symlinks or runtime caches"


def check_green_status(test_count: int) -> tuple[bool, str]:
    raw = json.loads((ROOT / "GREEN_STATUS.json").read_text(encoding="utf-8"))
    if raw.get("version") != EXPECTED_VERSION or raw.get("local_repository_quality") != "GREEN":
        return False, "GREEN_STATUS header mismatch"
    if int(raw.get("pytest_passed", -1)) != test_count or test_count != EXPECTED_TESTS:
        return False, f"GREEN_STATUS/test-count mismatch ({raw.get('pytest_passed')} vs {test_count})"
    if raw.get("campaign_receipt_sha256") != EXPECTED_CAMPAIGN_SHA:
        return False, "GREEN_STATUS campaign digest mismatch"
    if raw.get("physical_status") != "AWAITING_PHYSICAL_VALIDATION":
        return False, "GREEN_STATUS physical boundary mismatch"
    return True, "explicit v3 GREEN status artifact valid"


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    compile_proc = run([sys.executable, "-m", "compileall", "-q", "src", "scripts", "hardware/firmware/pico2", "check_green.py"])
    checks.append(("Python compile", compile_proc.returncode == 0, compile_proc.stderr.strip()))

    test_proc = run([sys.executable, "-m", "pytest", "-q"])
    combined = test_proc.stdout + "\n" + test_proc.stderr
    match = re.search(r"(\d+) passed", combined)
    test_count = int(match.group(1)) if match else -1
    checks.append(("Pytest", test_proc.returncode == 0 and test_count == EXPECTED_TESTS, f"{test_count} tests passed" if test_count >= 0 else combined[-500:]))

    campaign_proc = run([sys.executable, "scripts/run_v3_campaign.py"])
    checks.append(("V3 deterministic campaign", campaign_proc.returncode == 0, campaign_proc.stdout.strip().splitlines()[-1] if campaign_proc.stdout.strip() else campaign_proc.stderr.strip()))
    campaign_ok, campaign_msg = check_campaign(); checks.append(("Campaign receipt", campaign_ok, campaign_msg))
    license_ok, license_msg = check_license(); checks.append(("Evaluation license", license_ok, license_msg))
    physical_ok, physical_msg = check_physical_status(); checks.append(("Physical claim firewall", physical_ok, physical_msg))
    bom_ok, bom_msg = check_bom_and_reference_build(); checks.append(("P1 build package", bom_ok, bom_msg))
    cad_ok, cad_msg = check_cad(); checks.append(("P1 CAD envelope", cad_ok, cad_msg))
    status_ok, status_msg = check_green_status(test_count); checks.append(("GREEN status artifact", status_ok, status_msg))

    cleanup_runtime_junk()
    junk_ok, junk_msg = check_no_unfinished_or_junk(); checks.append(("Release hygiene", junk_ok, junk_msg))

    manifest_path = ROOT / "MANIFEST.sha256"
    manifest_errors = verify_manifest(ROOT, manifest_path) if manifest_path.is_file() else ("manifest missing",)
    checks.append(("Complete manifest", not manifest_errors, "; ".join(manifest_errors[:3]) if manifest_errors else "all released files accounted for"))

    print("AHIS v3.0.0 RELEASE QUALITY GATE")
    ok = True
    for name, passed, detail in checks:
        ok &= passed
        print(f"{name:.<34} {'PASS' if passed else 'FAIL'}")
        if detail:
            print(f"  {detail}")
    print(f"{'FINAL':.<34} {'GREEN' if ok else 'RED'}")
    print("PHYSICAL STATUS................... AWAITING_PHYSICAL_VALIDATION")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
