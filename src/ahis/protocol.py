"""Strict newline-delimited JSON protocol shared by host tools and P1 firmware."""
from __future__ import annotations

from dataclasses import dataclass
import json

_ALLOWED_COMMANDS = {"STATUS", "ARM", "DISARM", "PUMP_A", "PUMP_B", "PUMP_PAIR", "STOP"}


@dataclass(frozen=True, slots=True)
class ProtocolCommand:
    command: str
    duration_ms: int = 0
    duration_a_ms: int = 0
    duration_b_ms: int = 0


def encode_command(command: ProtocolCommand) -> str:
    cmd = command.command.upper()
    if cmd not in _ALLOWED_COMMANDS:
        raise ValueError("unsupported command")
    durations = (command.duration_ms, command.duration_a_ms, command.duration_b_ms)
    if any(v < 0 or v > 30_000 for v in durations):
        raise ValueError("duration outside hard protocol limit")
    if cmd in {"PUMP_A", "PUMP_B"}:
        if command.duration_ms <= 0 or command.duration_a_ms or command.duration_b_ms:
            raise ValueError("single-pump command requires only positive duration_ms")
        payload = {"cmd": cmd, "duration_ms": command.duration_ms}
    elif cmd == "PUMP_PAIR":
        if command.duration_ms or command.duration_a_ms <= 0 or command.duration_b_ms <= 0:
            raise ValueError("paired command requires positive duration_a_ms and duration_b_ms only")
        payload = {"cmd": cmd, "duration_a_ms": command.duration_a_ms, "duration_b_ms": command.duration_b_ms}
    else:
        if any(durations):
            raise ValueError("duration fields only valid for pump commands")
        payload = {"cmd": cmd}
    return json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"


def decode_message(line: str) -> dict[str, object]:
    raw = json.loads(line)
    if not isinstance(raw, dict):
        raise ValueError("protocol message must be an object")
    allowed = {
        "type", "ok", "reason", "head_mm", "pressure_kpa", "leak_ml_min", "supply_v",
        "estop_closed", "armed", "mass_g", "calibration_sha256", "channel",
        "max_pressure_kpa", "max_head_mm", "duration_a_ms", "duration_b_ms", "duration_ms",
    }
    extra = set(raw) - allowed
    if extra:
        raise ValueError(f"unknown protocol fields: {sorted(extra)}")
    return raw
