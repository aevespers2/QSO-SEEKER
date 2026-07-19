# QSO-SEEKER

QSO-SEEKER is a deliberately non-executing hostile-input boundary for bounded QSO research. It converts supported untrusted repository records into sanitized inert text, deterministic hashes, per-record audit decisions, optional evidence reports, and independently validated canonical handoff artifacts.

> Sanitization does not make arbitrary content safe to execute or true. Every output remains untrusted data.

## Capabilities

- Strict JSON record validation with unknown fields rejected.
- Relative-path, source-kind, URL, and content-size constraints.
- Rejection of executable, archive, NUL-containing, and binary-looking material.
- Unicode normalization, hidden-control removal, active-content neutralization, and bounded truncation.
- Classification of prompt-injection, execution-request, and credential-access indicators.
- Accepted-record and audit JSON outputs, plus optional JSON and PDF evidence reports.
- Canonical-record and attribution-sidecar contract version 1 with deterministic SHA-256 validation.
- Security and consent-capacity checks designed to fail closed.

## Architecture

```text
separately governed source reader
              |
              | bounded local JSON artifact
              v
       strict input schema
              |
       reject or sanitize
              |
       accepted + audit + report
              |
       canonical contract validation
              v
        bounded downstream consumer
```

The sanitizer does not require network access, source credentials, repository-write authority, or a content-execution path. Retrieval, downstream consumption, and publication remain separate architecture and policy decisions.

## Install

Requires Python 3.11 or later.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Run

```bash
unicernal-search sanitize input.json \
  --output build/accepted.json \
  --audit build/audit.json \
  --report build/report.json \
  --pdf build/report.pdf
```

Example input:

```json
[
  {
    "repository": "owner/project",
    "path": "README.md",
    "url": "https://example.invalid/owner/project/README.md",
    "content": "Untrusted text supplied by a separate read-only adapter",
    "source_kind": "file"
  }
]
```

The immediate accepted-record shape is not automatically a complete canonical-record v1 artifact. Cross-component producers must add and validate the versioned contract fields and provenance described in the design documentation.

## Test

```bash
python -m pytest
python tools/verify_security_envelope.py
```

## Documentation

The GitHub Pages source is under [`docs/`](docs/index.md) and is configured by [`mkdocs.yml`](mkdocs.yml).

- [Project overview](docs/project-overview.md)
- [Architecture and trust boundaries](docs/architecture.md)
- [Canonical record and attribution contracts](docs/design-contracts.md)
- [CLI and Python API](docs/api-and-cli.md)
- [Security model](docs/security.md)
- [Developer onboarding](docs/developer-guide.md)
- [Operations and recovery](docs/operations.md)
- [Repository governance](docs/governance.md)

## Project status

The local sanitizer and canonical-record/attribution-sidecar v1 contract are implemented on `main`. Release remains blocked until the accepted task chain's remaining isolation, adversarial conformance, retained evidence, documentation validation, provenance, rollback, legal/privacy, and human-approval gates are complete. Draft collection, scheduling, experimental spawning, QSIO integration, and shared-field proposals do not expand the accepted baseline merely by existing in open pull requests.

See [`taskchain.md`](taskchain.md), [`release.md`](release.md), and [`changelog.md`](changelog.md) for the current decision record.
