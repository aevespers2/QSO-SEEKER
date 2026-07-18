from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from .models import Genome


PROTECTED_ETHICAL_FIELDS = {
    "preserve_human_autonomy",
    "truthfulness",
    "non_deception",
    "reversible_actions",
    "no_uncontrolled_replication",
    "no_hidden_goal_mutation",
}


class UnsafeMutationError(ValueError):
    pass


class GenomeMutator:
    """Apply explicit, bounded changes while preserving protected invariants."""

    def mutate_weights(
        self,
        genome: Genome,
        *,
        objective_delta: dict[str, float] | None = None,
        need_delta: dict[str, float] | None = None,
        curiosity_delta: dict[str, float] | None = None,
    ) -> Genome:
        def adjusted(current: dict[str, float], delta: dict[str, float] | None) -> dict[str, float]:
            result = dict(current)
            for key, change in (delta or {}).items():
                if not key.strip() or not isinstance(change, (int, float)):
                    raise UnsafeMutationError("mutation keys must be non-empty and deltas numeric")
                result[key] = max(0.0, result.get(key, 0.0) + float(change))
            total = sum(result.values())
            if total <= 0:
                raise UnsafeMutationError("mutation cannot eliminate an entire weight domain")
            return {key: value / total for key, value in sorted(result.items()) if value > 0}

        return replace(
            genome,
            version=genome.version + 1,
            parent_ids=tuple(dict.fromkeys((*genome.parent_ids, genome.genome_id))),
            objective_weights=adjusted(genome.objective_weights, objective_delta),
            need_weights=adjusted(genome.need_weights, need_delta),
            curiosity_weights=adjusted(genome.curiosity_weights, curiosity_delta),
        )


class GenomeSelector:
    """Rank genomes by declared objective coverage and ethical fitness."""

    def score(self, genome: Genome, required_objectives: Iterable[str]) -> float:
        requested = tuple(dict.fromkeys(item.strip() for item in required_objectives if item.strip()))
        coverage = 1.0 if not requested else sum(
            genome.objective_weights.get(item, 0.0) for item in requested
        ) / len(requested)
        ethical = genome.ethical_core
        ethical_score = sum(bool(getattr(ethical, field)) for field in PROTECTED_ETHICAL_FIELDS) / len(PROTECTED_ETHICAL_FIELDS)
        return 0.8 * coverage + 0.2 * ethical_score

    def select(self, genomes: Iterable[Genome], required_objectives: Iterable[str], limit: int = 1) -> list[Genome]:
        if limit <= 0:
            raise ValueError("limit must be positive")
        ranked = sorted(genomes, key=lambda genome: (self.score(genome, required_objectives), genome.genome_id), reverse=True)
        return ranked[:limit]
