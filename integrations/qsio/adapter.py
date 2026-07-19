"""QSIO integration boundary for QSO-SEEKER."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json, os
from typing import Any, Mapping, Protocol

SCHEMA_VERSION = "qsio.integration.v1"
FEATURE_FLAG = "QSIO_INTEGRATION_ENABLED"

def canonical_json(v: Mapping[str, Any]) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def content_hash(v: Mapping[str, Any]) -> str:
    return "sha256:" + sha256(canonical_json(v).encode()).hexdigest()

@dataclass(frozen=True)
class CompatibilityReport:
    compatible: bool
    schema_version: str = SCHEMA_VERSION
    unsupported_mappings: tuple[str, ...] = ()

@dataclass(frozen=True)
class LocalApplicationResult:
    applied: bool
    canonical_id: str
    record_hash: str
    reason: str | None = None

class QSIOAdapter(Protocol):
    def describe_local_entity(self, local_id: str) -> Mapping[str, Any]: ...
    def to_qsi(self, local_event: object) -> Mapping[str, Any]: ...
    def apply_qsio(self, qsio: Mapping[str, Any]) -> LocalApplicationResult: ...
    def verify_compatibility(self) -> CompatibilityReport: ...

class SeekerQSIOAdapter:
    repository = "qso-seeker"
    @staticmethod
    def enabled() -> bool:
        return os.getenv(FEATURE_FLAG, "false").lower() in {"1","true","yes","on"}
    def describe_local_entity(self, local_id: str) -> Mapping[str, Any]:
        return {"schema_version": SCHEMA_VERSION, "canonical_id": f"qso:seeker:{local_id}", "local_id": local_id, "entity_type": "observer"}
    def to_qsi(self, local_event: object) -> Mapping[str, Any]:
        p = local_event if isinstance(local_event, Mapping) else vars(local_event)
        qsi = {"schema_version": SCHEMA_VERSION, "kind": "QSI", "source": self.repository, "action": p.get("action", "observation.submit"), "subject": p.get("canonical_id") or f"qso:seeker:{p['local_id']}", "payload": dict(p), "epistemic": {"status": p.get("epistemic_status", "unverified"), "confidence": p.get("confidence")}, "evidence": tuple(p.get("evidence", ())), "capabilities": tuple(p.get("capabilities", ())) }
        return {**qsi, "content_hash": content_hash(qsi)}
    def apply_qsio(self, qsio: Mapping[str, Any]) -> LocalApplicationResult:
        if not self.enabled(): return LocalApplicationResult(False, str(qsio.get("subject","unknown")), "", "feature_disabled")
        if qsio.get("kind") != "QSIO" or qsio.get("schema_version") != SCHEMA_VERSION: return LocalApplicationResult(False, str(qsio.get("subject","unknown")), "", "incompatible_record")
        supplied = str(qsio.get("content_hash", "")); expected = content_hash({k:v for k,v in qsio.items() if k != "content_hash"})
        return LocalApplicationResult(supplied == expected, str(qsio.get("subject","unknown")), supplied, None if supplied == expected else "hash_mismatch")
    def verify_compatibility(self) -> CompatibilityReport:
        return CompatibilityReport(True, unsupported_mappings=("hypotheses remain proposals until witnessed by QSIO",))
