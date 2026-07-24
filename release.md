# Release Plan

## Current decision

Status: `BLOCKED — CURRENT-MAIN REPLAY, P2 ISOLATION, P3 CONFORMANCE, G0-G2 PORTFOLIO AND SOURCE-REVIEW GOVERNANCE, RETAINED EVIDENCE, AND HUMAN APPROVAL REQUIRED`

QSO-SEEKER has an implemented local sanitizer, an accepted canonical-record/attribution-sidecar contract v1, and an accepted repository-wide consent-capacity control. PR #10 merged contract version 1, and PR #11 merged the exact-head consent-lock repair. Earlier P0 evidence from PR #2 still is not final release evidence for the current composition of `main`.

The documentation candidate identifies the cross-repository contracts required before QSO-SEEKER artifacts can be treated as portfolio-ready evidence: stable subject identity, source lineage, clock/freshness/replay interpretation, transport preservation, policy disposition, correction, revocation, reason codes, privacy, retention, emergency stop, and recovery.

Candidate source-observation-envelope and source-rights/privacy profiles now decompose the surrounding decisions into explicit artifact bindings, subject and temporal references, collection-completion states, policy/privacy references, lifecycle receipts, access and purpose review, source terms, minimization, retention, consumer limits, publication separation, fail-closed duties, pairwise fixtures, and triple-overlap witnesses. They are documentation only, have no accepted normative contract IDs or owners, and do not change canonical-record v1.

No tag, package publication, scheduled collection, live/private retrieval, QSO runtime handoff, canonical-state disposition, observation-envelope activation, source-policy automation, or shared-field publication is currently authorized.

## Versioning

- Semantic Versioning applies to the CLI, raw schema, canonical-record schema, attribution sidecar, sanitizer handoff, evidence format, reason-code namespace, correction/revocation events, and future adapter contracts.
- The first eligible hostile-input candidate remains `0.1.0-alpha.1` until a final accepted head passes every gate.
- Contract v1 is identified by `qso-seeker.canonical-record` and `qso-seeker.attribution-sidecar`, each with integer schema version `1`.
- Changes to required fields, accepted source kinds, transformations, canonical JSON, hash inputs, path/URL rules, isolation, retention, correction, revocation, or publisher envelopes require explicit compatibility review and migration fixtures.
- Subject identity, time/freshness/replay, policy disposition, source-rights/privacy decisions, and canonical-state decisions must remain separate versioned contracts rather than being silently added to canonical-record v1.
- The candidate source-observation envelope must receive its own accepted owner, identifier, version, canonical serialization, signing or attestation rules, compatibility policy, fixtures, and rollback plan before implementation.
- Any future machine-readable source-review record requires a separate owner, identifier, canonical representation, status vocabulary, validity and supersession rules, privacy controls, fixtures, migration, and rollback approval.
- Broader collection, private overlays, experimental spawning, action orchestration, QSIO integration, observation-envelope activation, source-policy automation, or shared-field work must use separately approved versions and may not enter the first release implicitly.

## Release scope

The first eligible candidate is limited to:

- reproducible local CLI sanitization and audit generation;
- strict raw-input validation and stable rejection reasons;
- canonical-record and attribution-sidecar contract v1;
- deterministic positive, negative, mutation, boundary, adversarial, and cross-language fixtures;
- independently permissioned read-only retrieval and credential-free/network-free sanitizer jobs;
- digest-verified artifact-only handoff;
- independent consumer validation of exact canonical bytes and identities;
- documentation and fixtures showing how later envelopes bind subject, time, replay, policy, privacy, completion, correction, revocation, and recovery without rewriting canonical-record v1;
- documentation showing how access, purpose, source terms, personal-data risk, retention, sharing, and publication decisions remain independent and fail closed;
- JSON and optional PDF evidence outputs;
- exact-source, minimum-permission, dependency, package-boundary, hidden-control, and consent-capacity checks;
- accurate Pages documentation, obstruction/gluing analysis, checksums, provenance, recovery, rollback, and approval evidence.

### Explicit exclusions

- General crawling or browser automation.
- Authenticated or private-source acquisition.
- Source-driven execution, import, compilation, shell use, or package installation.
- Scheduled or live collection service.
- Automatic source-rights, legal, privacy, retention, deletion, or publication decisions.
- Automatic repository writes or package publication.
- Autonomous truth promotion, learning, genome generation, or spawning.
- QSIO runtime authority, canonical-state authority, observation-envelope authority, or shared-field publication.
- Automatic mutation of QSO-GENOMES, QuantumStateObjects, or QSO-FABRIC state.
- Any capability present only in an unmerged draft pull request.

## Accepted work

Canonical-record and attribution-sidecar contract v1 are accepted implementation on `main`. They define exact fields, strict canonical JSON, SHA-256 content/source/record/sidecar identities, normalized relative paths, HTTPS URLs, canonical collections, fail-closed validation, and an inert-data authority boundary.

The repository-wide consent-capacity control is also accepted on `main`: strict JSON validation, repository-wide scope semantics, focused regressions, pinned Actions, exact submitted-head checkout and assertion, least-privilege workflow permissions, disabled credential persistence, and retained checksum evidence were merged through PR #11.

The Pages documentation candidate records the implemented components, distinguishes basic sanitizer output from canonical handoff artifacts, documents the target retrieval-to-sanitizer separation without claiming that P2 is already complete, maps portfolio obstructions, and defines candidate envelope and source-review methods without activating any external route or authority.

## Candidate portfolio ownership model

The documentation proposes the following lowest-overlap split:

- QSO-SEEKER owns source-facing sanitization, canonical-record v1 construction, attribution sidecars, and local rejection evidence.
- A neutral owner, not yet selected, owns the future source-observation envelope contract and registry.
- Named legal/source-rights, privacy, security, retention, deletion/legal-hold, and publication authorities own their respective decisions; QSO-SEEKER does not infer them from source visibility or sanitization success.
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
| Task completion | FAIL | P0 accepted; P1 remains accepted; P2-P3 and G0-G2 complete; D0 documentation accepted. |
| Contract determinism | PASS FOR V1 | PR #10 merged deterministic canonical-record and sidecar v1 validation and mutation tests; language-neutral fixtures, an independent consumer witness, and final release replay remain required. |
| Security isolation | FAIL | Retrieval and sanitizer must be independently permissioned; sanitizer must lack source credentials/network/repository-write authority and verify the handoff digest. |
| Adversarial validation | PARTIAL | Existing tests cover core sanitizer and contract behavior; complete versioned handoff, cross-language, cross-repository, wrong-subject, stale/replay, correction/revocation, partial-collection, and consumer conformance fixtures remain pending. |
| Portfolio gluing | BLOCKED | Subject, temporal, source-observation-envelope, policy, transport, canonical-state, reason-code, correction/revocation, privacy/retention, emergency-stop, and recovery ownership must be versioned and witnessed. |
| Source rights and privacy | DOCUMENTED / BLOCKED | Review axes, states, source classes, minimization, artifact separation, correction, withdrawal, deletion, legal hold, and publication separation are documented; named owners, source-specific evidence, decisions, and exact review records remain required. |
| Observation-envelope governance | PROPOSED | Approve neutral owner, contract ID, serialization, signing/attestation, subject and temporal binding, policy/privacy fields, lifecycle receipts, version negotiation, migration, and rollback. |
| Workflow integrity | REVIEW | Exact-head and least-permission evidence exists for accepted contract and consent-control candidates; one final current-composition replay with retained artifacts is required. |
| Consent-capacity control | PASS FOR CURRENT MAIN | PR #11 merged the repaired repository-wide validator, regression tests, exact-head workflow, pinned Actions, and retained evidence; final release replay remains required. |
| Scope integrity | PASS | Broader collection, live checkpoint, experimental spawning, action protocol, QSIO integration, source-observation envelope, source-policy automation, and shared-field work remain separate candidates. |
| Documentation | REVIEW | Pages foundation covers overview, architecture, contracts, source-observation envelope, source-rights/privacy review, obstruction/gluing, API/CLI, security, onboarding, operations, governance, punch list, and diagrams; strict build evidence is required on the final head. |
| Legal/privacy/license | BLOCKED | Source terms, attribution, privacy, minimization, retention, redaction, internal-envelope handling, deletion/legal hold, and any later collection/publication model require explicit approval. |
| Provenance | PARTIAL | Contract hashes and exact commit identities exist; retained release bundle, complete checksums, attestations, decision history, and rejected-candidate records remain incomplete. |
| Operations and rollback | PARTIAL | Procedures are documented; end-to-end freeze, evidence preservation, revocation propagation, cache invalidation, rollback, and bounded recovery require a retained exercise. |
| Deployment readiness | BLOCKED | No live, private, scheduled, runtime, canonical-state, observation-envelope, source-policy, or publication target is approved. |
| Approval | PENDING | Architect and each designated domain owner must approve the final immutable candidate after all blocking gates pass. |

## Required artifacts

- Source and package artifacts from the final accepted head.
- Canonical-record and attribution-sidecar specifications and machine-readable schemas.
- Candidate source-observation-envelope specification, accepted ownership decision, schema, canonical byte fixtures, and migration record if it proceeds.
- Source-rights/privacy review records for each permitted source class, including current terms or license snapshots, purpose, minimization, retention, consumer, correction/withdrawal, and publication dispositions.
- Language-neutral canonical byte fixtures and at least one independent consumer witness.
- Positive, negative, boundary, mutation, Unicode, dependency, digest-mismatch, stale, replay, wrong-subject, wrong-producer, privacy-downgrade, partial-collection, correction, revocation, and independent-consumer fixtures with expected identities.
- Pairwise and triple-overlap witness evidence across retrieval, sanitizer, canonical producer, observation envelope, temporal validation, Bridge, Repository `1`, QSO-STUDIO/AionUi, QSO-DIGITALIS, QSO-GENOMES, and QuantumStateObjects.
- Accepted, audit, JSON report, representative PDF, correction, revocation, freeze, and recovery outputs.
- Exact-head workflow logs, test reports, security verifier output, hidden-control results, permissions inventory, consent-lock evidence, and documentation build output.
- Artifact checksums, dependency inventory or SBOM where applicable, provenance manifest or attestation, and reviewer decisions.
- Recovery and rollback exercise evidence.
- Legal, privacy, attribution, source-term, redaction, retention, deletion, legal-hold, and publication approval records.

## Deployment and operations posture

The first verification target must be disposable and bounded. Source reading must be read-only. Sanitization must be credential-free, network-free, and repository-write-free, and must accept only a digest-verified artifact. Health requires exact source identity, deterministic record identities, complete audit decisions, no source-content execution, minimum permissions, visible failures, and no secrets or prohibited source data in evidence.

Downstream health also requires explicit treatment of `observed`, `sanitized`, `unverified`, `complete`, `partial`, `failed`, `unsupported`, `unknown`, `corrected`, and `revoked` states. A valid record hash, envelope, successful transport, visible interface, or runtime ingestion is not source permission, privacy approval, canonical acceptance, or verified truth.

Roll back on source drift, nondeterministic identities, execution paths, missing digest verification, permission leakage, dependency drift, contract mismatch, wrong-subject binding, stale or replayed evidence, privacy-class downgrade, failed correction/revocation propagation, source-rights or privacy violations, or documentation that overstates the boundary. Preserve evidence, quarantine affected artifacts, restore the prior accepted revision, revoke temporary permissions, invalidate downstream caches where authorized, rerun the full suite, and record human disposition.

## Unresolved blockers

- Final current-main P0 replay and Architect acceptance with retained artifacts.
- P2 independent retrieval/sanitizer permission split and digest-verified handoff.
- P3 complete adversarial, cross-language, and consumer conformance fixtures.
- G0 accepted ownership for subject identity, source lineage, time/freshness/replay, source-observation envelopes, reason codes, correction/revocation, privacy/retention, emergency stop, and recovery.
- G2 named source-rights, privacy, retention, deletion/legal-hold, and publication owners plus source-specific review evidence.
- Neutral source-observation-envelope owner, namespace, serialization/signing, compatibility, migration, and rollback decision.
- Strict Pages build and review of the reconciled documentation foundation.
- Complete provenance, checksums, rollback exercise, privacy, source-term, attribution, redaction, retention, and release approval evidence.
- Disposition of open action-protocol, collection-core, live-checkpoint, spawning, and QSIO candidates.
- Downstream consumers must not treat QSO-SEEKER artifacts or candidate envelopes as authoritative until the release contract is published by version and hash.

## Release log

- 2026-07-16 — Defined the first release as a secure, read-only hostile-input boundary.
- 2026-07-17 — Historical PR #2 exact-head checks passed for its candidate, but final retained evidence and Architect acceptance remained incomplete.
- 2026-07-17 — Broader collection and private-overlay work was excluded from the first release.
- 2026-07-18 — PR #10 merged canonical-record and attribution-sidecar contract v1 after exact-head verification.
- 2026-07-18 — Consent-capacity policy and CI enforcement were added.
- 2026-07-19 — Proposed a complete Pages, architecture, contract, API/CLI, security, onboarding, operations, governance, and diagram documentation foundation without changing runtime scope.
- 2026-07-20 — PR #11 merged the exact-head repository-wide consent-lock repair; the documentation candidate was reconciled to the accepted workflow, validator, tests, and release status.
- 2026-07-20 — Added the obstruction/gluing ledger, triple-overlap witnesses, expanded punch list, and portfolio ownership gates without changing runtime or authority scope.
- 2026-07-20 — Added the documentation-only candidate source-observation envelope profile and aligned release gates without changing canonical-record v1 or activating an integration route.
- 2026-07-23 — Added the documentation-only source-rights and privacy review, aligned release gates and required evidence, and preserved all collection, processing, retention, deletion, and publication holds.
