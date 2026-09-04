import pytest

from ahis.p1_host import MassSample, calibration_bundle_sha256, estimate_leak_rate, paired_runtime_ms
from ahis.protocol import ProtocolCommand, encode_command


def test_leak_rate_linear_mass_gain():
    samples = [MassSample(i, 100.0 + 0.5 * i) for i in range(10)]
    out = estimate_leak_rate(samples, water_density_g_ml=1.0)
    assert out.leak_ml_min == pytest.approx(30.0)
    assert out.r_squared == pytest.approx(1.0)


def test_leak_rate_rejects_nonmonotonic_time():
    with pytest.raises(ValueError):
        estimate_leak_rate([MassSample(0, 0), MassSample(1, 1), MassSample(1, 2), MassSample(2, 3), MassSample(3, 4)], water_density_g_ml=1.0)


def test_pair_runtime_uses_independent_calibrations():
    assert paired_runtime_ms(target_a_ml=8, target_b_ml=8, pump_a_ml_s=0.5, pump_b_ml_s=0.4) == (16000, 20000)


def test_pair_runtime_rejects_hard_limit():
    with pytest.raises(ValueError):
        paired_runtime_ms(target_a_ml=8, target_b_ml=8, pump_a_ml_s=0.1, pump_b_ml_s=0.1)


def test_calibration_bundle_digest_is_stable():
    a = "a" * 64
    b = "b" * 64
    assert calibration_bundle_sha256(a, b) == calibration_bundle_sha256(a, b)
    assert calibration_bundle_sha256(a, b) != calibration_bundle_sha256(b, a)


def test_protocol_paired_pump_command():
    text = encode_command(ProtocolCommand("PUMP_PAIR", duration_a_ms=1000, duration_b_ms=1500))
    assert text == '{"cmd":"PUMP_PAIR","duration_a_ms":1000,"duration_b_ms":1500}\n'
