#!/usr/bin/env python3
"""Validate QSO-SEEKER's documentation-only source-review record.

This validator is intentionally standard-library-only and side-effect-free.
It validates the documentation fixture and request/decision consistency. It
does not grant retrieval, processing, retention, handoff, or publication
authority.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

SCHEMA_ID = "qso-seeker.source-review-record"
SCHEMA_VERSION = 1
DOCUMENTATION_STATUS = "DOCUMENTED_NOT_AUTHORIZED"
DECISION_STATES = {
    "REVIEW_REQUIRED",
    "BOUNDED_RETRIEVAL_APPROVED",
    "SANITIZATION_ONLY",
    "RESTRICTED_PROCESSING",
    "PUBLICATION_REVIEW_REQUIRED",
    "BLOCKED",
    "WITHDRAWN",
    "EXPIRED",
    "SUPERSEDED",
}
OPERATIONS = {"retrieve", "sanitize", "handoff", "publish"}
PRIVACY_RANK = {
    "PUBLIC_SYNTHETIC": 0,
    "INTERNAL": 1,
    "RESTRICTED": 2,
    "SENSITIVE": 3,
    "QUARANTINED": 4,
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
TOP_LEVEL_KEYS = {
    "schema",
    "version",
    "status",
    "review_id",
    "source",
    "request",
    "decision",
    "retention",
    "authority",
    "provenance",
    "supersession",
    "uncertainty",
    "fail_closed_condition",
}
AUTHORITY_KEYS = {
    "retrieval",
    "processing",
    "retention",
    "handoff",
    "publication",
    "credentials",
    "network",
    "repository_write",
}


class RecordValidationError(ValueError):
    """Raised when a review record is malformed or semantically unsafe."""


def _object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RecordValidationError(f"{name} must be an object")
    return value


def _string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecordValidationError(f"{name} must be a non-empty string")
    return value


def _string_list(value: Any, name: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        qualifier = "possibly empty " if allow_empty else ""
        raise RecordValidationError(f"{name} must be a {qualifier}list of strings")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise RecordValidationError(f"{name} contains a non-string or empty value")
    if len(value) != len(set(value)):
        raise RecordValidationError(f"{name} contains duplicate values")
    return value


def _timestamp(value: Any, name: str) -> datetime:
    text = _string(value, name)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RecordValidationError(f"{name} must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RecordValidationError(f"{name} must include a timezone offset")
    return parsed


def _optional_timestamp(value: Any, name: str) -> datetime | None:
    if value is None:
        return None
    return _timestamp(value, name)


def _digest(value: Any, name: str) -> str:
    text = _string(value, name)
    if not SHA256_RE.fullmatch(text):
        raise RecordValidationError(f"{name} must be a lowercase SHA-256 digest")
    return text


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise RecordValidationError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _reject_constant(token: str) -> Any:
    raise RecordValidationError(f"non-standard JSON constant: {token}")


def validate_record(record: dict[str, Any], *, now: datetime | None = None) -> None:
    if set(record) != TOP_LEVEL_KEYS:
        missing = sorted(TOP_LEVEL_KEYS - set(record))
        extra = sorted(set(record) - TOP_LEVEL_KEYS)
        raise RecordValidationError(
            f"top-level keys mismatch; missing={missing}; extra={extra}"
        )

    if record["schema"] != SCHEMA_ID or record["version"] != SCHEMA_VERSION:
        raise RecordValidationError("unsupported source-review record schema or version")
    if record["status"] != DOCUMENTATION_STATUS:
        raise RecordValidationError("record must remain DOCUMENTED_NOT_AUTHORIZED")
    _string(record["review_id"], "review_id")

    source = _object(record["source"], "source")
    if set(source) != {
        "class",
        "locator_policy",
        "terms_snapshot_digest",
        "license_id",
        "contains_private_locator",
    }:
        raise RecordValidationError("source keys mismatch")
    _string(source["class"], "source.class")
    _string(source["locator_policy"], "source.locator_policy")
    _digest(source["terms_snapshot_digest"], "source.terms_snapshot_digest")
    _string(source["license_id"], "source.license_id")
    if source["contains_private_locator"] is not False:
        raise RecordValidationError(
            "documentation fixture must not contain a private locator"
        )

    request = _object(record["request"], "request")
    if set(request) != {
        "purpose",
        "consumer",
        "operation",
        "requested_privacy_class",
        "publication_requested",
    }:
        raise RecordValidationError("request keys mismatch")
    purpose = _string(request["purpose"], "request.purpose")
    consumer = _string(request["consumer"], "request.consumer")
    operation = _string(request["operation"], "request.operation")
    if operation not in OPERATIONS:
        raise RecordValidationError("request.operation is unsupported")
    requested_privacy = _string(
        request["requested_privacy_class"], "request.requested_privacy_class"
    )
    if requested_privacy not in PRIVACY_RANK:
        raise RecordValidationError(
            "request.requested_privacy_class is unsupported"
        )
    if not isinstance(request["publication_requested"], bool):
        raise RecordValidationError("request.publication_requested must be boolean")

    decision = _object(record["decision"], "decision")
    if set(decision) != {
        "state",
        "approved_purpose",
        "allowed_consumers",
        "allowed_operations",
        "output_privacy_class",
        "publication_approved",
        "issued_at",
        "not_before",
        "expires_at",
        "withdrawn_at",
        "owner_role",
        "reviewer_role",
    }:
        raise RecordValidationError("decision keys mismatch")
    state = _string(decision["state"], "decision.state")
    if state not in DECISION_STATES:
        raise RecordValidationError("decision.state is unsupported")
    approved_purpose = _string(
        decision["approved_purpose"], "decision.approved_purpose"
    )
    allowed_consumers = _string_list(
        decision["allowed_consumers"],
        "decision.allowed_consumers",
        allow_empty=True,
    )
    allowed_operations = _string_list(
        decision["allowed_operations"],
        "decision.allowed_operations",
        allow_empty=True,
    )
    if any(item not in OPERATIONS for item in allowed_operations):
        raise RecordValidationError(
            "decision.allowed_operations contains an unsupported operation"
        )
    output_privacy = _string(
        decision["output_privacy_class"], "decision.output_privacy_class"
    )
    if output_privacy not in PRIVACY_RANK:
        raise RecordValidationError("decision.output_privacy_class is unsupported")
    if not isinstance(decision["publication_approved"], bool):
        raise RecordValidationError("decision.publication_approved must be boolean")
    issued_at = _timestamp(decision["issued_at"], "decision.issued_at")
    not_before = _timestamp(decision["not_before"], "decision.not_before")
    expires_at = _timestamp(decision["expires_at"], "decision.expires_at")
    withdrawn_at = _optional_timestamp(
        decision["withdrawn_at"], "decision.withdrawn_at"
    )
    _string(decision["owner_role"], "decision.owner_role")
    _string(decision["reviewer_role"], "decision.reviewer_role")
    if not (issued_at <= not_before < expires_at):
        raise RecordValidationError(
            "decision timestamps must satisfy issued_at <= not_before < expires_at"
        )

    if purpose != approved_purpose:
        raise RecordValidationError("PURPOSE_MISMATCH")
    if consumer not in allowed_consumers:
        raise RecordValidationError("CONSUMER_MISMATCH")
    if operation not in allowed_operations and state not in {
        "REVIEW_REQUIRED",
        "BLOCKED",
    }:
        raise RecordValidationError("OPERATION_NOT_APPROVED")
    if PRIVACY_RANK[output_privacy] < PRIVACY_RANK[requested_privacy]:
        raise RecordValidationError("PRIVACY_DOWNGRADE")
    if request["publication_requested"] and not decision["publication_approved"]:
        raise RecordValidationError("PUBLICATION_NOT_APPROVED")
    if decision["publication_approved"] and "publish" not in allowed_operations:
        raise RecordValidationError(
            "publication approval requires publish in allowed_operations"
        )

    inactive_states = {
        "REVIEW_REQUIRED",
        "BLOCKED",
        "WITHDRAWN",
        "EXPIRED",
        "SUPERSEDED",
        "PUBLICATION_REVIEW_REQUIRED",
    }
    if state in inactive_states and allowed_operations:
        raise RecordValidationError(f"{state} must not retain allowed operations")
    if state in {"WITHDRAWN", "EXPIRED", "SUPERSEDED"} and allowed_consumers:
        raise RecordValidationError(f"{state} must not retain allowed consumers")
    if state == "WITHDRAWN" and withdrawn_at is None:
        raise RecordValidationError("WITHDRAWN requires withdrawn_at")
    if state != "WITHDRAWN" and withdrawn_at is not None:
        raise RecordValidationError("withdrawn_at requires WITHDRAWN state")
    if now is not None:
        if now.tzinfo is None or now.utcoffset() is None:
            raise RecordValidationError("now must be timezone-aware")
        if now < not_before:
            raise RecordValidationError("NOT_YET_VALID")
        if now >= expires_at and state != "EXPIRED":
            raise RecordValidationError("EXPIRED_STATE_REQUIRED")
        if now < expires_at and state == "EXPIRED":
            raise RecordValidationError("EXPIRED state is premature")

    retention = _object(record["retention"], "retention")
    if set(retention) != {
        "max_days",
        "deletion_authority",
        "legal_hold_authority",
    }:
        raise RecordValidationError("retention keys mismatch")
    if (
        not isinstance(retention["max_days"], int)
        or isinstance(retention["max_days"], bool)
        or retention["max_days"] < 0
    ):
        raise RecordValidationError(
            "retention.max_days must be a non-negative integer"
        )
    _string(retention["deletion_authority"], "retention.deletion_authority")
    _string(retention["legal_hold_authority"], "retention.legal_hold_authority")

    authority = _object(record["authority"], "authority")
    if set(authority) != AUTHORITY_KEYS:
        raise RecordValidationError("authority keys mismatch")
    if any(value is not False for value in authority.values()):
        raise RecordValidationError(
            "documentation fixture must deny every authority flag"
        )

    provenance = _object(record["provenance"], "provenance")
    if set(provenance) != {
        "source_digest",
        "decision_evidence_digest",
        "policy_references",
    }:
        raise RecordValidationError("provenance keys mismatch")
    _digest(provenance["source_digest"], "provenance.source_digest")
    _digest(
        provenance["decision_evidence_digest"],
        "provenance.decision_evidence_digest",
    )
    _string_list(provenance["policy_references"], "provenance.policy_references")

    supersession = _object(record["supersession"], "supersession")
    if set(supersession) != {"supersedes", "correction_of"}:
        raise RecordValidationError("supersession keys mismatch")
    for key in ("supersedes", "correction_of"):
        if supersession[key] is not None:
            _string(supersession[key], f"supersession.{key}")

    _string_list(record["uncertainty"], "uncertainty")
    _string(record["fail_closed_condition"], "fail_closed_condition")


def load_record(path: Path) -> dict[str, Any]:
    try:
        text = path.read_bytes().decode("utf-8", errors="strict")
        data = json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except RecordValidationError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RecordValidationError(f"unable to load JSON record: {exc}") from exc
    return _object(data, "record")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--now", help="optional timezone-aware ISO-8601 time")
    args = parser.parse_args()

    now = _timestamp(args.now, "--now") if args.now else None
    try:
        validate_record(load_record(args.record), now=now)
    except RecordValidationError as exc:
        print(f"INVALID: {exc}")
        return 1
    print(f"VALID: {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
