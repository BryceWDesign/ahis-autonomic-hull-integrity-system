"""AHIS-P1 Raspberry Pi Pico 2 MicroPython firmware.

Safety model:
- GP15 observes a dedicated normally-closed E-stop contact. Pressed/open => NOT SAFE.
- A separate normally-closed E-stop contact physically interrupts 12 V relay-coil power.
- GP6 commands the Pololu 2482 relay carrier; relay NO contacts feed actuator-only 12 V.
- GP2/GP3 command independent low-side pump drivers.
- Pump outputs cannot assert unless armed, calibrated, E-stop closed, and pressure/head
  remain inside the low-energy gravity-head P1 envelope.

This firmware is only for AHIS-P1. It is not pressure-vessel, hull, life-support,
flight, marine-control, or safety-certified software.
"""
from machine import ADC, Pin
import json
import sys
import time

PUMP_A = Pin(2, Pin.OUT, value=0)
PUMP_B = Pin(3, Pin.OUT, value=0)
HX_DOUT = Pin(4, Pin.IN)
HX_CLK = Pin(5, Pin.OUT, value=0)
RELAY_ENABLE = Pin(6, Pin.OUT, value=0)
ESTOP_SENSE = Pin(15, Pin.IN, Pin.PULL_UP)
PRESSURE_ADC = ADC(26)

MAX_HEAD_MM = 800.0
MAX_PRESSURE_KPA = 8.0
MAX_PUMP_MS = 30_000
CALIBRATION_FILE = "device_calibration.json"


class HX711:
    def __init__(self, dout, clk):
        self.dout = dout
        self.clk = clk

    def read_raw(self, timeout_ms=250):
        start = time.ticks_ms()
        while self.dout.value():
            if time.ticks_diff(time.ticks_ms(), start) > timeout_ms:
                raise RuntimeError("HX711 timeout")
        value = 0
        for _ in range(24):
            self.clk.value(1)
            value = (value << 1) | self.dout.value()
            self.clk.value(0)
        self.clk.value(1)  # gain 128, channel A
        self.clk.value(0)
        if value & 0x800000:
            value -= 1 << 24
        return value


hx = HX711(HX_DOUT, HX_CLK)
armed = False


def load_calibration():
    try:
        with open(CALIBRATION_FILE, "r") as f:
            raw = json.load(f)
    except Exception:
        return None
    required = {
        "pressure_kpa_per_adc_fraction",
        "pressure_offset_kpa",
        "loadcell_counts_per_g",
        "loadcell_zero_counts",
        "calibration_sha256",
    }
    if not required.issubset(raw):
        return None
    if raw["loadcell_counts_per_g"] == 0:
        return None
    digest = str(raw["calibration_sha256"])
    if len(digest) != 64:
        return None
    return raw


calibration = load_calibration()


def estop_closed():
    return ESTOP_SENSE.value() == 0


def pressure_kpa():
    if calibration is None:
        raise RuntimeError("calibration unavailable")
    fraction = PRESSURE_ADC.read_u16() / 65535.0
    return max(0.0, calibration["pressure_kpa_per_adc_fraction"] * fraction + calibration["pressure_offset_kpa"])


def head_mm_from_pressure(kpa):
    return kpa / 0.00980665


def mass_g(samples=5):
    if calibration is None:
        raise RuntimeError("calibration unavailable")
    total = 0
    for _ in range(samples):
        total += hx.read_raw()
    raw = total / samples
    return (raw - calibration["loadcell_zero_counts"]) / calibration["loadcell_counts_per_g"]


def hard_stop():
    global armed
    PUMP_A.value(0)
    PUMP_B.value(0)
    RELAY_ENABLE.value(0)
    armed = False


def safety_snapshot():
    if calibration is None:
        return {"ok": False, "reason": "calibration_missing", "estop_closed": estop_closed()}
    try:
        p = pressure_kpa()
        m = mass_g()
    except Exception as exc:
        hard_stop()
        return {"ok": False, "reason": "sensor_fault:" + str(exc), "estop_closed": estop_closed()}
    head = head_mm_from_pressure(p)
    ok = estop_closed() and p <= MAX_PRESSURE_KPA and head <= MAX_HEAD_MM
    return {
        "ok": ok,
        "reason": "safe" if ok else "interlock_open",
        "estop_closed": estop_closed(),
        "pressure_kpa": p,
        "head_mm": head,
        "mass_g": m,
        "armed": armed,
        "calibration_sha256": calibration["calibration_sha256"],
    }


def _check_live_interlocks():
    if not estop_closed():
        raise RuntimeError("estop opened during actuation")
    p = pressure_kpa()
    h = head_mm_from_pressure(p)
    if p > MAX_PRESSURE_KPA or h > MAX_HEAD_MM:
        raise RuntimeError("pressure/head limit exceeded during actuation")
    return p, h


def pump_single(pin, duration_ms):
    if duration_ms <= 0 or duration_ms > MAX_PUMP_MS:
        raise ValueError("duration outside hard limit")
    snap = safety_snapshot()
    if not armed or not snap.get("ok"):
        hard_stop()
        raise RuntimeError("actuation denied by arm/interlock state")
    max_p = float(snap["pressure_kpa"])
    max_h = float(snap["head_mm"])
    pin.value(1)
    start = time.ticks_ms()
    try:
        while time.ticks_diff(time.ticks_ms(), start) < duration_ms:
            p, h = _check_live_interlocks()
            max_p = max(max_p, p)
            max_h = max(max_h, h)
            time.sleep_ms(20)
    finally:
        pin.value(0)
    return max_p, max_h


def pump_pair(duration_a_ms, duration_b_ms):
    if duration_a_ms <= 0 or duration_b_ms <= 0 or duration_a_ms > MAX_PUMP_MS or duration_b_ms > MAX_PUMP_MS:
        raise ValueError("paired durations outside hard limit")
    snap = safety_snapshot()
    if not armed or not snap.get("ok"):
        hard_stop()
        raise RuntimeError("paired actuation denied by arm/interlock state")
    max_p = float(snap["pressure_kpa"])
    max_h = float(snap["head_mm"])
    PUMP_A.value(1)
    PUMP_B.value(1)
    start = time.ticks_ms()
    try:
        while True:
            elapsed = time.ticks_diff(time.ticks_ms(), start)
            if elapsed >= duration_a_ms:
                PUMP_A.value(0)
            if elapsed >= duration_b_ms:
                PUMP_B.value(0)
            if elapsed >= duration_a_ms and elapsed >= duration_b_ms:
                break
            p, h = _check_live_interlocks()
            max_p = max(max_p, p)
            max_h = max(max_h, h)
            time.sleep_ms(20)
    finally:
        PUMP_A.value(0)
        PUMP_B.value(0)
    return max_p, max_h


def reply(obj):
    sys.stdout.write(json.dumps(obj) + "\n")


def handle(line):
    global armed
    raw = json.loads(line)
    if not isinstance(raw, dict):
        raise ValueError("invalid command object")
    allowed = {"cmd", "duration_ms", "duration_a_ms", "duration_b_ms"}
    if set(raw) - allowed:
        raise ValueError("invalid command fields")
    cmd = str(raw.get("cmd", "")).upper()
    duration = int(raw.get("duration_ms", 0))
    duration_a = int(raw.get("duration_a_ms", 0))
    duration_b = int(raw.get("duration_b_ms", 0))
    if cmd == "STATUS":
        if duration or duration_a or duration_b:
            raise ValueError("status takes no duration")
        return {"type": "status", **safety_snapshot()}
    if cmd == "STOP" or cmd == "DISARM":
        if duration or duration_a or duration_b:
            raise ValueError("stop/disarm takes no duration")
        hard_stop()
        return {"type": "ack", "ok": True, "reason": "stopped"}
    if cmd == "ARM":
        if duration or duration_a or duration_b:
            raise ValueError("arm takes no duration")
        snap = safety_snapshot()
        if not snap.get("ok"):
            hard_stop()
            return {"type": "ack", "ok": False, "reason": snap.get("reason", "unsafe")}
        RELAY_ENABLE.value(1)
        armed = True
        return {"type": "ack", "ok": True, "reason": "armed"}
    if cmd in ("PUMP_A", "PUMP_B"):
        if duration <= 0 or duration > MAX_PUMP_MS or duration_a or duration_b:
            raise ValueError("invalid single-pump duration")
        max_p, max_h = pump_single(PUMP_A if cmd == "PUMP_A" else PUMP_B, duration)
        return {
            "type": "ack", "ok": True, "reason": cmd.lower() + "_complete", "duration_ms": duration,
            "max_pressure_kpa": max_p, "max_head_mm": max_h,
        }
    if cmd == "PUMP_PAIR":
        if duration or duration_a <= 0 or duration_b <= 0:
            raise ValueError("invalid paired-pump durations")
        max_p, max_h = pump_pair(duration_a, duration_b)
        return {
            "type": "ack", "ok": True, "reason": "pump_pair_complete",
            "duration_a_ms": duration_a, "duration_b_ms": duration_b,
            "max_pressure_kpa": max_p, "max_head_mm": max_h,
        }
    raise ValueError("unsupported command")


hard_stop()
reply({"type": "boot", "ok": calibration is not None, "reason": "ready" if calibration is not None else "calibration_missing"})
while True:
    try:
        line = sys.stdin.readline()
        if not line:
            time.sleep_ms(10)
            continue
        reply(handle(line))
    except Exception as exc:
        hard_stop()
        reply({"type": "error", "ok": False, "reason": str(exc)})
