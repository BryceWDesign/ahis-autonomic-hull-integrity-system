from ahis.hardware import HILRig, InterlockLimits, RepairRecipe, assess_interlocks
from ahis.repair_control import plan_two_agent_repair
from ahis.resources import RepairResourceBudget


def setup():
    rig=HILRig()
    lock=assess_interlocks(rig.frame(0), InterlockLimits())
    recipe=RepairRecipe("P1",10,10,30,.8)
    return rig,lock,recipe


def test_plan_generates_two_bounded_commands():
    rig,lock,recipe=setup()
    plan=plan_two_agent_repair(recipe,budget=RepairResourceBudget(50,50,5000,30,10),interlock=lock,pump_a_ml_s=.5,pump_b_ml_s=.5)
    assert plan.allowed
    assert len(plan.commands)==2
    assert all(c.runtime_s==20 for c in plan.commands)


def test_plan_rejects_open_estop():
    rig,_,recipe=setup()
    lock=assess_interlocks(HILRig(estop_closed=False).frame(0),InterlockLimits())
    plan=plan_two_agent_repair(recipe,budget=RepairResourceBudget(50,50,5000,30,10),interlock=lock,pump_a_ml_s=.5,pump_b_ml_s=.5)
    assert not plan.allowed
    assert "interlock" in plan.reason


def test_plan_rejects_resource_deficit():
    _,lock,recipe=setup()
    plan=plan_two_agent_repair(recipe,budget=RepairResourceBudget(1,1,50,1,1),interlock=lock,pump_a_ml_s=.5,pump_b_ml_s=.5)
    assert not plan.allowed
    assert "resource deficit" in plan.reason


def test_plan_rejects_runtime_beyond_recipe_limit():
    _,lock,recipe=setup()
    plan=plan_two_agent_repair(recipe,budget=RepairResourceBudget(50,50,5000,30,10),interlock=lock,pump_a_ml_s=.1,pump_b_ml_s=.1)
    assert not plan.allowed
    assert "runtime" in plan.reason
