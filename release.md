# Release Plan

## Current decision

Status: `BLOCKED — CURRENT-MAIN REPLAY, P2 ISOLATION, P3 CONFORMANCE, RETAINED EVIDENCE, AND HUMAN APPROVAL REQUIRED`

QSO-SEEKER has an implemented local sanitizer, an accepted canonical-record/attribution-sidecar contract v1, and an accepted repository-wide consent-capacity control. PR #10 merged contract version 1, and PR #11 merged the exact-head consent-lock repair. Earlier P0 evidence from PR #2 still is not final release evidence for the current composition of `main`.

No tag, package publication, scheduled collection, live/private retrieval, QSO runtime handoff, or shared-field publication is currently authorized.

## Versioning

- Semantic Versioning applies to the CLI, raw schema, canonical-record schema, attribution sidecar, sanitizer handoff, evidence format, and future adapter contracts.
- The first eligible hostile-input candidate remains `0.1.0-alpha.1` until a final accepted head passes every gate.
- Contract v1 is identified by `qso-seeker.canonical-record` and `qso-seeker.attribution-sidecar`, each with integer schema version `1`.
- Changes to required fields, accepted source kinds, transformations, canonical JSON, hash inputs, path/URL rules, isolation, retention, or publisher envelopes require explicit compatibility review and migration fixtures.
- Broader collection, private overlays, experimental spawning, QSIO integration, or shared-field work must use separately approved versions and may not enter the first release implicitly.

## Release scope

The first eligible candidate is limited to:

- reproducible local CLI sanitization and audit generation;
- strict raw-input validation and stable rejection reasons;
- canonical-record and attribution-sidecar contract v1;
- deterministic positive, negative, mutation, boundary, and adversarial fixtures;
- independently permissioned read-only retrieval and credential-free/network-free sanitizer jobs;
- digest-verified artifact-only handoff;
- JSON and optional PDF evidence outputs;
- exact-source, minimum-permission, dependency, package-boundary, hidden-control, and consent-capacity checks;
- accurate Pages documentation, checksums, provenance, recovery, rollback, and approval evidence.

### Explicit exclusions

- General crawling or browser automation.
- Authenticated or private-source acquisition.
- Source-driven execution, import, compilation, shell use, or package installation.
- Scheduled or live collection service.
- Automatic repository writes or package publication.
- Autonomous truth promotion, learning, genome generation, or spawning.
- QSIO runtime authority or shared-field publication.
- Any capability present only in an unmerged draft pull request.

## Accepted work

Canonical-record and attribution-sidecar contract v1 are accepted implementation on `main`. They define exact fields, strict canonical JSON, SHA-256 content/source/record/sidecar identities, normalized relative paths, HTTPS URLs, canonical collections, fail-closed validation, and an inert-data authority boundary.

The repository-wide consent-capacity control is also accepted on `main`: strict JSON validation, repository-wide scope semantics, focused regressions, pinned Actions, exact submitted-head checkout and assertion, least-privilege workflow permissions, disabled credential persistence, and retained checksum evidence were merged through PR #11.

The Pages documentation candidate records the implemented components, distinguishes basic sanitizer output from canonical handoff artifacts, and documents the target retrieval-to-sanitizer separation without claiming that P2 is already complete.

## Acceptance gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical P0 composition | REVIEW | Replay current `main` composition on one immutable final head; retain complete evidence and obtain Architect disposition. |
| Task completion | FAIL | P0 accepted; P1 remains accepted; P2-P3 complete; D0 documentation accepted. |
| Contract determinism | PASS FOR V1 | PR #10 merged deterministic canonical-record and sidecar v1 validation and mutation tests; final release replay is still required. |
| Security isolation | FAIL | Retrieval and sanitizer must be independently permissioned; sanitizer must lack source credentials/network/repository-write authority and verify the handoff digest. |
| Adversarial validation | PARTIAL | Existing tests cover core sanitizer and contract behavior; complete versioned handoff and consumer conformance fixtures remain pending. |
| Workflow integrity | REVIEW | Exact-head and least-permission evidence exists for accepted contract and consent-control candidates; one final current-composition replay with retained artifacts is required. |
| Consent-capacity control | PASS FOR CURRENT MAIN | PR #11 merged the repaired repository-wide validator, regression tests, exact-head workflow, pinned Actions, and retained evidence; final release replay remains required. |
| Scope integrity | PASS | Broader collection, live checkpoint, experimental spawning, QSIO integration, and shared-field work remain separate candidates. |
| Documentation | REVIEW | Pages foundation covers overview, architecture, contracts, API/CLI, security, onboarding, operations, governance, and diagrams; strict build evidence is required on the reconciled final documentation head. |
| Legal/privacy/license | BLOCKED | Source terms, attribution, privacy, retention, and any later collection/publication model require explicit approval. |
| Provenance | PARTIAL | Contract hashes and exact commit identities exist; retained release bundle, complete checksums, attestations, and rejected-candidate records remain incomplete. |
| Operations and rollback | PARTIAL | Procedures are documented; a final-head rollback exercise and retained result are required. |
| Deployment readiness | BLOCKED | No live, private, scheduled, runtime, or publication target is approved. |
| Approval | PENDING | Architect and release owner must approve the final immutable candidate after all blocking gates pass. |

## Required artifacts

- Source and package artifacts from the final accepted head.
- Canonical-record and attribution-sidecar specifications and machine-readable schemas.
- Positive, negative, boundary, mutation, Unicode, dependency, digest-mismatch, and independent-consumer fixtures with expected identities.
- Accepted, audit, JSON report, and representative PDF outputs.
- Exact-head workflow logs, test reports, security verifier output, hidden-control results, permissions inventory, consent-lock evidence, and documentation build output.
- Artifact checksums, dependency inventory or SBOM where applicable, provenance manifest or attestation, and reviewer decisions.
- Recovery and rollback exercise evidence.
- Legal, privacy, attribution, source-term, and retention approval records.

## Deployment and operations posture

The first verification target must be disposable and bounded. Source reading must be read-only. Sanitization must be credential-free, network-free, and repository-write-free, and must accept only a digest-verified artifact. Health requires exact source identity, deterministic record identities, complete audit decisions, no source-content execution, minimum permissions, visible failures, and no secrets or prohibited source data in evidence.

Roll back on source drift, nondeterministic identities, execution paths, missing digest verification, permission leakage, dependency drift, contract mismatch, privacy or source-term violations, or documentation that overstates the boundary. Preserve evidence, quarantine affected artifacts, restore the prior accepted revision, revoke temporary permissions, rerun the full suite, and record human disposition.

## Unresolved blockers

- Final current-main P0 replay and Architect acceptance with retained artifacts.
- P2 independent retrieval/sanitizer permission split and digest-verified handoff.
- P3 complete adversarial and consumer conformance fixtures.
- Strict Pages build and review of the reconciled documentation foundation.
- Complete provenance, checksums, rollback exercise, privacy, source-term, attribution, retention, and release approval evidence.
- Downstream consumers must not treat QSO-SEEKER artifacts as authoritative until the release contract is published by version and hash.

## Release log

- 2026-07-16 — Defined the first release as a secure, read-only hostile-input boundary.
- 2026-07-17 — Historical PR #2 exact-head checks passed for its candidate, but final retained evidence and Architect acceptance remained incomplete.
- 2026-07-17 — Broader collection and private-overlay work was excluded from the first release.
- 2026-07-18 — PR #10 merged canonical-record and attribution-sidecar contract v1 after exact-head verification.
- 2026-07-18 — Consent-capacity policy and CI enforcement were added.
- 2026-07-19 — Proposed a complete Pages, architecture, contract, API/CLI, security, onboarding, operations, governance, and diagram documentation foundation without changing runtime scope.
- 2026-07-20 — PR #11 merged the exact-head repository-wide consent-lock repair; the documentation candidate was reconciled to the accepted workflow, validator, tests, and release status.
