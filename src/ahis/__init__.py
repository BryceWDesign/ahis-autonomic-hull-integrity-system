"""AHIS v2 autonomic integrity research package."""

from .damage import DamageEstimate, SensorReading, localize_event
from .healing import DamageCase, HealingMechanism, HealingDecision, select_healing_response
from .barriers import Barrier, BarrierNetwork, BoundaryObservation
from .mission import AutonomicIntegrityManager, IntegrityState, MissionDecision
from .verification import VerificationChannel, VerificationResult, VerificationVerdict, verify_repair

__all__ = [
    "DamageEstimate",
    "SensorReading",
    "localize_event",
    "DamageCase",
    "HealingMechanism",
    "HealingDecision",
    "select_healing_response",
    "Barrier",
    "BarrierNetwork",
    "BoundaryObservation",
    "AutonomicIntegrityManager",
    "IntegrityState",
    "MissionDecision",
    "VerificationChannel",
    "VerificationResult",
    "VerificationVerdict",
    "verify_repair",
]

__version__ = "2.0.0"
