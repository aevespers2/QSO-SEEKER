from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .models import EvidenceItem, SeekerHandoff


class HandoffValidationError(ValueError):
    pass


def _strings(value: Any, field: str, *, required: bool = False) -> tuple[str, ...]:
    if value is None:
        value = []
    if not isinstance(value, list):
        raise HandoffValidationError(f"{field} must be an array")
    cleaned = tuple(dict.fromkeys(item.strip() for item in value if isinstance(item, str) and item.strip()))
    if required and not cleaned:
        raise HandoffValidationError(f"{field} must contain at least one non-empty string")
    if len(cleaned) != len(value):
        raise HandoffValidationError(f"{field} contains duplicates, non-strings, or empty values")
    return cleaned


def parse_handoff(payload: Mapping[str, Any]) -> SeekerHandoff:
    allowed = {
        "objectives", "needs", "curiosities", "scenarios", "synthetic_judgments",
        "analytic_judgments", "priors", "evidence", "metadata",
    }
    unknown = set(payload) - allowed
    if unknown:
        raise HandoffValidationError(f"unknown handoff fields: {sorted(unknown)}")

    priors_raw = payload.get("priors", {})
    if not isinstance(priors_raw, dict):
        raise HandoffValidationError("priors must be an object")
    priors: dict[str, float] = {}
    for key, value in priors_raw.items():
        if not isinstance(key, str) or not key.strip() or not isinstance(value, (int, float)):
            raise HandoffValidationError("prior names must be non-empty strings and values numeric")
        probability = float(value)
        if not 0.0 <= probability <= 1.0:
            raise HandoffValidationError(f"prior {key!r} must be within [0, 1]")
        priors[key.strip()] = probability

    evidence: list[EvidenceItem] = []
    evidence_raw = payload.get("evidence", [])
    if not isinstance(evidence_raw, list):
        raise HandoffValidationError("evidence must be an array")
    for index, item in enumerate(evidence_raw):
        if not isinstance(item, dict):
            raise HandoffValidationError(f"evidence[{index}] must be an object")
        try:
            evidence.append(EvidenceItem(
                content=str(item["content"]),
                kind=item["kind"],
                confidence=float(item["confidence"]),
                source=str(item["source"]),
            ))
        except (KeyError, TypeError, ValueError) as exc:
            raise HandoffValidationError(f"invalid evidence[{index}]: {exc}") from exc

    metadata = payload.get("metadata", {})
    if not isinstance(metadata, dict):
        raise HandoffValidationError("metadata must be an object")

    handoff = SeekerHandoff(
        objectives=_strings(payload.get("objectives"), "objectives", required=True),
        needs=_strings(payload.get("needs"), "needs"),
        curiosities=_strings(payload.get("curiosities"), "curiosities"),
        scenarios=_strings(payload.get("scenarios"), "scenarios"),
        synthetic_judgments=_strings(payload.get("synthetic_judgments"), "synthetic_judgments"),
        analytic_judgments=_strings(payload.get("analytic_judgments"), "analytic_judgments"),
        priors=priors,
        evidence=tuple(evidence),
        metadata=metadata,
    )
    handoff.validate()
    return handoff


def load_handoff(path: str | Path) -> SeekerHandoff:
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HandoffValidationError(f"unable to load handoff {source}: {exc}") from exc
    if not isinstance(payload, dict):
        raise HandoffValidationError("handoff root must be an object")
    return parse_handoff(payload)
