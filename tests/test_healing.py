import pytest
from ahis.healing import DamageCase, HealingMechanism, select_healing_response


def case(**kw):
    base = dict(damage_kind="matrix_crack", opening_mm=.2, affected_area_mm2=100, through_thickness=False, substrate_family="hybrid_laminate", temperature_c=25, available_activation_temp_c=150, vascular_agent_available=True, healing_cycles_used=0)
    base.update(kw); return DamageCase(**base)


def test_ionomer_lane_is_seal_only():
    d = case(damage_kind="puncture", opening_mm=2, through_thickness=True)
    out = select_healing_response(d)
    assert out.mechanism is HealingMechanism.IONOMER_PUNCTURE_SEAL
    assert out.seal_credit
    assert out.structural_restoration_credit == 0


def test_microvascular_lane():
    out = select_healing_response(case())
    assert out.mechanism is HealingMechanism.MICROVASCULAR_MATRIX_REPAIR
    assert out.eligible


def test_microvascular_reservoir_limit():
    out = select_healing_response(case(healing_cycles_used=3))
    assert not out.eligible


def test_vitrimer_lane():
    out = select_healing_response(case(substrate_family="vitrimer_composite", vascular_agent_available=False))
    assert out.mechanism is HealingMechanism.VITRIMER_THERMAL_REPAIR


def test_vitrimer_denied_without_heat():
    out = select_healing_response(case(substrate_family="vitrimer_composite", vascular_agent_available=False, available_activation_temp_c=80))
    assert not out.eligible


def test_sma_mmc_lane():
    out = select_healing_response(case(damage_kind="fatigue_crack", substrate_family="sma_liquid_assisted_mmc", opening_mm=1.0, available_activation_temp_c=160, vascular_agent_available=False))
    assert out.mechanism is HealingMechanism.SMA_LIQUID_ASSISTED_METAL_REPAIR


def test_oversize_damage_rejected():
    out = select_healing_response(case(opening_mm=5.0, affected_area_mm2=10000))
    assert out.mechanism is HealingMechanism.NONE


def test_negative_dimensions_rejected():
    with pytest.raises(ValueError):
        select_healing_response(case(opening_mm=-.1))
