from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any, Mapping
from urllib.parse import urlparse

CANONICAL_RECORD_CONTRACT = "qso-seeker.canonical-record"
ATTRIBUTION_CONTRACT = "qso-seeker.attribution-sidecar"
SCHEMA_VERSION = 1
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_KINDS = {"description", "file", "release", "issue", "pull_request", "commit"}


class ContractError(ValueError):
    pass


def _canonicalize(value: Any) -> Any:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, str):
        value.encode("utf-8", "strict")
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise ContractError("non-finite number")
        return value
    if isinstance(value, list):
        return [_canonicalize(item) for item in value]
    if isinstance(value, Mapping):
        out: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ContractError("object keys must be strings")
            key.encode("utf-8", "strict")
            out[key] = _canonicalize(item)
        return out
    raise ContractError(f"unsupported value: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        _canonicalize(value),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8", "strict")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _require_hash(value: Any, name: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise ContractError(f"{name} must be lowercase SHA-256")
    return value


def _require_sorted_unique_strings(value: Any, name: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ContractError(f"{name} must be an array of non-empty strings")
    if value != sorted(set(value)):
        raise ContractError(f"{name} must be sorted and unique")
    return list(value)


def _validate_relative_path(value: Any) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ContractError("path must be a non-empty relative path")
    if value.startswith(("/", "\\")) or any(part in {"", ".", ".."} for part in value.replace("\\", "/").split("/")):
        raise ContractError("path must be normalized and relative")
    return value


def _validate_https_url(value: Any) -> str:
    if not isinstance(value, str):
        raise ContractError("source_url must be a string")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ContractError("source_url must be HTTPS")
    return value


def validate_canonical_record(record: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(record, Mapping):
        raise ContractError("record must be an object")
    required = {
        "contract", "schema_version", "record_id", "repository", "path", "source_url",
        "source_kind", "content", "content_sha256", "transformations", "flags", "provenance",
    }
    if set(record) != required:
        raise ContractError("record fields do not match canonical-record v1")
    if record["contract"] != CANONICAL_RECORD_CONTRACT:
        raise ContractError("unsupported contract")
    if isinstance(record["schema_version"], bool) or record["schema_version"] != SCHEMA_VERSION:
        raise ContractError("unsupported schema_version")
    if not isinstance(record["repository"], str) or not record["repository"]:
        raise ContractError("repository must be a non-empty string")
    _validate_relative_path(record["path"])
    _validate_https_url(record["source_url"])
    if record["source_kind"] not in SOURCE_KINDS:
        raise ContractError("unsupported source_kind")
    content = record["content"]
    if not isinstance(content, str):
        raise ContractError("content must be a string")
    content_bytes = content.encode("utf-8", "strict")
    expected_content_hash = sha256_hex(content_bytes)
    if _require_hash(record["content_sha256"], "content_sha256") != expected_content_hash:
        raise ContractError("content_sha256 mismatch")
    _require_sorted_unique_strings(record["transformations"], "transformations")
    _require_sorted_unique_strings(record["flags"], "flags")
    provenance = record["provenance"]
    if not isinstance(provenance, Mapping) or set(provenance) != {"collector", "collected_at", "source_sha256"}:
        raise ContractError("invalid provenance")
    if not isinstance(provenance["collector"], str) or not provenance["collector"]:
        raise ContractError("invalid provenance collector")
    if not isinstance(provenance["collected_at"], str) or not provenance["collected_at"]:
        raise ContractError("invalid provenance timestamp")
    _require_hash(provenance["source_sha256"], "source_sha256")
    payload = deepcopy(dict(record))
    record_id = payload.pop("record_id")
    expected_id = "sha256:" + sha256_hex(canonical_json_bytes(payload))
    if record_id != expected_id:
        raise ContractError("record_id mismatch")
    return deepcopy(dict(record))


def build_canonical_record(*, repository: str, path: str, source_url: str, source_kind: str,
                           content: str, transformations: list[str], flags: list[str],
                           collector: str, collected_at: str, source_bytes: bytes) -> dict[str, Any]:
    record: dict[str, Any] = {
        "contract": CANONICAL_RECORD_CONTRACT,
        "schema_version": SCHEMA_VERSION,
        "record_id": "",
        "repository": repository,
        "path": path,
        "source_url": source_url,
        "source_kind": source_kind,
        "content": content,
        "content_sha256": sha256_hex(content.encode("utf-8", "strict")),
        "transformations": sorted(set(transformations)),
        "flags": sorted(set(flags)),
        "provenance": {
            "collector": collector,
            "collected_at": collected_at,
            "source_sha256": sha256_hex(source_bytes),
        },
    }
    payload = deepcopy(record)
    payload.pop("record_id")
    record["record_id"] = "sha256:" + sha256_hex(canonical_json_bytes(payload))
    return validate_canonical_record(record)


def validate_attribution_sidecar(sidecar: Mapping[str, Any]) -> dict[str, Any]:
    required = {"contract", "schema_version", "record_id", "source", "author", "license", "sidecar_sha256"}
    if not isinstance(sidecar, Mapping) or set(sidecar) != required:
        raise ContractError("invalid attribution sidecar fields")
    if sidecar["contract"] != ATTRIBUTION_CONTRACT:
        raise ContractError("unsupported attribution contract")
    if isinstance(sidecar["schema_version"], bool) or sidecar["schema_version"] != SCHEMA_VERSION:
        raise ContractError("unsupported attribution schema_version")
    if not isinstance(sidecar["record_id"], str) or not sidecar["record_id"].startswith("sha256:"):
        raise ContractError("invalid bound record_id")
    for field in ("source", "author", "license"):
        if sidecar[field] is not None and not isinstance(sidecar[field], str):
            raise ContractError(f"{field} must be string or null")
    payload = deepcopy(dict(sidecar))
    actual = payload.pop("sidecar_sha256")
    expected = sha256_hex(canonical_json_bytes(payload))
    if _require_hash(actual, "sidecar_sha256") != expected:
        raise ContractError("sidecar_sha256 mismatch")
    return deepcopy(dict(sidecar))
