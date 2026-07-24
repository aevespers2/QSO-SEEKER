from __future__ import annotations

import json
import re
from collections.abc import Collection, Mapping
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from .contracts import canonical_json_bytes, sha256_hex

HANDOFF_CONTRACT = "qso-seeker.retrieval-artifact"
HANDOFF_SCHEMA_VERSION = 1
JSON_MEDIA_TYPE = "application/json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
HANDOFF_ID_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


class HandoffError(ValueError):
    """Raised when a retrieval artifact cannot cross the sanitizer boundary."""


def _reject_constant(value: str) -> None:
    raise HandoffError(f"non-standard JSON number: {value}")


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise HandoffError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _strict_json_loads(data: bytes) -> Any:
    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise HandoffError("artifact must be strict UTF-8 JSON") from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_constant,
        )
    except HandoffError:
        raise
    except json.JSONDecodeError as exc:
        raise HandoffError("artifact must be valid JSON") from exc


def _require_relative_name(value: Any) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise HandoffError("artifact_name must be a non-empty relative path")
    normalized = value.replace("\\", "/")
    if value.startswith(("/", "\\")) or any(part in {"", ".", ".."} for part in normalized.split("/")):
        raise HandoffError("artifact_name must be normalized and relative")
    return value


def _require_sha256(value: Any, name: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise HandoffError(f"{name} must be lowercase SHA-256")
    return value


def _parse_timestamp(value: Any, name: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise HandoffError(f"{name} must be an RFC 3339 timestamp")
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise HandoffError(f"{name} must be an RFC 3339 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise HandoffError(f"{name} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _manifest_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    payload = deepcopy(dict(manifest))
    payload.pop("handoff_id", None)
    return payload


def build_handoff_manifest(
    *,
    producer: str,
    artifact_name: str,
    artifact_bytes: bytes,
    produced_at: str,
    expires_at: str,
) -> dict[str, Any]:
    if not isinstance(producer, str) or not producer:
        raise HandoffError("producer must be a non-empty string")
    _require_relative_name(artifact_name)
    if not isinstance(artifact_bytes, bytes):
        raise HandoffError("artifact_bytes must be bytes")
    produced = _parse_timestamp(produced_at, "produced_at")
    expires = _parse_timestamp(expires_at, "expires_at")
    if expires <= produced:
        raise HandoffError("expires_at must be later than produced_at")

    manifest: dict[str, Any] = {
        "contract": HANDOFF_CONTRACT,
        "schema_version": HANDOFF_SCHEMA_VERSION,
        "handoff_id": "",
        "producer": producer,
        "artifact_name": artifact_name,
        "media_type": JSON_MEDIA_TYPE,
        "artifact_size": len(artifact_bytes),
        "artifact_sha256": sha256_hex(artifact_bytes),
        "produced_at": produced_at,
        "expires_at": expires_at,
    }
    manifest["handoff_id"] = "sha256:" + sha256_hex(canonical_json_bytes(_manifest_payload(manifest)))
    return manifest


def verify_retrieval_handoff(
    artifact_bytes: bytes | None,
    manifest: Mapping[str, Any],
    *,
    expected_producer: str,
    now: datetime,
    max_bytes: int = 1_000_000,
    seen_handoff_ids: Collection[str] = (),
) -> list[Any]:
    """Verify artifact identity and policy before any JSON payload parsing.

    The caller supplies replay state. This function does not mutate external state,
    access a network, read credentials, or execute artifact content.
    """

    required = {
        "contract",
        "schema_version",
        "handoff_id",
        "producer",
        "artifact_name",
        "media_type",
        "artifact_size",
        "artifact_sha256",
        "produced_at",
        "expires_at",
    }
    if not isinstance(manifest, Mapping) or set(manifest) != required:
        raise HandoffError("manifest fields do not match retrieval-artifact v1")
    if manifest["contract"] != HANDOFF_CONTRACT:
        raise HandoffError("unsupported handoff contract")
    if isinstance(manifest["schema_version"], bool) or manifest["schema_version"] != HANDOFF_SCHEMA_VERSION:
        raise HandoffError("unsupported handoff schema_version")
    if not isinstance(expected_producer, str) or not expected_producer:
        raise HandoffError("expected_producer must be a non-empty string")
    if manifest["producer"] != expected_producer:
        raise HandoffError("wrong artifact producer")
    _require_relative_name(manifest["artifact_name"])
    if manifest["media_type"] != JSON_MEDIA_TYPE:
        raise HandoffError("artifact media_type must be application/json")

    handoff_id = manifest["handoff_id"]
    if not isinstance(handoff_id, str) or not HANDOFF_ID_RE.fullmatch(handoff_id):
        raise HandoffError("handoff_id must be a domain-separated SHA-256 identity")
    expected_handoff_id = "sha256:" + sha256_hex(canonical_json_bytes(_manifest_payload(manifest)))
    if handoff_id != expected_handoff_id:
        raise HandoffError("handoff_id mismatch")
    if handoff_id in seen_handoff_ids:
        raise HandoffError("replayed handoff")

    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes <= 0:
        raise HandoffError("max_bytes must be a positive integer")
    declared_size = manifest["artifact_size"]
    if isinstance(declared_size, bool) or not isinstance(declared_size, int) or declared_size < 0:
        raise HandoffError("artifact_size must be a non-negative integer")
    if declared_size > max_bytes:
        raise HandoffError("artifact exceeds maximum size")
    if artifact_bytes is None:
        raise HandoffError("artifact is missing")
    if not isinstance(artifact_bytes, bytes):
        raise HandoffError("artifact must be bytes")
    if len(artifact_bytes) > max_bytes:
        raise HandoffError("artifact exceeds maximum size")
    if len(artifact_bytes) != declared_size:
        raise HandoffError("artifact_size mismatch")
    expected_digest = _require_sha256(manifest["artifact_sha256"], "artifact_sha256")
    if sha256_hex(artifact_bytes) != expected_digest:
        raise HandoffError("artifact_sha256 mismatch")

    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        raise HandoffError("now must be timezone-aware")
    current = now.astimezone(timezone.utc)
    produced = _parse_timestamp(manifest["produced_at"], "produced_at")
    expires = _parse_timestamp(manifest["expires_at"], "expires_at")
    if expires <= produced:
        raise HandoffError("expires_at must be later than produced_at")
    if current < produced:
        raise HandoffError("artifact is not yet valid")
    if current >= expires:
        raise HandoffError("artifact is stale")

    payload = _strict_json_loads(artifact_bytes)
    if not isinstance(payload, list):
        raise HandoffError("retrieval artifact must contain a JSON array")
    return payload
