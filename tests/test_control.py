import pytest
from ahis.control import ModalTarget, plan_modal_damping, resonant_transmissibility


def test_damping_reduces_resonant_transmissibility():
    p = plan_modal_damping(ModalTarget(120,.02,.08), max_delta_zeta=.10)
    assert p.predicted_resonant_transmissibility_after < p.predicted_resonant_transmissibility_before
    assert not p.saturated


def test_authority_saturation():
    p = plan_modal_damping(ModalTarget(120,.02,.20), max_delta_zeta=.05)
    assert p.saturated
    assert p.authority_utilization == 1


def test_bad_zeta_rejected():
    with pytest.raises(ValueError): resonant_transmissibility(0)
    with pytest.raises(ValueError): plan_modal_damping(ModalTarget(10,.2,.1), max_delta_zeta=.1)


def test_bad_frequency_rejected():
    with pytest.raises(ValueError): plan_modal_damping(ModalTarget(0,.02,.08), max_delta_zeta=.1)
