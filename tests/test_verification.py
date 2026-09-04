import pytest
from ahis.verification import VerificationChannel, VerificationVerdict, verify_repair


def good_channels():
    return [
        VerificationChannel("leak", .1, .2),
        VerificationChannel("frf", .04, .05),
        VerificationChannel("strain", .08, .1),
        VerificationChannel("thermal", 2, 5),
    ]


def test_verification_passes_with_quorum():
    r = verify_repair(good_channels())
    assert r.verdict is VerificationVerdict.PASS_POC


def test_verification_fails_on_bound_exceedance():
    rows = good_channels(); rows[0] = VerificationChannel("leak", .3, .2)
    r = verify_repair(rows)
    assert r.verdict is VerificationVerdict.FAIL
    assert r.failed_channels == ("leak",)


def test_required_unhealthy_is_inconclusive():
    rows = good_channels(); rows[1] = VerificationChannel("frf", 0, .05, healthy=False)
    r = verify_repair(rows)
    assert r.verdict is VerificationVerdict.INCONCLUSIVE
    assert r.unavailable_required_channels == ("frf",)


def test_optional_unhealthy_can_be_ignored_if_quorum_remains():
    rows = good_channels(); rows[3] = VerificationChannel("thermal", 0, 5, healthy=False, required=False)
    r = verify_repair(rows)
    assert r.verdict is VerificationVerdict.PASS_POC


def test_duplicate_channels_rejected():
    with pytest.raises(ValueError):
        verify_repair([VerificationChannel("x", 0, 1), VerificationChannel("x", 0, 1)])


def test_too_small_quorum_is_inconclusive():
    r = verify_repair(good_channels()[:2], minimum_independent_channels=3)
    assert r.verdict is VerificationVerdict.INCONCLUSIVE
