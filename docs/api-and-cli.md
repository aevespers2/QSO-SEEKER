# API and CLI

## Installation

QSO-SEEKER requires Python 3.11 or later.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

The package name is `unicernal-search-gateway`; the console command is `unicernal-search`.

## Input format

The `sanitize` command accepts a JSON array of strict objects:

```json
[
  {
    "repository": "owner/project",
    "path": "README.md",
    "url": "https://example.invalid/owner/project/README.md",
    "content": "Untrusted text supplied by a separate reader",
    "source_kind": "file"
  }
]
```

Required fields are `repository`, `path`, `url`, and `content`. `source_kind` defaults to `file` and the raw schema currently permits `description`, `topic`, `readme`, `file`, `issue`, `pull_request`, `comment`, `commit`, `release`, and `workflow_log`. The narrower canonical-record v1 contract supports only its documented six source kinds; producers must map or reject unsupported raw kinds before canonical handoff.

## Sanitize command

```bash
unicernal-search sanitize INPUT.json \
  --output ACCEPTED.json \
  --audit AUDIT.json \
  [--report REPORT.json] \
  [--pdf REPORT.pdf]
```

| Argument | Required | Description |
|---|---:|---|
| `INPUT.json` | yes | Local JSON array of untrusted records |
| `--output` | yes | Accepted sanitized records |
| `--audit` | yes | Per-input accepted or rejected decisions |
| `--report` | no | JSON evidence summary |
| `--pdf` | no | PDF rendering of the generated evidence summary |

The command returns zero after processing a structurally valid input array, even when individual records are rejected and recorded in the audit. Invalid top-level input raises an error.

## PDF command

An existing JSON evidence report can be rendered separately:

```bash
unicernal-search pdf REPORT.json --output REPORT.pdf
```

PDF generation is a presentation step. The JSON report and its recorded hashes remain the primary machine-readable evidence.

## Output semantics

### Accepted record

A basic sanitizer record contains:

- `repository`
- `path`
- `source_kind`
- `source_url`
- `content`
- `content_sha256`
- `flags`
- `transformations`

This shape is not identical to canonical-record v1 because it does not include the contract identifier, schema version, canonical `record_id`, or complete provenance object.

### Audit entry

Every input receives an audit entry. Accepted entries record status, flags, transformations, and content hash. Rejected entries record the input index and a stable rejection reason such as schema failure or unsupported binary, archive, or executable material.

### Evidence report

The CLI report records a generated event identifier, generation time, source file, summary hash, accepted/audit/flagged/rejected counts, and flagged-record findings. Because generation time is included, complete report files are not intended to be byte-identical across separate invocations; the accepted records and contract artifacts carry the deterministic content identities.

## Python surfaces

### `unicernal_search.gateway.sanitize_records`

```python
from unicernal_search.gateway import sanitize_records

accepted, audit = sanitize_records(payload)
```

`payload` must be a list of dictionaries. The function processes each record independently and returns `(accepted, audit)`.

### `unicernal_search.contracts.build_canonical_record`

Builds a canonical-record v1 object from explicit repository, path, URL, source kind, content, transformations, flags, collector, timestamp, and original source bytes. The builder sorts canonical collections and computes source, content, and record identities.

### `unicernal_search.contracts.validate_canonical_record`

```python
from unicernal_search.contracts import validate_canonical_record

validated = validate_canonical_record(candidate)
```

Returns a defensive copy on success and raises `ContractError` on malformed fields, unsupported versions, invalid paths or URLs, noncanonical collections, or hash mismatch.

### `unicernal_search.contracts.validate_attribution_sidecar`

Validates the exact attribution-sidecar v1 field set and recomputes its hash. Consumers must also confirm that the sidecar's `record_id` is the record they intend to use.

### `canonical_json_bytes` and `sha256_hex`

These helpers expose the version-1 canonical JSON and hashing primitives. They are suitable for fixtures and independent validators but do not replace record-level validation.

## Error handling

- Raw schema problems become audit rejections during `sanitize_records`.
- Top-level CLI input shape problems raise `ValueError`.
- Canonical contract problems raise `ContractError`.
- File-system or PDF errors propagate to the caller and should be treated as failed evidence generation.

## Consumer example

```python
import json
from pathlib import Path

from unicernal_search.contracts import validate_canonical_record

candidate = json.loads(Path("canonical-record.json").read_text(encoding="utf-8"))
record = validate_canonical_record(candidate)

# Continue only with consumer-specific policy checks.
print(record["record_id"])
```

Never execute, import, compile, shell, or evaluate the `content` field.
