# Design contracts

## Contract status

QSO-SEEKER defines two version-1 handoff contracts:

- `qso-seeker.canonical-record`
- `qso-seeker.attribution-sidecar`

They authorize deterministic local construction, validation, and inert artifact handoff. They do not authorize source retrieval, content execution, repository writes, runtime execution, publication, or autonomous conclusions.

## Canonical JSON

Contract hashing uses UTF-8 JSON with:

- object keys sorted lexicographically;
- compact separators;
- Unicode preserved rather than ASCII-escaped;
- finite numeric values only;
- string keys only;
- strict UTF-8 encoding;
- no unsupported Python value types.

A consumer must reproduce these semantics exactly. Similar-looking pretty-printed JSON is not necessarily the canonical hash payload.

## Canonical record v1

A version-1 record contains exactly these fields:

| Field | Meaning |
|---|---|
| `contract` | Exactly `qso-seeker.canonical-record` |
| `schema_version` | Integer `1`; Boolean values are invalid |
| `record_id` | `sha256:` followed by the SHA-256 of the canonical record payload without `record_id` |
| `repository` | Non-empty declared repository identity |
| `path` | Normalized relative path without traversal, empty segments, NUL, or absolute prefix |
| `source_url` | HTTPS source URL |
| `source_kind` | One of `description`, `file`, `release`, `issue`, `pull_request`, or `commit` |
| `content` | Canonicalized inert UTF-8 text |
| `content_sha256` | SHA-256 of the exact UTF-8 bytes of `content` |
| `transformations` | Sorted unique non-empty strings |
| `flags` | Sorted unique non-empty strings |
| `provenance` | Exact object containing `collector`, `collected_at`, and `source_sha256` |

`source_sha256` identifies the exact source bytes before canonicalization. `content_sha256` identifies the resulting text. `record_id` binds content, source identity, transformations, flags, and all remaining fields into one artifact identity.

## Attribution sidecar v1

The attribution sidecar remains separate so attribution and licensing metadata can be maintained without changing content text. It contains:

- contract identifier `qso-seeker.attribution-sidecar`;
- schema version `1`;
- the bound canonical `record_id`;
- source, author, and license values where known; and
- `sidecar_sha256`, computed from every sidecar field except itself.

A change to a bound record requires a new sidecar hash. A change to attribution does not silently rewrite the canonical record.

## Validation sequence

A consumer should validate in this order:

1. Parse JSON without accepting duplicate keys.
2. Confirm the object has exactly the supported fields.
3. Confirm contract identifier and integer schema version.
4. Validate strings, URL, relative path, source kind, and canonical collections.
5. Recompute `content_sha256` from exact UTF-8 content bytes.
6. Validate provenance and source hash shape.
7. Recompute `record_id` from the canonical payload without `record_id`.
8. Validate the attribution sidecar and recompute `sidecar_sha256`.
9. Apply consumer-specific policy before storage or use.

## Compatibility policy

Version-1 consumers fail closed on:

- missing or unknown fields;
- unsupported contract names or versions;
- Boolean schema versions;
- malformed, uppercase, or mismatched hashes;
- non-HTTPS source URLs;
- absolute, empty-segment, dot-segment, or traversal paths;
- unsorted or duplicate `flags` or `transformations`;
- non-finite numbers, lone surrogates, or unsupported values;
- content, record, or sidecar mutation.

A field addition is not automatically backward compatible because version 1 requires an exact field set. Compatible evolution therefore requires a documented new version, independent fixtures, and migration guidance.

## Sanitizer record versus canonical handoff record

The sanitizer's basic accepted record and the canonical contract are related but distinct. The basic record is the immediate result of local hostile-input processing. The canonical contract adds strict provenance and artifact identity requirements for cross-component handoff. Documentation and consumers must not imply that every basic sanitizer output is already a complete canonical-record v1 artifact.

## Design change checklist

Before changing a contract, record:

- the user and system need;
- exact field and hash changes;
- compatibility classification;
- positive, negative, boundary, mutation, and deterministic fixtures;
- migration and rollback behavior;
- producer and consumer version negotiation;
- privacy, licensing, retention, and provenance effects;
- updated `taskchain.md`, `release.md`, and `changelog.md` entries.
