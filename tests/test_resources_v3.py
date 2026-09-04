import pytest

from ahis.resources import RepairDemand, RepairResourceBudget, reserve_resources


def budget():
    return RepairResourceBudget(20, 20, 1000, 30, 10)


def test_reserve_resources_consumes_all_dimensions():
    result = reserve_resources(budget(), RepairDemand(2, 3, 100, 5, 2))
    assert result.allowed
    assert result.remaining == RepairResourceBudget(18, 17, 900, 25, 8)

@pytest.mark.parametrize("demand,deficit", [
    (RepairDemand(agent_a_ml=21), "agent_a_ml"),
    (RepairDemand(agent_b_ml=21), "agent_b_ml"),
    (RepairDemand(electrical_energy_j=1001), "electrical_energy_j"),
    (RepairDemand(thermal_headroom_c=31), "thermal_headroom_c"),
    (RepairDemand(actuator_cycles=11), "actuator_cycles_remaining"),
])
def test_each_resource_deficit_fails_closed(demand, deficit):
    result = reserve_resources(budget(), demand)
    assert not result.allowed
    assert deficit in result.deficits
    assert result.remaining == budget()

@pytest.mark.parametrize("kwargs", [
    {"agent_a_ml": -1}, {"agent_b_ml": -1}, {"electrical_energy_j": -1},
    {"thermal_headroom_c": -1}, {"actuator_cycles_remaining": -1},
])
def test_negative_budget_rejected(kwargs):
    base = dict(agent_a_ml=1, agent_b_ml=1, electrical_energy_j=1, thermal_headroom_c=1, actuator_cycles_remaining=1)
    base.update(kwargs)
    with pytest.raises(ValueError):
        RepairResourceBudget(**base)
