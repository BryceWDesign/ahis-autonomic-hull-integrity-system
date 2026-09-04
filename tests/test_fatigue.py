import pytest
from ahis.fatigue import SNBlock, miners_rule, paris_crack_growth_per_cycle, project_paris_growth


def test_miners_rule_accumulates_history():
    state = miners_rule([SNBlock(100, 1000), SNBlock(50, 500)], prior_damage_fraction=.2)
    assert state.miner_damage_fraction == pytest.approx(.4)
    assert not state.screen_exceeded


def test_miners_rule_exceedance():
    state = miners_rule([SNBlock(1000, 1000)])
    assert state.screen_exceeded


def test_miners_rule_rejects_bad_life():
    with pytest.raises(ValueError):
        miners_rule([SNBlock(1, 0)])


def test_paris_growth_zero_delta_k():
    assert paris_crack_growth_per_cycle(delta_k_mpa_sqrt_m=0, c=1e-10, m=3) == 0


def test_paris_growth_projection():
    a = project_paris_growth(initial_crack_m=.001, cycles=1000, delta_k_mpa_sqrt_m=10, c=1e-12, m=3)
    assert a == pytest.approx(.001001)


def test_paris_rejects_negative_inputs():
    with pytest.raises(ValueError):
        project_paris_growth(initial_crack_m=-1, cycles=1, delta_k_mpa_sqrt_m=1, c=1, m=1)
