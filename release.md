# Release Plan

## Current decision

Status: `BLOCKED — CURRENT-MAIN REPLAY, P2 ISOLATION, P3 CONFORMANCE, G0 PORTFOLIO GLUING, RETAINED EVIDENCE, AND HUMAN APPROVAL REQUIRED`

QSO-SEEKER has an implemented local sanitizer, an accepted canonical-record/attribution-sidecar contract v1, and an accepted repository-wide consent-capacity control. PR #10 merged contract version 1, and PR #11 merged the exact-head consent-lock repair. Earlier P0 evidence from PR #2 still is not final release evidence for the current composition of `main`.

The documentation candidate now also identifies the cross-repository contracts required before QSO-SEEKER artifacts can be treated as portfolio-ready evidence: stable subject identity, source lineage, clock/freshness/replay interpretation, transport preservation, policy disposition, correction, revocation, reason codes, privacy, retention, emergency stop, and recovery.

No tag, package publication, scheduled collection, live/private retrieval, QSO runtime handoff, canonical-state disposition, or shared-field publication is currently authorized.

## Versioning

- Semantic Versioning applies to the CLI, raw schema, canonical-record schema, attribution sidecar, sanitizer handoff, evidence format, reason-code namespace, correction/revocation events, and future adapter contracts.
- The first eligible hostile-input candidate remains `0.1.0-alpha.1` until a final accepted head passes every gate.
- Contract v1 is identified by `qso-seeker.canonical-record` and `qso-seeker.attribution-sidecar`, each with integer schema version `1`.
- Changes to required fields, accepted source kinds, transformations, canonical JSON, hash inputs, path/URL rules, isolation, retention, correction, revocation, or publisher envelopes require explicit compatibility review and migration fixtures.
- Subject identity, time/freshness/replay, policy disposition, and canonical-state decisions must remain separate versioned contracts rather than being silently added to canonical-record v1.
- Broader collection, private overlays, experimental spawning, action orchestration, QSIO integration, or shared-field work must use separately approved versions and may not enter the first release implicitly.

## Release scope

The first eligible candidate is limited to:

- reproducible local CLI sanitization and audit generation;
- strict raw-input validation and stable rejection reasons;
- canonical-record and attribution-sidecar contract v1;
- deterministic positive, negative, mutation, boundary, adversarial, and cross-language fixtures;
- independently permissioned read-only retrieval and credential-free/network-free sanitizer jobs;
- digest-verified artifact-only handoff;
- independent consumer validation of exact canonical bytes and identities;
- JSON and optional PDF evidence outputs;
- exact-source, minimum-permission, dependency, package-boundary, hidden-control, and consent-capacity checks;
- accurate Pages documentation, obstruction/gluing analysis, checksums, provenance, recovery, rollback, and approval evidence.

### Explicit exclusions

- General crawling or browser automation.
- Authenticated or private-source acquisition.
- Source-driven execution, import, compilation, shell use, or package installation.
- Scheduled or live collection service.
- Automatic repository writes or package publication.
- Autonomous truth promotion, learning, genome generation, or spawning.
- QSIO runtime authority, canonical-state authority, or shared-field publication.
- Automatic mutation of QSO-GENOMES, QuantumStateObjects, or QSO-FABRIC state.
- Any capability present only in an unmerged draft pull request.

## Accepted work

Canonical-record and attribution-sidecar contract v1 are accepted implementation on `main`. They define exact fields, strict canonical JSON, SHA-256 content/source/record/sidecar identities, normalized relative paths, HTTPS URLs, canonical collections, fail-closed validation, and an inert-data authority boundary.

The repository-wide consent-capacity control is also accepted on `main`: strict JSON validation, repository-wide scope semantics, focused regressions, pinned Actions, exact submitted-head checkout and assertion, least-privilege workflow permissions, disabled credential persistence, and retained checksum evidence were merged through PR #11.

The Pages documentation candidate records the implemented components, distinguishes basic sanitizer output from canonical handoff artifacts, documents the target retrieval-to-sanitizer separation without claiming that P2 is already complete, and maps portfolio obstructions without activating any external route or authority.

## Candidate portfolio ownership model

The documentation proposes the following lowest-overlap split:

- QSO-SEEKER owns source-facing sanitization, canonical-record v1 construction, attribution sidecars, and local rejection evidence.
- `datarepo-temporal-invariants` owns subject, clock, uncertainty, freshness, replay, and ordering interpretation.
- QSO-DIGITALIS owns domain-specific evidence interpretation and synthesis proposals.
- Bridge owns version-preserving transport and evidence packaging.
- Repository `1` owns quarantine admission, policy disposition, canonical state, correction, revocation, and recovery receipts.
- QSO-STUDIO and AionUi own human review and presentation without implicit approval authority.
- QSO-GENOMES owns immutable identity, lineage, traits, and policy-genome contracts.
- QuantumStateObjects and QSO-FABRIC own runtime and multi-QSO orchestration after independent validation.

This model remains a proposal until contract owners, versions, fixtures, and approvals are recorded.

## Acceptance gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical P0 composition | REVIEW | Replay current `main` composition on one immutable final head; retain complete evidence and obtain Architect disposition. |
| Task completion | FAIL | P0 accepted; P1 remains accepted; P2-P3 and G0 complete; D0 documentation accepted. |
| Contract determinism | PASS FOR V1 | PR #10 merged deterministic canonical-record and sidecar v1 validation and mutation tests; language-neutral fixtures, an independent consumer witness, and final release replay remain required. |
| Security isolation | FAIL | Retrieval and sanitizer must be independently permissioned; sanitizer must lack source credentials/network/repository-write authority and verify the handoff digest. |
| Adversarial validation | PARTIAL | Existing tests cover core sanitizer and contract behavior; complete versioned handoff, cross-language, cross-repository, correction, revocation, and consumer conformance fixtures remain pending. |
| Portfolio gluing | BLOCKED | Subject, temporal, evidence-envelope, policy, transport, canonical-state, reason-code, correction/revocation, privacy/retention, emergency-stop, and recovery ownership must be versioned and witnessed. |
| Workflow integrity | REVIEW | Exact-head and least-permission evidence exists for accepted contract and consent-control candidates; one final current-composition replay with retained artifacts is required. |
| Consent-capacity control | PASS FOR CURRENT MAIN | PR #11 merged the repaired repository-wide validator, regression tests, exact-head workflow, pinned Actions, and retained evidence; final release replay remains required. |
| Scope integrity | PASS | Broader collection, live checkpoint, experimental spawning, action protocol, QSIO integration, and shared-field work remain separate candidates. |
| Documentation | REVIEW | Pages foundation covers overview, architecture, contracts, obstruction/gluing, API/CLI, security, onboarding, operations, governance, punch list, and diagrams; strict build evidence is required on the final head. |
| Legal/privacy/license | BLOCKED | Source terms, attribution, privacy, retention, redaction, and any later collection/publication model require explicit approval. |
| Provenance | PARTIAL | Contract hashes and exact commit identities exist; retained release bundle, complete checksums, attestations, correction history, and rejected-candidate records remain incomplete. |
| Operations and rollback | PARTIAL | Procedures are documented; end-to-end freeze, evidence preservation, revocation propagation, cache invalidation, rollback, and bounded recovery require a retained exercise. |
| Deployment readiness | BLOCKED | No live, private, scheduled, runtime, canonical-state, or publication target is approved. |
| Approval | PENDING | Architect and release owner must approve the final immutable candidate after all blocking gates pass. |

## Required artifacts

- Source and package artifacts from the final accepted head.
- Canonical-record and attribution-sidecar specifications and machine-readable schemas.
- Language-neutral canonical byte fixtures and at least one independent consumer witness.
- Positive, negative, boundary, mutation, Unicode, dependency, digest-mismatch, stale, replay, wrong-subject, correction, revocation, and independent-consumer fixtures with expected identities.
- Pairwise and triple-overlap witness evidence across retrieval, sanitizer, canonical producer, temporal validation, Bridge, Repository `1`, QSO-STUDIO/AionUi, QSO-GENOMES, and QuantumStateObjects.
- Accepted, audit, JSON report, representative PDF, correction, revocation, freeze, and recovery outputs.
- Exact-head workflow logs, test reports, security verifier output, hidden-control results, permissions inventory, consent-lock evidence, and documentation build output.
- Artifact checksums, dependency inventory or SBOM where applicable, provenance manifest or attestation, and reviewer decisions.
- Recovery and rollback exercise evidence.
- Legal, privacy, attribution, source-term, redaction, and retention approval records.

## Deployment and operations posture

The first verification target must be disposable and bounded. Source reading must be read-only. Sanitization must be credential-free, network-free, and repository-write-free, and must accept only a digest-verified artifact. Health requires exact source identity, deterministic record identities, complete audit decisions, no source-content execution, minimum permissions, visible failures, and no secrets or prohibited source data in evidence.

Downstream health also requires explicit treatment of `observed`, `sanitized`, `unverified`, `rejected`, `unknown`, `corrected`, and `revoked` states. A valid record hash, successful transport, visible interface, or runtime ingestion is not canonical acceptance or verified truth.

Roll back on source drift, nondeterministic identities, execution paths, missing digest verification, permission leakage, dependency drift, contract mismatch, wrong-subject binding, stale or replayed evidence, failed correction/revocation propagation, privacy or source-term violations, or documentation that overstates the boundary. Preserve evidence, quarantine affected artifacts, restore the prior accepted revision, revoke temporary permissions, invalidate downstream caches where authorized, rerun the full suite, and record human disposition.

## Unresolved blockers

- Final current-main P0 replay and Architect acceptance with retained artifacts.
- P2 independent retrieval/sanitizer permission split and digest-verified handoff.
- P3 complete adversarial, cross-language, and consumer conformance fixtures.
- G0 accepted ownership for subject identity, source lineage, time/freshness/replay, evidence envelopes, reason codes, correction/revocation, privacy/retention, emergency stop, and recovery.
- Strict Pages build and review of the reconciled documentation foundation.
- Complete provenance, checksums, rollback exercise, privacy, source-term, attribution, redaction, retention, and release approval evidence.
- Disposition of open action-protocol, collection-core, live-checkpoint, spawning, and QSIO candidates.
- Downstream consumers must not treat QSO-SEEKER artifacts as authoritative until the release contract is published by version and hash.

## Release log

- 2026-07-16 — Defined the first release as a secure, read-only hostile-input boundary.
- 2026-07-17 — Historical PR #2 exact-head checks passed for its candidate, but final retained evidence and Architect acceptance remained incomplete.
- 2026-07-17 — Broader collection and private-overlay work was excluded from the first release.
- 2026-07-18 — PR #10 merged canonical-record and attribution-sidecar contract v1 after exact-head verification.
- 2026-07-18 — Consent-capacity policy and CI enforcement were added.
- 2026-07-19 — Proposed a complete Pages, architecture, contract, API/CLI, security, onboarding, operations, governance, and diagram documentation foundation without changing runtime scope.
- 2026-07-20 — PR #11 merged the exact-head repository-wide consent-lock repair; the documentation candidate was reconciled to the accepted workflow, validator, tests, and release status.
- 2026-07-20 — Added the obstruction/gluing ledger, triple-overlap witnesses, expanded punch list, and portfolio ownership gates without changing runtime or authority scope.
