"""Run a deterministic, network-disabled collection rehearsal.

This routine validates the dry-run source registry, sanitizes bounded fixture content,
creates content-addressed canonical records, writes provenance links, prepares
Digital Consciousness Field publication envelopes, and emits an auditable summary.
It performs no external network requests and executes no collected content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "sources.dry-run.json"
DEFAULT_OUTPUT = ROOT / "artifacts" / "dry-run"
MAX_CONTENT_CHARS = 50_000
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
SCRIPT_RE = re.compile(r"<\s*(script|iframe|object|embed)\b.*?>.*?<\s*/\s*\1\s*>", re.I | re.S)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sanitize(content: str) -> tuple[str, list[str]]:
    transformations: list[str] = []
    bounded = content[:MAX_CONTENT_CHARS]
    if bounded != content:
        transformations.append("truncated_to_max_content_chars")
    without_scripts = SCRIPT_RE.sub("", bounded)
    if without_scripts != bounded:
        transformations.append("removed_script_like_markup")
    cleaned = CONTROL_RE.sub("", without_scripts)
    if cleaned != without_scripts:
        transformations.append("removed_control_characters")
    return cleaned, transformations


def validate_registry(registry: dict[str, Any]) -> list[dict[str, Any]]:
    if registry.get("registry_version") != "1.0.0":
        raise ValueError("registry_version must be 1.0.0")
    if registry.get("mode") != "dry-run":
        raise ValueError("registry mode must be dry-run")
    if registry.get("network_enabled") is not False:
        raise ValueError("network_enabled must be false")
    retrieved_at = registry.get("deterministic_retrieved_at")
    if not isinstance(retrieved_at, str) or not retrieved_at:
        raise ValueError("deterministic_retrieved_at is required")
    sources = registry.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources must be a non-empty list")
    seen: set[str] = set()
    for source in sources:
        required = {"source_id", "adapter", "topic", "retention_days", "sensitivity", "purpose", "fixture"}
        missing = sorted(required - set(source))
        if missing:
            raise ValueError(f"source missing required fields: {missing}")
        if source["adapter"] != "mock":
            raise ValueError("dry-run permits only the mock adapter")
        if source["source_id"] in seen:
            raise ValueError(f"duplicate source_id: {source['source_id']}")
        if not isinstance(source["retention_days"], int) or source["retention_days"] < 1:
            raise ValueError(f"source {source['source_id']} has invalid retention_days")
        seen.add(source["source_id"])
        fixture = source["fixture"]
        if not isinstance(fixture, dict) or "content" not in fixture:
            raise ValueError(f"source {source['source_id']} lacks fixture content")
    return sources


def run(config_path: Path, output_dir: Path) -> dict[str, Any]:
    config_text = config_path.read_text(encoding="utf-8")
    registry = json.loads(config_text)
    sources = validate_registry(registry)
    output_dir.mkdir(parents=True, exist_ok=True)
    records_dir = output_dir / "records"
    envelopes_dir = output_dir / "field-envelopes"
    records_dir.mkdir(exist_ok=True)
    envelopes_dir.mkdir(exist_ok=True)

    run_id = sha256_text(canonical_json(registry))[:16]
    retrieved_at = registry["deterministic_retrieved_at"]
    records: list[dict[str, Any]] = []
    envelopes: list[dict[str, Any]] = []
    deduplicated: dict[str, str] = {}

    for source in sources:
        fixture = source["fixture"]
        sanitized, transformations = sanitize(str(fixture["content"]))
        content_hash = sha256_text(sanitized)
        record = {
            "schema_version": "qso-seeker-canonical-record-v1",
            "run_id": run_id,
            "source_id": source["source_id"],
            "repository": fixture.get("repository"),
            "path": fixture.get("path"),
            "source_url": fixture.get("url"),
            "retrieved_at": retrieved_at,
            "adapter": "mock",
            "network_used": False,
            "content_type": source.get("content_type", "text/plain"),
            "content": sanitized,
            "content_sha256": content_hash,
            "transformations": transformations,
            "sensitivity": source["sensitivity"],
            "retention_days": source["retention_days"],
            "purpose": source["purpose"],
            "untrusted_text": True,
            "executable": False,
        }
        record_hash = sha256_text(canonical_json(record))
        record["record_sha256"] = record_hash
        duplicate_of = deduplicated.get(content_hash)
        if duplicate_of:
            record["duplicate_of"] = duplicate_of
        else:
            deduplicated[content_hash] = record_hash
        record_path = records_dir / f"{record_hash}.json"
        record_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
        records.append(record)

        envelope = {
            "schema_version": "digital-consciousness-field-envelope-v1",
            "mode": "dry-run",
            "publisher": "qso-seeker",
            "topic": source["topic"],
            "record_sha256": record_hash,
            "content_sha256": content_hash,
            "sensitivity": source["sensitivity"],
            "purpose": source["purpose"],
            "retention_days": source["retention_days"],
            "capabilities_required": ["field.discover", "evidence.read"],
            "raw_network_payload_available": False,
            "human_review_required": True,
        }
        envelope_hash = sha256_text(canonical_json(envelope))
        envelope["envelope_sha256"] = envelope_hash
        (envelopes_dir / f"{envelope_hash}.json").write_text(
            json.dumps(envelope, indent=2, sort_keys=True), encoding="utf-8"
        )
        envelopes.append(envelope)

    provenance = {
        "schema_version": "qso-seeker-provenance-run-v1",
        "run_id": run_id,
        "config_sha256": sha256_text(config_text),
        "network_used": False,
        "record_hashes": [record["record_sha256"] for record in records],
        "envelope_hashes": [envelope["envelope_sha256"] for envelope in envelopes],
        "pipeline": [
            "registry_validation",
            "mock_retrieval",
            "sanitization",
            "canonicalization",
            "content_addressing",
            "deduplication",
            "field_envelope_preparation",
        ],
    }
    provenance["provenance_sha256"] = sha256_text(canonical_json(provenance))
    (output_dir / "provenance.json").write_text(json.dumps(provenance, indent=2, sort_keys=True), encoding="utf-8")

    summary = {
        "run_id": run_id,
        "status": "pass",
        "mode": "dry-run",
        "network_used": False,
        "source_count": len(sources),
        "record_count": len(records),
        "field_envelope_count": len(envelopes),
        "unique_content_count": len(deduplicated),
        "provenance_sha256": provenance["provenance_sha256"],
        "output_dir": str(output_dir),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run network-disabled QSO-SEEKER collection rehearsal")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    summary = run(args.config, args.output)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
