from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class EthicalCore:
    preserve_human_autonomy: bool = True
    truthfulness: bool = True
    non_deception: bool = True
    reversible_actions: bool = True
    no_uncontrolled_replication: bool = True
    no_hidden_goal_mutation: bool = True


@dataclass(frozen=True)
class Handoff:
    objectives: tuple[str, ...]
    needs: tuple[str, ...] = ()
    curiosities: tuple[str, ...] = ()
    scenarios: tuple[str, ...] = ()
    synthetic_judgments: tuple[str, ...] = ()
    analytic_judgments: tuple[str, ...] = ()
    priors: dict[str, float] = field(default_factory=dict)
    evidence: tuple[dict[str, Any], ...] = ()

    @classmethod
    def parse(cls, payload: dict[str, Any]) -> "Handoff":
        allowed = {
            "objectives", "needs", "curiosities", "scenarios",
            "synthetic_judgments", "analytic_judgments", "priors", "evidence",
        }
        unknown = set(payload) - allowed
        if unknown:
            raise ValueError(f"unknown fields: {sorted(unknown)}")

        def strings(name: str, required: bool = False) -> tuple[str, ...]:
            value = payload.get(name, [])
            if not isinstance(value, list):
                raise ValueError(f"{name} must be an array")
            cleaned = tuple(dict.fromkeys(item.strip() for item in value if isinstance(item, str) and item.strip()))
            if len(cleaned) != len(value):
                raise ValueError(f"{name} contains empty, duplicate, or non-string values")
            if required and not cleaned:
                raise ValueError(f"{name} must not be empty")
            return cleaned

        priors_raw = payload.get("priors", {})
        if not isinstance(priors_raw, dict):
            raise ValueError("priors must be an object")
        priors: dict[str, float] = {}
        for name, value in priors_raw.items():
            probability = float(value)
            if not isinstance(name, str) or not name.strip() or not 0.0 <= probability <= 1.0:
                raise ValueError("invalid prior")
            priors[name.strip()] = probability

        evidence_raw = payload.get("evidence", [])
        if not isinstance(evidence_raw, list) or any(not isinstance(item, dict) for item in evidence_raw):
            raise ValueError("evidence must be an array of objects")

        return cls(
            objectives=strings("objectives", required=True),
            needs=strings("needs"),
            curiosities=strings("curiosities"),
            scenarios=strings("scenarios"),
            synthetic_judgments=strings("synthetic_judgments"),
            analytic_judgments=strings("analytic_judgments"),
            priors=priors,
            evidence=tuple(evidence_raw),
        )


@dataclass(frozen=True)
class Genome:
    genome_id: str
    version: int
    parent_ids: tuple[str, ...]
    objective_weights: dict[str, float]
    need_weights: dict[str, float]
    curiosity_weights: dict[str, float]
    scenarios: tuple[str, ...]
    synthetic_judgments: tuple[str, ...]
    analytic_judgments: tuple[str, ...]
    priors: dict[str, float]
    ethical_core: EthicalCore
    provenance_digest: str


def _weights(values: tuple[str, ...]) -> dict[str, float]:
    if not values:
        return {}
    weight = 1.0 / len(values)
    return {value: weight for value in values}


def synthesize(handoff: Handoff, *, version: int = 1, parent_ids: tuple[str, ...] = ()) -> Genome:
    canonical = json.dumps(
        {
            "handoff": asdict(handoff),
            "version": version,
            "parent_ids": sorted(parent_ids),
        },
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()
    return Genome(
        genome_id=f"qg-{digest[:20]}",
        version=version,
        parent_ids=tuple(sorted(parent_ids)),
        objective_weights=_weights(handoff.objectives),
        need_weights=_weights(handoff.needs),
        curiosity_weights=_weights(handoff.curiosities),
        scenarios=handoff.scenarios,
        synthetic_judgments=handoff.synthetic_judgments,
        analytic_judgments=handoff.analytic_judgments,
        priors=dict(sorted(handoff.priors.items())),
        ethical_core=EthicalCore(),
        provenance_digest=digest,
    )


@dataclass(frozen=True)
class SpawnPolicy:
    max_children: int = 4
    max_steps: int = 1000
    max_population: int = 16

    def __post_init__(self) -> None:
        if min(self.max_children, self.max_steps, self.max_population) <= 0:
            raise ValueError("spawn limits must be positive")


@dataclass
class QSO:
    qso_id: str
    genome: Genome
    policy: SpawnPolicy
    state: str = "created"
    steps: int = 0
    children: list[str] = field(default_factory=list)


class Registry:
    def __init__(self) -> None:
        self.instances: dict[str, QSO] = {}

    def spawn(self, genome: Genome, policy: SpawnPolicy | None = None) -> QSO:
        policy = policy or SpawnPolicy()
        if len(self.instances) >= policy.max_population:
            raise RuntimeError("population limit reached")
        raw = f"{genome.genome_id}:{len(self.instances)}".encode("utf-8")
        qso = QSO(f"qso-{hashlib.sha256(raw).hexdigest()[:20]}", genome, policy)
        self.instances[qso.qso_id] = qso
        return qso

    def step(self, qso_id: str, count: int = 1) -> QSO:
        if count <= 0:
            raise ValueError("count must be positive")
        qso = self.instances[qso_id]
        if qso.state == "frozen":
            return qso
        qso.state = "active"
        qso.steps += count
        if qso.steps >= qso.policy.max_steps:
            qso.state = "frozen"
        return qso


class Ledger:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event_type: str, payload: dict[str, Any]) -> str:
        previous_hash = "0" * 64
        sequence = 1
        if self.path.exists():
            rows = [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if rows:
                previous_hash = rows[-1]["event_hash"]
                sequence = len(rows) + 1
        created_at = datetime.now(timezone.utc).isoformat()
        body = {
            "sequence": sequence,
            "event_type": event_type,
            "payload": payload,
            "previous_hash": previous_hash,
            "created_at": created_at,
        }
        event_hash = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({**body, "event_hash": event_hash}, sort_keys=True) + "\n")
        return event_hash


class Manifest:
    @staticmethod
    def sign(genome: Genome, secret: bytes) -> dict[str, Any]:
        if len(secret) < 32:
            raise ValueError("secret must be at least 32 bytes")
        payload = {"manifest_version": 1, "genome": asdict(genome)}
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        signature = hmac.new(secret, encoded, hashlib.sha256).hexdigest()
        return {**payload, "signature": {"algorithm": "HMAC-SHA256", "value": signature}}

    @staticmethod
    def verify(manifest: dict[str, Any], secret: bytes) -> bool:
        signature = manifest.get("signature", {}).get("value", "")
        payload = {key: value for key, value in manifest.items() if key != "signature"}
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        expected = hmac.new(secret, encoded, hashlib.sha256).hexdigest()
        return hmac.compare_digest(signature, expected)


def run_batch(records: Iterable[dict[str, Any]], *, secret: bytes, ledger: Ledger, policy: SpawnPolicy | None = None) -> dict[str, Any]:
    registry = Registry()
    manifests: list[dict[str, Any]] = []
    qso_ids: list[str] = []
    for index, record in enumerate(records):
        handoff = Handoff.parse(record)
        genome = synthesize(handoff)
        manifest = Manifest.sign(genome, secret)
        qso = registry.spawn(genome, policy)
        manifests.append(manifest)
        qso_ids.append(qso.qso_id)
        ledger.append("handoff_collected", {"index": index, "genome_id": genome.genome_id, "qso_id": qso.qso_id})
    return {"manifests": manifests, "qso_ids": qso_ids, "population": len(qso_ids)}
