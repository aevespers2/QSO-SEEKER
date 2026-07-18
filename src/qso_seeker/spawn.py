from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from .models import Genome, QSOInstance, SpawnPolicy


@dataclass
class QSORegistry:
    instances: dict[str, QSOInstance] = field(default_factory=dict)

    def add(self, instance: QSOInstance) -> None:
        if instance.qso_id in self.instances:
            raise ValueError(f"duplicate QSO id: {instance.qso_id}")
        self.instances[instance.qso_id] = instance

    def get(self, qso_id: str) -> QSOInstance:
        try:
            return self.instances[qso_id]
        except KeyError as exc:
            raise KeyError(f"unknown QSO id: {qso_id}") from exc


class QSOSpawner:
    def __init__(self, registry: QSORegistry | None = None) -> None:
        self.registry = registry or QSORegistry()

    def spawn(self, genome: Genome, policy: SpawnPolicy | None = None) -> QSOInstance:
        policy = policy or SpawnPolicy()
        index = len(self.registry.instances)
        raw = f"{genome.genome_id}:{index}".encode()
        qso_id = f"qso-{hashlib.sha256(raw).hexdigest()[:20]}"
        instance = QSOInstance(qso_id=qso_id, genome=genome, policy=policy)
        self.registry.add(instance)
        return instance

    def spawn_child(self, parent_id: str, genome: Genome) -> QSOInstance:
        parent = self.registry.get(parent_id)
        if parent.state in {"frozen", "retired"}:
            raise RuntimeError("frozen or retired QSO instances cannot spawn children")
        if len(parent.child_ids) >= parent.policy.max_children:
            raise RuntimeError("parent child limit reached")
        child = self.spawn(genome, parent.policy)
        parent.child_ids.append(child.qso_id)
        return child

    def step(self, qso_id: str, count: int = 1) -> QSOInstance:
        if count <= 0:
            raise ValueError("step count must be positive")
        instance = self.registry.get(qso_id)
        if instance.state == "retired":
            raise RuntimeError("retired QSO instances cannot advance")
        if instance.state == "frozen":
            return instance
        instance.activate()
        instance.steps += count
        instance.metrics.evaluated_steps += count
        if instance.steps >= instance.policy.freeze_after_steps:
            instance.freeze()
        return instance
