import pytest

from ahis.hardware import HILRig, HardwareCommand, InterlockLimits, PumpChannel, RepairRecipe, SensorFrame, assess_interlocks


def test_safe_frame_allows_actuation():
    assert assess_interlocks(HILRig().frame(0), InterlockLimits()).allowed

@pytest.mark.parametrize("rig,reason", [
    (HILRig(estop_closed=False), "estop_open"),
    (HILRig(sensor_valid=False), "sensor_invalid"),
    (HILRig(head_mm=801), "head_limit_exceeded"),
    (HILRig(injected_pressure_kpa=8.01), "pressure_limit_exceeded"),
    (HILRig(supply_v=13.1), "supply_limit_exceeded"),
])
def test_interlock_faults_fail_closed(rig, reason):
    decision = assess_interlocks(rig.frame(0), InterlockLimits())
    assert not decision.allowed
    assert reason in decision.reasons


def test_hil_volume_is_calibrated_runtime_product():
    rig = HILRig(pump_a_ml_s=0.8)
    assert rig.delivered_volume(HardwareCommand(PumpChannel.AGENT_A, 10)) == pytest.approx(8.0)


def test_hil_leak_decreases_with_paired_delivery():
    rig = HILRig()
    before = rig.frame(0).leak_ml_min
    after = rig.frame(10, 12, 12).leak_ml_min
    assert after < before


def test_unpaired_agent_does_not_create_synthetic_repair_credit():
    rig = HILRig()
    before = rig.frame(0).leak_ml_min
    after = rig.frame(10, 12, 0).leak_ml_min
    assert after == pytest.approx(before)

@pytest.mark.parametrize("bad", [0, -1])
def test_hardware_command_requires_positive_runtime(bad):
    with pytest.raises(ValueError):
        HardwareCommand(PumpChannel.AGENT_A, bad)


def test_recipe_rejects_impossible_target():
    with pytest.raises(ValueError):
        RepairRecipe("x", 1, 1, 10, 1.1)
