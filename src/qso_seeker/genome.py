from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from .models import EthicalCore, Genome, SeekerHandoff


def _normalize_weights(values: tuple[str, ...]) -> dict[str, float]:
    clean = tuple(dict.fromkeys(value.strip() for value in values if value.strip()))
    if not clean:
        return {}
    weight = 1.0 / len(clean)
    return {value: weight for value in clean}


class GenomeSynthesizer:
    """Generate reproducible genomes from a validated Seeker handoff."""

    def synthesize(
        self,
        handoff: SeekerHandoff,
        *,
        version: int = 1,
        parent_ids: tuple[str, ...] = (),
        salt: str = "qso-seeker-v1",
    ) -> Genome:
        handoff.validate()
        if version <= 0:
            raise ValueError("version must be positive")

        canonical = {
            "objectives": sorted(handoff.objectives),
            "needs": sorted(handoff.needs),
            "curiosities": sorted(handoff.curiosities),
            "scenarios": sorted(handoff.scenarios),
            "synthetic_judgments": sorted(handoff.synthetic_judgments),
            "analytic_judgments": sorted(handoff.analytic_judgments),
            "priors": dict(sorted(handoff.priors.items())),
            "evidence": [
                {
                    "content": item.content,
                    "kind": item.kind,
                    "confidence": item.confidence,
                    "source": item.source,
                }
                for item in handoff.evidence
            ],
            "metadata": handoff.metadata,
            "version": version,
            "parent_ids": sorted(parent_ids),
            "salt": salt,
        }
        encoded = json.dumps(canonical, sort_keys=True, separators=(",", ":"), default=str).encode()
        digest = hashlib.sha256(encoded).hexdigest()

        return Genome(
            genome_id=f"qg-{digest[:20]}",
            version=version,
            parent_ids=tuple(sorted(parent_ids)),
            objective_weights=_normalize_weights(handoff.objectives),
            need_weights=_normalize_weights(handoff.needs),
            curiosity_weights=_normalize_weights(handoff.curiosities),
            scenario_seeds=tuple(dict.fromkeys(handoff.scenarios)),
            synthetic_judgments=tuple(dict.fromkeys(handoff.synthetic_judgments)),
            analytic_judgments=tuple(dict.fromkeys(handoff.analytic_judgments)),
            priors=dict(sorted(handoff.priors.items())),
            ethical_core=EthicalCore(),
            provenance_digest=digest,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
