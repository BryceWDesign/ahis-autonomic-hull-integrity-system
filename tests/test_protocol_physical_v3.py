import json
import pytest

from ahis.physical import P1RunEvidence, assess_p1_campaign, assess_p1_run, physical_run_receipt
from ahis.protocol import ProtocolCommand, decode_message, encode_command

CAL = "a" * 64
TEL = "b" * 64


def run(run_id="r1", post=5, source="PHYSICAL_MEASUREMENT", r2=0.99, n=40):
    return P1RunEvidence(run_id, source, 50, post, r2, r2, n, n, 500, 5, False, False, CAL, TEL)


def test_protocol_encodes_bounded_pump_command():
    raw = encode_command(ProtocolCommand("PUMP_A", 1000))
    assert json.loads(raw) == {"cmd": "PUMP_A", "duration_ms": 1000}


@pytest.mark.parametrize("cmd,duration", [("BAD", 0), ("PUMP_A", 0), ("STATUS", 1), ("PUMP_B", 30001)])
def test_protocol_rejects_invalid_commands(cmd, duration):
    with pytest.raises(ValueError):
        encode_command(ProtocolCommand(cmd, duration))


def test_protocol_decoder_rejects_unknown_fields():
    with pytest.raises(ValueError):
        decode_message('{"type":"status","magic":1}')


def test_physical_run_passes_only_with_measured_evidence():
    a = assess_p1_run(run())
    assert a.passed
    assert a.leak_reduction_fraction == pytest.approx(.9)


def test_nonphysical_source_rejected():
    with pytest.raises(ValueError):
        run(source="HIL")


def test_physical_run_fails_insufficient_reduction():
    assert not assess_p1_run(run(post=15)).passed


def test_physical_run_fails_weak_measurement_fit():
    assert not assess_p1_run(run(r2=0.8)).passed


def test_physical_run_fails_insufficient_samples():
    assert not assess_p1_run(run(n=10)).passed


def test_campaign_requires_two_of_three_passes():
    c = assess_p1_campaign([run("1", 5), run("2", 5), run("3", 15)])
    assert c["physical_demonstration"]
    assert c["pass_count"] == 2


def test_campaign_rejects_wrong_run_count():
    with pytest.raises(ValueError):
        assess_p1_campaign([run("1"), run("2")])


def test_receipt_is_stable_sha256_and_binds_telemetry():
    a = physical_run_receipt(run())
    b = physical_run_receipt(run())
    assert a == b and len(a) == 64
    changed = P1RunEvidence("r1", "PHYSICAL_MEASUREMENT", 50, 5, .99, .99, 40, 40, 500, 5, False, False, CAL, "c" * 64)
    assert physical_run_receipt(changed) != a
