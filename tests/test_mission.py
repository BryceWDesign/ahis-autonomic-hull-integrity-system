from ahis.barriers import BarrierAssessment
from ahis.damage import DamageEstimate
from ahis.healing import HealingDecision, HealingMechanism
from ahis.mission import AutonomicIntegrityManager, IntegrityState


def damage(detected=True):
    return DamageEstimate(detected,.2 if detected else None,.2 if detected else None,.01 if detected else None,1e-6 if detected else None,5,.9 if detected else 0,"x")


def barriers(ok=True, unobs=()):
    return BarrierAssessment(ok, ("seal",), tuple(unobs), (), "x")


def heal(ok=True):
    return HealingDecision(HealingMechanism.IONOMER_PUNCTURE_SEAL if ok else HealingMechanism.NONE,ok,ok,0,True,"x")


def test_nominal():
    d=AutonomicIntegrityManager().decide(damage=damage(False),barriers=barriers(),healing=heal(False),post_heal_verification_passed=None)
    assert d.state is IntegrityState.NOMINAL and d.return_to_service_allowed


def test_healing_never_immediately_returns_service():
    d=AutonomicIntegrityManager().decide(damage=damage(),barriers=barriers(),healing=heal(),post_heal_verification_passed=None)
    assert d.state is IntegrityState.HEALING and not d.return_to_service_allowed


def test_verified_repair_still_externally_gated():
    d=AutonomicIntegrityManager().decide(damage=damage(),barriers=barriers(),healing=heal(),post_heal_verification_passed=True)
    assert d.state is IntegrityState.RECOVERED_LIMITED and not d.return_to_service_allowed


def test_failed_verification_degrades():
    d=AutonomicIntegrityManager().decide(damage=damage(),barriers=barriers(),healing=heal(),post_heal_verification_passed=False)
    assert d.state is IntegrityState.DEGRADED_SAFE


def test_no_healing_lane_degrades():
    d=AutonomicIntegrityManager().decide(damage=damage(),barriers=barriers(),healing=heal(False),post_heal_verification_passed=None)
    assert d.state is IntegrityState.DEGRADED_SAFE


def test_containment_failure_dominates():
    d=AutonomicIntegrityManager().decide(damage=damage(),barriers=barriers(False),healing=heal(),post_heal_verification_passed=None)
    assert d.state is IntegrityState.DEGRADED_SAFE and not d.activate_healing
