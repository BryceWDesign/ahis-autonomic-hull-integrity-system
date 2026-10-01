"""Evidence-gated preservation, repair and limited-recovery state transitions."""

from enum import Enum


class State(str, Enum):
    NOMINAL = "NOMINAL"
    PRESERVATION = "PRESERVATION"
    CONTAINED = "CONTAINED"
    REPAIRING = "REPAIRING"
    VERIFYING = "VERIFYING"
    RECOVERED_LIMITED = "RECOVERED_LIMITED"
    ISOLATED = "ISOLATED"


class SurvivalMachine:
    def __init__(self):
        self.state = State.NOMINAL
        self.history = []

    def advance(self, event):
        transitions = {
            (State.NOMINAL, "stress"): State.PRESERVATION,
            (State.PRESERVATION, "containment_confirmed"): State.CONTAINED,
            (State.CONTAINED, "plan_accepted"): State.REPAIRING,
            (State.REPAIRING, "response_recorded"): State.VERIFYING,
            (State.VERIFYING, "held_out_pass"): State.RECOVERED_LIMITED,
        }
        old = self.state
        if event in {
            "interlock_denied",
            "plan_rejected",
            "verification_failed",
            "accounting_failed",
            "evidence_failed",
        }:
            self.state = State.ISOLATED
        elif (old, event) in transitions:
            self.state = transitions[old, event]
        else:
            raise ValueError("illegal survival transition: " + old.value + "/" + event)
        self.history.append({"from": old.value, "event": event, "to": self.state.value})
        return self.state
