from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable

from .models import Genome, QSOInstance, SpawnPolicy
from .spawn import QSOSpawner


@dataclass(frozen=True)
class ExperimentPolicy:
    max_population: int = 16
    max_total_steps: int = 10_000
    step_batch: int = 1

    def __post_init__(self) -> None:
        if min(self.max_population, self.max_total_steps, self.step_batch) <= 0:
            raise ValueError("experiment limits must be positive")


@dataclass
class ExperimentReport:
    qso_ids: list[str] = field(default_factory=list)
    total_steps: int = 0
    frozen_ids: list[str] = field(default_factory=list)
    stopped_reason: str = "not_started"


class ExperimentRunner:
    """Run a bounded population without autonomous network or tool access."""

    def __init__(self, spawner: QSOSpawner | None = None) -> None:
        self.spawner = spawner or QSOSpawner()

    def run(
        self,
        genomes: Iterable[Genome],
        *,
        spawn_policy: SpawnPolicy | None = None,
        experiment_policy: ExperimentPolicy | None = None,
        evaluator: Callable[[QSOInstance], None] | None = None,
    ) -> ExperimentReport:
        policy = experiment_policy or ExperimentPolicy()
        report = ExperimentReport()
        population: list[QSOInstance] = []

        for genome in genomes:
            if len(population) >= policy.max_population:
                break
            qso = self.spawner.spawn(genome, spawn_policy)
            population.append(qso)
            report.qso_ids.append(qso.qso_id)

        if not population:
            report.stopped_reason = "empty_population"
            return report

        while report.total_steps < policy.max_total_steps:
            active = [qso for qso in population if qso.state not in {"frozen", "retired"}]
            if not active:
                report.stopped_reason = "all_frozen_or_retired"
                break
            for qso in active:
                remaining = policy.max_total_steps - report.total_steps
                if remaining <= 0:
                    break
                count = min(policy.step_batch, remaining)
                self.spawner.step(qso.qso_id, count)
                report.total_steps += count
                if evaluator is not None:
                    evaluator(qso)
                if qso.state == "frozen" and qso.qso_id not in report.frozen_ids:
                    report.frozen_ids.append(qso.qso_id)
        else:
            report.stopped_reason = "step_budget_exhausted"

        if report.stopped_reason == "not_started":
            report.stopped_reason = "step_budget_exhausted"
        return report
