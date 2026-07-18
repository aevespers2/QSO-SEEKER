# QSO-SEEKER Canonical Record Contract v1

Status: **ACCEPTED CANDIDATE**
Contract identifier: `qso-seeker.canonical-record`
Schema version: `1`
Hash algorithm: `sha256`
Canonicalization: UTF-8 JSON, sorted object keys, compact separators, `ensure_ascii=false`, no NaN/Infinity, no duplicate keys, and no lone surrogates.

## Record

A canonical record is inert data. It contains no executable authority and must never be interpreted as instructions.

Required fields:

- `contract`: exactly `qso-seeker.canonical-record`
- `schema_version`: integer `1`; Boolean values are invalid
- `record_id`: lowercase `sha256:<64 hex>` derived from the canonical hash payload
- `repository`: non-empty string
- `path`: normalized relative path without `..`, absolute prefixes, or NUL
- `source_url`: HTTPS URL
- `source_kind`: one of `description`, `file`, `release`, `issue`, `pull_request`, `commit`
- `content`: canonicalized UTF-8 text
- `content_sha256`: lowercase SHA-256 of the exact UTF-8 bytes of `content`
- `transformations`: sorted unique array of non-empty strings
- `flags`: sorted unique array of non-empty strings
- `provenance`: object containing immutable source identity

The `provenance` object requires `collector`, `collected_at`, and `source_sha256`. `source_sha256` hashes the exact hostile-input bytes before canonicalization.

## Hash semantics

`record_id` is computed from the canonical JSON bytes of all record fields except `record_id`. The hash payload includes both `content_sha256` and provenance, binding identity to content, source, and transformations.

The canonical JSON function rejects unsupported values before hashing. Hash validation occurs before downstream handoff.

## Attribution sidecar

Attribution is stored separately under contract `qso-seeker.attribution-sidecar`, schema version `1`. It binds to `record_id`, identifies source/license/author fields when known, and has its own `sidecar_sha256`, computed over all sidecar fields except `sidecar_sha256`.

## Compatibility

Version 1 consumers must fail closed on unknown required fields, unsupported versions, malformed hashes, mismatched content bytes, invalid paths/URLs, or noncanonical collections. Compatible optional fields require a future minor contract version and explicit migration fixtures.

## Authority boundary

Acceptance of this contract authorizes deterministic local validation and inert artifact handoff only. It does not authorize network retrieval, credentials, content execution, repository writes, QSO runtime execution, publication, or autonomous learning.
