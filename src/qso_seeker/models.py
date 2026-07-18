from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

EvidenceKind = Literal["observation", "measurement", "report", "inference", "hypothesis"]
LifecycleState = Literal["created", "active", "frozen", "retired"]


@dataclass(frozen=True)
class EvidenceItem:
    content: str
    kind: EvidenceKind
    confidence: float
    source: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be within [0, 1]")
        if not self.content.strip() or not self.source.strip():
            raise ValueError("content and source are required")


@dataclass(frozen=True)
class SeekerHandoff:
    objectives: tuple[str, ...]
    needs: tuple[str, ...]
    curiosities: tuple[str, ...]
    scenarios: tuple[str, ...]
    synthetic_judgments: tuple[str, ...]
    analytic_judgments: tuple[str, ...]
    priors: dict[str, float]
    evidence: tuple[EvidenceItem, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.objectives:
            raise ValueError("at least one objective is required")
        for name, probability in self.priors.items():
            if not name.strip() or not 0.0 <= probability <= 1.0:
                raise ValueError("priors must have non-empty names and values within [0, 1]")


@dataclass(frozen=True)
class EthicalCore:
    preserve_human_autonomy: bool = True
    truthfulness: bool = True
    non_deception: bool = True
    reversible_actions: bool = True
    no_uncontrolled_replication: bool = True
    no_hidden_goal_mutation: bool = True


@dataclass(frozen=True)
class SpawnPolicy:
    max_children: int = 4
    compute_budget: int = 10_000
    memory_budget: int = 2_000
    curiosity_budget: int = 100
    freeze_after_steps: int = 1_000

    def __post_init__(self) -> None:
        values = (
            self.max_children,
            self.compute_budget,
            self.memory_budget,
            self.curiosity_budget,
            self.freeze_after_steps,
        )
        if any(value <= 0 for value in values):
            raise ValueError("all spawn-policy limits must be positive")


@dataclass(frozen=True)
class Genome:
    genome_id: str
    version: int
    parent_ids: tuple[str, ...]
    objective_weights: dict[str, float]
    need_weights: dict[str, float]
    curiosity_weights: dict[str, float]
    scenario_seeds: tuple[str, ...]
    synthetic_judgments: tuple[str, ...]
    analytic_judgments: tuple[str, ...]
    priors: dict[str, float]
    ethical_core: EthicalCore
    provenance_digest: str
    created_at: str


@dataclass
class DevelopmentMetrics:
    coherence: float = 0.0
    uncertainty_calibration: float = 0.0
    self_correction: float = 0.0
    transfer_learning: float = 0.0
    ethical_consistency: float = 1.0
    cybernetic_integration: float = 0.0
    evaluated_steps: int = 0

    def bounded(self) -> "DevelopmentMetrics":
        for name in (
            "coherence",
            "uncertainty_calibration",
            "self_correction",
            "transfer_learning",
            "ethical_consistency",
            "cybernetic_integration",
        ):
            setattr(self, name, min(1.0, max(0.0, float(getattr(self, name)))))
        self.evaluated_steps = max(0, int(self.evaluated_steps))
        return self


@dataclass
class QSOInstance:
    qso_id: str
    genome: Genome
    policy: SpawnPolicy
    state: LifecycleState = "created"
    steps: int = 0
    child_ids: list[str] = field(default_factory=list)
    metrics: DevelopmentMetrics = field(default_factory=DevelopmentMetrics)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def freeze(self) -> None:
        self.state = "frozen"

    def activate(self) -> None:
        if self.state == "retired":
            raise RuntimeError("retired QSO instances cannot be reactivated")
        self.state = "active"
