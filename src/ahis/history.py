"""Hash-chained lifetime structural history."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json


GENESIS = "0" * 64


@dataclass(frozen=True, slots=True)
class StructuralEvent:
    sequence: int
    event_type: str
    timestamp_utc: str
    payload: dict[str, object]
    previous_hash: str
    event_hash: str


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _hash_event(sequence: int, event_type: str, timestamp_utc: str, payload: dict[str, object], previous_hash: str) -> str:
    return sha256(_canonical({
        "sequence": sequence,
        "event_type": event_type,
        "timestamp_utc": timestamp_utc,
        "payload": payload,
        "previous_hash": previous_hash,
    })).hexdigest()


class StructuralHistory:
    def __init__(self) -> None:
        self._events: list[StructuralEvent] = []

    @property
    def events(self) -> tuple[StructuralEvent, ...]:
        return tuple(self._events)

    def append(self, event_type: str, timestamp_utc: str, payload: dict[str, object]) -> StructuralEvent:
        if not event_type.strip() or not timestamp_utc.strip():
            raise ValueError("event_type and timestamp_utc are required")
        previous = self._events[-1].event_hash if self._events else GENESIS
        seq = len(self._events)
        digest = _hash_event(seq, event_type, timestamp_utc, payload, previous)
        event = StructuralEvent(seq, event_type, timestamp_utc, dict(payload), previous, digest)
        self._events.append(event)
        return event

    def verify(self) -> tuple[str, ...]:
        errors: list[str] = []
        expected_prev = GENESIS
        for idx, event in enumerate(self._events):
            if event.sequence != idx:
                errors.append(f"sequence mismatch at {idx}")
            if event.previous_hash != expected_prev:
                errors.append(f"previous hash mismatch at {idx}")
            expected = _hash_event(event.sequence, event.event_type, event.timestamp_utc, event.payload, event.previous_hash)
            if event.event_hash != expected:
                errors.append(f"event hash mismatch at {idx}")
            expected_prev = event.event_hash
        return tuple(errors)

    def as_records(self) -> list[dict[str, object]]:
        return [asdict(e) for e in self._events]
