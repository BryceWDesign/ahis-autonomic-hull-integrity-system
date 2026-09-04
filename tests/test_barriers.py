import pytest
from ahis.barriers import Barrier, BarrierNetwork, BoundaryObservation


def net():
    return BarrierNetwork([Barrier("b1",True,True,True), Barrier("b2",True,True,False), Barrier("b3",True,True,True), Barrier("skin",False,True,True)])


def obs(**leaks):
    return [BoundaryObservation(k, leaks.get(k,0), 1.0) for k in ("b1","b2","b3","skin")]


def test_single_isolatable_fault_contained():
    a = net().assess(obs(b1=2))
    assert a.containment_intact
    assert a.isolate_barriers == ("b1",)


def test_multiple_structural_faults_still_not_claimed_as_nominal():
    a = net().assess(obs(b1=2,b2=2))
    assert a.structural_failures == ("b1","b2")
    assert a.isolate_barriers == ("b1",)


def test_monitor_loss_can_fail_closed():
    a = net().assess([BoundaryObservation("b1",0,1), BoundaryObservation("b2",0,1,False), BoundaryObservation("b3",0,1,False), BoundaryObservation("skin",0,1)])
    assert not a.containment_intact


def test_unknown_barrier_rejected():
    with pytest.raises(ValueError):
        net().assess([BoundaryObservation("bogus",0,1)])


def test_duplicate_ids_rejected():
    with pytest.raises(ValueError):
        BarrierNetwork([Barrier("x",True,True,True), Barrier("x",True,True,True)])
