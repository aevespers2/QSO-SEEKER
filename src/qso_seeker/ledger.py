from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class LedgerEvent:
    sequence: int
    event_type: str
    payload: dict[str, Any]
    previous_hash: str
    event_hash: str
    created_at: str


class EventLedger:
    """Append-only hash-chained JSONL ledger."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _events(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows

    def append(self, event_type: str, payload: dict[str, Any]) -> LedgerEvent:
        if not event_type.strip():
            raise ValueError("event_type is required")
        events = self._events()
        previous_hash = events[-1]["event_hash"] if events else "0" * 64
        sequence = len(events) + 1
        created_at = datetime.now(timezone.utc).isoformat()
        canonical = json.dumps(
            {
                "sequence": sequence,
                "event_type": event_type,
                "payload": payload,
                "previous_hash": previous_hash,
                "created_at": created_at,
            },
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
        event_hash = hashlib.sha256(canonical).hexdigest()
        event = LedgerEvent(sequence, event_type, payload, previous_hash, event_hash, created_at)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(event), sort_keys=True, default=str) + "\n")
        return event

    def verify(self) -> bool:
        previous_hash = "0" * 64
        for expected_sequence, row in enumerate(self._events(), start=1):
            if row.get("sequence") != expected_sequence or row.get("previous_hash") != previous_hash:
                return False
            canonical = json.dumps(
                {
                    "sequence": row["sequence"],
                    "event_type": row["event_type"],
                    "payload": row["payload"],
                    "previous_hash": row["previous_hash"],
                    "created_at": row["created_at"],
                },
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            ).encode("utf-8")
            if hashlib.sha256(canonical).hexdigest() != row.get("event_hash"):
                return False
            previous_hash = row["event_hash"]
        return True
