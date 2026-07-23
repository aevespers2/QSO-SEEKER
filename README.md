# QSO-SEEKER

QSO-SEEKER is a deliberately non-executing hostile-input boundary for bounded QSO research. It converts supported untrusted repository records into sanitized inert text, deterministic hashes, per-record audit decisions, optional evidence reports, and independently validated canonical handoff artifacts.

> Sanitization does not make arbitrary content safe to execute, current, authoritative, or true. Every output remains untrusted data until each downstream consumer independently validates the applicable contracts and policy.

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
              | bounded local artifact + declared digest
              v
       strict input schema
              |
       reject or sanitize
              |
       accepted + audit + report
              |
       canonical producer + v1 validation
              |
       candidate source-observation envelope
              |
       temporal / policy / transport validation
              v
        bounded downstream consumer
```

The sanitizer does not require network access, source credentials, repository-write authority, or a content-execution path. Retrieval, subject identity, temporal validity, canonical-state disposition, downstream consumption, and publication remain separate architecture and policy decisions.

A valid canonical-record hash proves conformance to the local record contract. It does not independently prove that the record is current, non-replayed, bound to the correct long-lived subject, legally publishable, accepted into canonical state, or safe for runtime use.

The candidate source-observation envelope profile documents how subject, time, replay, policy, privacy, completion, correction, revocation, and recovery references can accompany a canonical record without changing canonical-record v1. It remains a documentation proposal and activates no route, schema package, credential, or authority.

The source-rights and privacy review guide separates access, purpose, terms, privacy, retention, handoff, and publication decisions. It is documentation only: public visibility is not treated as permission to collect, correlate, retain, or republish, and unresolved evidence keeps the route closed.

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
- [Candidate source-observation envelope profile](docs/source-observation-envelope.md)
- [Source rights and privacy review](docs/source-rights-and-privacy-review.md)
- [Obstruction and gluing analysis](docs/obstruction-and-gluing.md)
- [CLI and Python API](docs/api-and-cli.md)
- [Security model](docs/security.md)
- [Developer onboarding](docs/developer-guide.md)
- [Operations and recovery](docs/operations.md)
- [Repository governance](docs/governance.md)
- [Release and gluing punch list](punchlist.md)

## Portfolio boundary

The documentation proposes the following non-overlapping model, pending formal approval and compatibility fixtures:

- QSO-SEEKER owns source sanitization, canonical-record v1 construction, attribution sidecars, and local rejection evidence.
- The candidate source-observation envelope binds Seeker artifacts to external subject, temporal, replay, policy, privacy, completion, correction, revocation, and recovery references without rewriting local record identity.
- `datarepo-temporal-invariants` owns subject, clock, uncertainty, freshness, replay, and ordering interpretation.
- QSO-DIGITALIS owns domain-specific evidence interpretation and synthesis proposals.
- Bridge owns version-preserving transport and evidence packaging.
- Repository `1` owns quarantine admission, policy disposition, canonical state, correction, revocation, and recovery receipts.
- QSO-STUDIO and AionUi present evidence without creating approval authority.
- QSO-GENOMES, QuantumStateObjects, QSO-FABRIC, and `qsio-kernel` retain their own genome, runtime, orchestration, and semantic responsibilities.

This is a documentation proposal. No adapter, credential, network route, runtime handoff, canonical-state authority, or publication path is activated.

## Project status

The local sanitizer and canonical-record/attribution-sidecar v1 contract are implemented on `main`. Release remains blocked until the accepted task chain's remaining current-composition replay, independent isolation, adversarial and cross-repository conformance, portfolio gluing, retained evidence, documentation validation, provenance, rollback, legal/privacy, and human-approval gates are complete.

Draft collection, scheduling, action-protocol, experimental spawning, QSIO integration, shared-field, and observation-envelope proposals do not expand the accepted baseline merely by existing in open pull requests.

See [`taskchain.md`](taskchain.md), [`punchlist.md`](punchlist.md), [`release.md`](release.md), and [`changelog.md`](changelog.md) for the current decision record.
