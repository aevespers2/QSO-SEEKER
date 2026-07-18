from copy import deepcopy

import pytest

from unicernal_search.contracts import (
    ContractError,
    build_canonical_record,
    canonical_json_bytes,
    sha256_hex,
    validate_attribution_sidecar,
    validate_canonical_record,
)


def record():
    return build_canonical_record(
        repository="example/project",
        path="README.md",
        source_url="https://example.invalid/example/project/README.md",
        source_kind="file",
        content="safe inert text",
        transformations=["unicode_nfkc"],
        flags=["prompt_injection"],
        collector="qso-seeker-local",
        collected_at="2026-07-18T00:00:00Z",
        source_bytes=b"safe inert text",
    )


def test_record_is_deterministic_and_valid():
    first = record()
    second = record()
    assert first == second
    assert validate_canonical_record(first) == first
    assert first["record_id"].startswith("sha256:")


def test_content_hash_mismatch_fails_closed():
    candidate = record()
    candidate["content"] = "mutated"
    with pytest.raises(ContractError, match="content_sha256 mismatch"):
        validate_canonical_record(candidate)


def test_record_id_binds_provenance_and_transformations():
    candidate = record()
    candidate["provenance"]["collector"] = "other"
    with pytest.raises(ContractError, match="record_id mismatch"):
        validate_canonical_record(candidate)


def test_boolean_version_and_unknown_fields_are_rejected():
    candidate = record()
    candidate["schema_version"] = True
    with pytest.raises(ContractError, match="schema_version"):
        validate_canonical_record(candidate)
    candidate = record()
    candidate["extra"] = "no"
    with pytest.raises(ContractError, match="fields"):
        validate_canonical_record(candidate)


def test_paths_urls_and_collections_are_canonical():
    candidate = record()
    candidate["path"] = "../secret"
    with pytest.raises(ContractError, match="path"):
        validate_canonical_record(candidate)
    candidate = record()
    candidate["source_url"] = "http://example.invalid"
    with pytest.raises(ContractError, match="HTTPS"):
        validate_canonical_record(candidate)
    candidate = record()
    candidate["flags"] = ["z", "a", "a"]
    with pytest.raises(ContractError, match="sorted and unique"):
        validate_canonical_record(candidate)


def test_lone_surrogates_and_nonfinite_values_are_rejected():
    with pytest.raises((UnicodeEncodeError, ContractError)):
        canonical_json_bytes({"content": "\ud800"})
    with pytest.raises(ContractError, match="non-finite"):
        canonical_json_bytes({"value": float("inf")})


def test_attribution_sidecar_hash_is_verified():
    payload = {
        "contract": "qso-seeker.attribution-sidecar",
        "schema_version": 1,
        "record_id": record()["record_id"],
        "source": "Example",
        "author": None,
        "license": "MIT",
    }
    sidecar = deepcopy(payload)
    sidecar["sidecar_sha256"] = sha256_hex(canonical_json_bytes(payload))
    assert validate_attribution_sidecar(sidecar) == sidecar
    sidecar["license"] = "Apache-2.0"
    with pytest.raises(ContractError, match="sidecar_sha256 mismatch"):
        validate_attribution_sidecar(sidecar)
