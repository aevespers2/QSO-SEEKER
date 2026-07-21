from copy import deepcopy
from datetime import datetime, timezone

import pytest

import unicernal_search.handoff as handoff
from unicernal_search.handoff import (
    HandoffError,
    build_handoff_manifest,
    verify_retrieval_handoff,
)


NOW = datetime(2026, 7, 21, 22, 0, tzinfo=timezone.utc)
PRODUCED = "2026-07-21T21:55:00Z"
EXPIRES = "2026-07-21T22:05:00Z"


def artifact_bytes() -> bytes:
    return b'[{"content":"inert text","path":"README.md","repository":"example/project"}]'


def manifest(data: bytes | None = None):
    payload = artifact_bytes() if data is None else data
    return build_handoff_manifest(
        producer="retriever-v1",
        artifact_name="retrieval/input.json",
        artifact_bytes=payload,
        produced_at=PRODUCED,
        expires_at=EXPIRES,
    )


def verify(data: bytes | None, document=None, **kwargs):
    return verify_retrieval_handoff(
        data,
        manifest(data) if document is None and data is not None else document,
        expected_producer="retriever-v1",
        now=NOW,
        **kwargs,
    )


def test_valid_handoff_is_deterministic_and_parsed_after_verification():
    data = artifact_bytes()
    first = manifest(data)
    second = manifest(data)
    assert first == second
    assert verify(data, first) == [
        {"content": "inert text", "path": "README.md", "repository": "example/project"}
    ]


def test_missing_artifact_fails_closed_before_payload_parsing(monkeypatch):
    document = manifest(artifact_bytes())
    monkeypatch.setattr(handoff, "_strict_json_loads", lambda _: pytest.fail("payload parser was called"))
    with pytest.raises(HandoffError, match="artifact is missing"):
        verify(None, document)


def test_changed_artifact_with_same_length_fails_digest_verification():
    original = artifact_bytes()
    changed = original.replace(b"inert", b"other")
    assert len(changed) == len(original)
    with pytest.raises(HandoffError, match="artifact_sha256 mismatch"):
        verify(changed, manifest(original))


def test_truncated_artifact_fails_size_verification():
    original = artifact_bytes()
    with pytest.raises(HandoffError, match="artifact_size mismatch"):
        verify(original[:-1], manifest(original))


def test_oversized_artifact_is_rejected_before_payload_parsing(monkeypatch):
    data = b"[" + (b" " * 128) + b"]"
    document = manifest(data)
    monkeypatch.setattr(handoff, "_strict_json_loads", lambda _: pytest.fail("payload parser was called"))
    with pytest.raises(HandoffError, match="exceeds maximum size"):
        verify(data, document, max_bytes=64)


def test_wrong_producer_is_rejected_before_payload_parsing(monkeypatch):
    data = artifact_bytes()
    document = manifest(data)
    monkeypatch.setattr(handoff, "_strict_json_loads", lambda _: pytest.fail("payload parser was called"))
    with pytest.raises(HandoffError, match="wrong artifact producer"):
        verify_retrieval_handoff(
            data,
            document,
            expected_producer="different-retriever",
            now=NOW,
        )


def test_replayed_handoff_is_rejected_before_payload_parsing(monkeypatch):
    data = artifact_bytes()
    document = manifest(data)
    monkeypatch.setattr(handoff, "_strict_json_loads", lambda _: pytest.fail("payload parser was called"))
    with pytest.raises(HandoffError, match="replayed handoff"):
        verify(data, document, seen_handoff_ids={document["handoff_id"]})


def test_stale_and_not_yet_valid_artifacts_fail_closed():
    data = artifact_bytes()
    stale = build_handoff_manifest(
        producer="retriever-v1",
        artifact_name="retrieval/input.json",
        artifact_bytes=data,
        produced_at="2026-07-21T21:00:00Z",
        expires_at="2026-07-21T21:30:00Z",
    )
    with pytest.raises(HandoffError, match="artifact is stale"):
        verify(data, stale)

    future = build_handoff_manifest(
        producer="retriever-v1",
        artifact_name="retrieval/input.json",
        artifact_bytes=data,
        produced_at="2026-07-21T22:30:00Z",
        expires_at="2026-07-21T23:00:00Z",
    )
    with pytest.raises(HandoffError, match="not yet valid"):
        verify(data, future)


def test_manifest_identity_binds_every_policy_field():
    data = artifact_bytes()
    document = manifest(data)
    mutated = deepcopy(document)
    mutated["expires_at"] = "2026-07-21T22:06:00Z"
    with pytest.raises(HandoffError, match="handoff_id mismatch"):
        verify(data, mutated)


def test_duplicate_keys_and_non_standard_numbers_are_rejected():
    duplicate = b'[{"path":"a","path":"b"}]'
    with pytest.raises(HandoffError, match="duplicate JSON key"):
        verify(duplicate, manifest(duplicate))

    nonfinite = b'[{"score":NaN}]'
    with pytest.raises(HandoffError, match="non-standard JSON number"):
        verify(nonfinite, manifest(nonfinite))


def test_non_array_payload_and_invalid_limits_are_rejected():
    object_payload = b'{"path":"README.md"}'
    with pytest.raises(HandoffError, match="JSON array"):
        verify(object_payload, manifest(object_payload))

    data = artifact_bytes()
    with pytest.raises(HandoffError, match="positive integer"):
        verify(data, manifest(data), max_bytes=True)


def test_manifest_builder_rejects_unsafe_names_and_time_windows():
    data = artifact_bytes()
    with pytest.raises(HandoffError, match="normalized and relative"):
        build_handoff_manifest(
            producer="retriever-v1",
            artifact_name="../input.json",
            artifact_bytes=data,
            produced_at=PRODUCED,
            expires_at=EXPIRES,
        )
    with pytest.raises(HandoffError, match="later than"):
        build_handoff_manifest(
            producer="retriever-v1",
            artifact_name="input.json",
            artifact_bytes=data,
            produced_at=EXPIRES,
            expires_at=PRODUCED,
        )
