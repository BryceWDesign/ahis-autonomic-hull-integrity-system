#!/usr/bin/env python3
"""Run one live AHIS-P1 low-energy autonomous leak-seal experiment.

The script requires a physical Pico 2 over USB serial and two measured calibration
artifacts. It does not offer a synthetic mode and therefore cannot manufacture a
physical pass without live hardware telemetry.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ahis.p1_host import MassSample, calibration_bundle_sha256, estimate_leak_rate, paired_runtime_ms
from ahis.physical import P1RunEvidence, assess_p1_run, physical_run_receipt
from ahis.protocol import ProtocolCommand, decode_message, encode_command


class PicoClient:
    def __init__(self, port: str, baud: int, timeout_s: float):
        try:
            import serial  # type: ignore
        except ImportError as exc:
            raise RuntimeError("pyserial is required for a physical run: python -m pip install -e '.[hardware]'") from exc
        self.serial = serial.Serial(port, baudrate=baud, timeout=timeout_s, write_timeout=timeout_s)
        time.sleep(0.25)
        self.serial.reset_input_buffer()

    def close(self) -> None:
        self.serial.close()

    def request(self, command: ProtocolCommand, *, response_timeout_s: float = 35.0) -> dict[str, object]:
        self.serial.write(encode_command(command).encode("utf-8"))
        self.serial.flush()
        deadline = time.monotonic() + response_timeout_s
        while time.monotonic() < deadline:
            line = self.serial.readline().decode("utf-8", errors="strict").strip()
            if not line:
                continue
            msg = decode_message(line)
            if msg.get("type") == "boot":
                continue
            if msg.get("type") == "error":
                raise RuntimeError(str(msg.get("reason", "device error")))
            if msg.get("ok") is False:
                raise RuntimeError(str(msg.get("reason", "device denied command")))
            return msg
        raise TimeoutError(f"device did not answer {command.command} before timeout")


def _load_calibration(path: Path, required_fields: set[str]) -> dict[str, object]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("source_kind") != "PHYSICAL_CALIBRATION":
        raise ValueError(f"{path} is not marked PHYSICAL_CALIBRATION")
    missing = required_fields - set(raw)
    if missing:
        raise ValueError(f"{path} missing calibration fields: {sorted(missing)}")
    digest = str(raw.get("calibration_sha256", ""))
    unsigned = dict(raw)
    unsigned.pop("calibration_sha256", None)
    expected = sha256(json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if digest != expected:
        raise ValueError(f"{path} calibration SHA-256 does not match its content")
    return raw


def _append_telemetry(handle, *, phase: str, msg: dict[str, object], t0: float) -> None:
    record = {"elapsed_s": time.monotonic() - t0, "phase": phase, "device": msg}
    handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    handle.flush()


def _sample_leak(client: PicoClient, handle, *, phase: str, duration_s: float, interval_s: float, density: float, t0: float) -> tuple[object, float, float, bool]:
    samples: list[MassSample] = []
    max_head = 0.0
    max_pressure = 0.0
    estop_violation = False
    start = time.monotonic()
    next_sample = start
    while time.monotonic() - start < duration_s:
        now = time.monotonic()
        if now < next_sample:
            time.sleep(min(0.05, next_sample - now))
            continue
        msg = client.request(ProtocolCommand("STATUS"), response_timeout_s=2.0)
        _append_telemetry(handle, phase=phase, msg=msg, t0=t0)
        if not msg.get("estop_closed", False):
            estop_violation = True
        max_head = max(max_head, float(msg.get("head_mm", 0.0)))
        max_pressure = max(max_pressure, float(msg.get("pressure_kpa", 0.0)))
        if "mass_g" not in msg:
            raise RuntimeError("device status omitted mass_g")
        samples.append(MassSample(time.monotonic() - start, float(msg["mass_g"])))
        next_sample += interval_s
    estimate = estimate_leak_rate(samples, water_density_g_ml=density)
    return estimate, max_head, max_pressure, estop_violation


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True, help="Pico 2 serial port, e.g. COM6 or /dev/ttyACM0")
    parser.add_argument("--run-id", required=True, help="unique physical run identifier")
    parser.add_argument("--sensor-calibration", required=True, type=Path)
    parser.add_argument("--pump-calibration", required=True, type=Path)
    parser.add_argument("--fixture-leak-check", required=True, choices=["pass"], help="manual pre-run seam/plumbing leak inspection must pass")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "physical" / "P1")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--sample-interval-s", type=float, default=0.5)
    args = parser.parse_args()

    cfg = json.loads((ROOT / "configs" / "p1_reference.json").read_text(encoding="utf-8"))
    measurement = cfg["measurement"]
    repair = cfg["repair_surrogate"]
    density = float(measurement["water_density_g_ml_for_flow_conversion"])
    baseline_duration = float(measurement["baseline_window_s"])
    post_duration = float(measurement["post_repair_window_s"])
    if args.sample_interval_s <= 0 or args.sample_interval_s > 1.0:
        raise ValueError("sample interval must be >0 and <=1.0 s")

    sensor = _load_calibration(args.sensor_calibration, {
        "pressure_kpa_per_adc_fraction", "pressure_offset_kpa", "loadcell_counts_per_g", "loadcell_zero_counts", "calibration_sha256"
    })
    pump = _load_calibration(args.pump_calibration, {"pump_a_ml_s", "pump_b_ml_s", "calibration_sha256"})
    sensor_sha = str(sensor["calibration_sha256"])
    pump_sha = str(pump["calibration_sha256"])
    calibration_sha = calibration_bundle_sha256(sensor_sha, pump_sha)
    runtime_a_ms, runtime_b_ms = paired_runtime_ms(
        target_a_ml=float(repair["agent_a_target_volume_ml"]),
        target_b_ml=float(repair["agent_b_target_volume_ml"]),
        pump_a_ml_s=float(pump["pump_a_ml_s"]),
        pump_b_ml_s=float(pump["pump_b_ml_s"]),
        hard_limit_ms=int(repair["maximum_single_pump_runtime_s"] * 1000),
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    run_path = args.output_dir / f"{args.run_id}.json"
    telemetry_path = args.output_dir / f"{args.run_id}.telemetry.jsonl"
    if run_path.exists() or telemetry_path.exists():
        raise FileExistsError("run-id already exists; physical evidence is append-only by run identifier")

    client = PicoClient(args.port, args.baud, 1.0)
    t0 = time.monotonic()
    max_head = 0.0
    max_pressure = 0.0
    estop_violation = False
    try:
        with telemetry_path.open("x", encoding="utf-8", newline="\n") as telemetry:
            status = client.request(ProtocolCommand("STATUS"), response_timeout_s=2.0)
            _append_telemetry(telemetry, phase="preflight", msg=status, t0=t0)
            if status.get("calibration_sha256") != sensor_sha:
                raise RuntimeError("Pico sensor calibration digest does not match the supplied measured calibration")
            if not status.get("estop_closed", False):
                raise RuntimeError("E-stop is open at preflight")
            max_head = max(max_head, float(status.get("head_mm", 0.0)))
            max_pressure = max(max_pressure, float(status.get("pressure_kpa", 0.0)))

            baseline, h, p, e = _sample_leak(
                client, telemetry, phase="baseline", duration_s=baseline_duration, interval_s=args.sample_interval_s, density=density, t0=t0
            )
            max_head, max_pressure, estop_violation = max(max_head, h), max(max_pressure, p), estop_violation or e
            if baseline.leak_ml_min < float(measurement["minimum_baseline_leak_ml_min"]):
                raise RuntimeError("baseline leak is below the canonical P1 minimum; repair actuation is prohibited")
            if baseline.r_squared < float(measurement["minimum_flow_fit_r_squared"]):
                raise RuntimeError("baseline leak measurement fit is too weak; repair actuation is prohibited")

            arm = client.request(ProtocolCommand("ARM"), response_timeout_s=2.0)
            _append_telemetry(telemetry, phase="arm", msg=arm, t0=t0)
            pair = client.request(
                ProtocolCommand("PUMP_PAIR", duration_a_ms=runtime_a_ms, duration_b_ms=runtime_b_ms),
                response_timeout_s=max(runtime_a_ms, runtime_b_ms) / 1000.0 + 5.0,
            )
            _append_telemetry(telemetry, phase="repair_delivery", msg=pair, t0=t0)
            max_head = max(max_head, float(pair.get("max_head_mm", 0.0)))
            max_pressure = max(max_pressure, float(pair.get("max_pressure_kpa", 0.0)))
            disarm = client.request(ProtocolCommand("DISARM"), response_timeout_s=2.0)
            _append_telemetry(telemetry, phase="disarm", msg=disarm, t0=t0)

            dwell_s = float(repair["post_delivery_dwell_s"])
            dwell_start = time.monotonic()
            while time.monotonic() - dwell_start < dwell_s:
                msg = client.request(ProtocolCommand("STATUS"), response_timeout_s=2.0)
                _append_telemetry(telemetry, phase="dwell", msg=msg, t0=t0)
                estop_violation = estop_violation or not bool(msg.get("estop_closed", False))
                max_head = max(max_head, float(msg.get("head_mm", 0.0)))
                max_pressure = max(max_pressure, float(msg.get("pressure_kpa", 0.0)))
                time.sleep(min(1.0, max(0.0, dwell_s - (time.monotonic() - dwell_start))))

            post, h, p, e = _sample_leak(
                client, telemetry, phase="post_repair", duration_s=post_duration, interval_s=args.sample_interval_s, density=density, t0=t0
            )
            max_head, max_pressure, estop_violation = max(max_head, h), max(max_pressure, p), estop_violation or e
            final_status = client.request(ProtocolCommand("STATUS"), response_timeout_s=2.0)
            _append_telemetry(telemetry, phase="final", msg=final_status, t0=t0)
    except Exception:
        try:
            client.request(ProtocolCommand("STOP"), response_timeout_s=2.0)
        except Exception:
            pass
        raise
    finally:
        client.close()

    telemetry_sha = sha256(telemetry_path.read_bytes()).hexdigest()
    evidence = P1RunEvidence(
        run_id=args.run_id,
        source_kind="PHYSICAL_MEASUREMENT",
        baseline_leak_ml_min=baseline.leak_ml_min,
        post_repair_leak_ml_min=post.leak_ml_min,
        baseline_fit_r_squared=baseline.r_squared,
        post_fit_r_squared=post.r_squared,
        baseline_sample_count=baseline.sample_count,
        post_sample_count=post.sample_count,
        max_head_mm=max_head,
        max_pressure_kpa=max_pressure,
        estop_violation=estop_violation,
        unintended_fixture_leak=False,
        calibration_sha256=calibration_sha,
        telemetry_sha256=telemetry_sha,
    )
    assessment = assess_p1_run(evidence)
    payload = asdict(evidence) | {
        "measurement_metadata": {
            "water_density_g_ml": density,
            "sample_interval_s": args.sample_interval_s,
            "sensor_calibration_sha256": sensor_sha,
            "pump_calibration_sha256": pump_sha,
            "pump_runtime_a_ms": runtime_a_ms,
            "pump_runtime_b_ms": runtime_b_ms,
            "fixture_leak_check": args.fixture_leak_check,
        },
        "assessment": asdict(assessment),
        "receipt_sha256": physical_run_receipt(evidence),
        "claim_boundary": "P1_LOW_ENERGY_LEAK_SEAL_ONLY__NO_STRUCTURAL_STRENGTH_OR_HULL_SURVIVABILITY_CREDIT",
    }
    run_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(run_path)
    print(f"passed={assessment.passed}")
    return 0 if assessment.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
