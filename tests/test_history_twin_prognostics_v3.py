from dataclasses import replace
import pytest

from ahis.digital_twin import TwinBaseline, TwinObservation, assess_twin
from ahis.history import StructuralHistory
from ahis.prognostics import FatigueState, screen_remaining_cycles


def test_history_chain_verifies():
    h=StructuralHistory()
    h.append("a","2026-01-01T00:00:00Z",{"x":1})
    h.append("b","2026-01-01T00:00:01Z",{"y":2})
    assert h.verify()==()


def test_history_tamper_is_detected():
    h=StructuralHistory()
    e=h.append("a","2026-01-01T00:00:00Z",{"x":1})
    h._events[0]=replace(e,payload={"x":2})
    assert "event hash mismatch at 0" in h.verify()


def test_twin_nominal_accepts_small_drift():
    a=assess_twin(TwinBaseline((100,200),500,.5),TwinObservation((99,198),520,1))
    assert a.accepted


def test_twin_flags_multiple_channels():
    a=assess_twin(TwinBaseline((100,200),500,.5),TwinObservation((90,180),600,10))
    assert not a.accepted
    assert set(a.failed_channels)=={"modal","strain","leak"}


def test_rul_bounds_contain_nominal():
    r=screen_remaining_cycles(FatigueState(.5,1e-4,.2))
    assert r.lower_cycles <= r.nominal_cycles <= r.upper_cycles
    assert r.status=="SCREEN_ONLY_UNCERTIFIED"


def test_exhausted_rul_is_zero():
    r=screen_remaining_cycles(FatigueState(1.2,1e-4,.2))
    assert (r.lower_cycles,r.nominal_cycles,r.upper_cycles)==(0,0,0)
    assert r.status=="EXHAUSTED"

@pytest.mark.parametrize("uncertainty",[-.1,1,1.2])
def test_invalid_uncertainty_rejected(uncertainty):
    with pytest.raises(ValueError):
        FatigueState(.1,1e-4,uncertainty)
