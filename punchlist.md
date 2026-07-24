# QSO-SEEKER Punch List

This punch list converts the current task chain, release gates, documentation review, and obstruction analysis into bounded work. Completion requires immutable evidence; a checked box without a linked commit, workflow, artifact, review, or decision is not release evidence.

## P0 — Current composition and ownership

- [ ] Select one immutable candidate head containing the accepted canonical-record v1 and consent-capacity controls.
- [ ] Reproduce clean installation, imports, complete tests, capability verification, hidden-control scan, consent validation, and documentation build on that exact head.
- [ ] Retain logs, test reports, dependency inventory, exact-head identity, permissions inventory, and SHA-256 manifest.
- [ ] Record Architect disposition for the local sanitizer and canonical-record baseline.
- [ ] Approve or revise the repository responsibility statement: hostile-input boundary, not canonical truth, runtime, or publication authority.
- [ ] Assign owners for contract evolution, security, privacy, legal/source terms, release, incident response, emergency stop, rollback, and recovery.

## P1 — Canonical-record v1 conformance

- [x] Merge exact canonical-record and attribution-sidecar fields and validation semantics.
- [x] Merge deterministic canonical JSON and content/source/record/sidecar SHA-256 identities.
- [x] Reject unknown fields, unsupported versions, malformed URLs and paths, invalid collections, mutation, and noncanonical values.
- [ ] Publish language-neutral canonical byte fixtures.
- [ ] Validate at least one independent consumer implementation or separately implemented verifier.
- [ ] Define namespaced reason codes for schema, sanitization, policy, temporal, legal, privacy, and consumer failures.
- [ ] Record correction, supersession, and attribution-sidecar migration rules.

## P2 — Retrieval and sanitizer isolation

- [ ] Define the versioned retrieval-artifact handoff envelope.
- [ ] Run retrieval and sanitization as independently permissioned jobs or processes.
- [ ] Prove the sanitizer has no source credentials, network dependency, repository-write token, shell execution path, or package-install path.
- [ ] Verify artifact digest, size, media type, source-policy reference, and expected producer before parsing.
- [ ] Fail closed on missing, changed, truncated, oversized, replayed, or unsupported artifacts.
- [ ] Retain positive and negative permission evidence.
- [ ] Exercise rollback from a failed or contaminated handoff.

## P3 — Adversarial and cross-repository conformance

- [ ] Publish supported, rejected, malformed, concealment, prompt-injection, executable, binary, Unicode, oversize, and mutation fixtures.
- [ ] Add digest mismatch, stale, replay, wrong-subject, wrong-source, unsupported-version, and expected-head fixtures.
- [ ] Add duplicate, contradictory, partial, correction, revocation, and cache-invalidation fixtures.
- [ ] Demonstrate sanitizer → canonical producer agreement.
- [ ] Demonstrate Seeker → source-observation envelope agreement without changing canonical-record v1.
- [ ] Demonstrate Seeker → temporal validator → Repository `1` agreement.
- [ ] Demonstrate Seeker → Bridge → QSO-STUDIO/AionUi agreement.
- [ ] Demonstrate Seeker → QSO-DIGITALIS → QuantumStateObjects evidence-only behavior.
- [ ] Demonstrate Seeker → QSO-GENOMES → QuantumStateObjects evidence-only behavior.
- [ ] Bind all witness results to immutable commits and one evidence manifest.

## P4 — Portfolio contract ownership

- [ ] Designate the neutral owner of the cross-repository source-observation/evidence envelope.
- [ ] Select the normative contract ID, package or registry location, canonical serialization, version negotiation, and signing or attestation method.
- [ ] Designate stable subject-identity, source-lineage, device/environment authorization, and ownership-reference methods.
- [ ] Designate clock, uncertainty, freshness, replay, and ordering ownership.
- [ ] Approve the responsibility split among QSO-SEEKER, QSO-DIGITALIS, Bridge, Repository `1`, datarepo-temporal-invariants, QSO-GENOMES, QuantumStateObjects, QSO-FABRIC, and `qsio-kernel`.
- [ ] Define the exact Seeker → observation envelope → temporal validation → Digitalis/Bridge → Repository `1` route or remove unsupported edges.
- [ ] Define collection-completion vocabulary that preserves `complete`, `partial`, `failed`, `unsupported`, and `unknown`.
- [ ] Define namespaced reason-code registry ownership and compatibility.
- [ ] Define policy, privacy, access, source-term, retention, and redaction reference ownership.
- [ ] Define correction, supersession, revocation, freeze, downstream invalidation, recovery, and bounded-restart contracts.
- [ ] Pin producer and consumer contract versions with compatibility, migration, and rollback guidance.
- [ ] Preserve canonical-record and sidecar bytes during any envelope migration.

## P5 — Source rights, privacy, and deployment boundary

- [x] Document independent review axes for access, purpose, terms/license, privacy, sensitivity, retention, transformation, sharing, and publication.
- [x] Document fail-closed review states, source-class starting dispositions, artifact-class separation, and reviewer onboarding.
- [ ] Assign named legal/source-rights, privacy, security, retention, deletion, legal-hold, and publication decision owners.
- [ ] Define the public adapter interface and safe example registry.
- [ ] Define the private deployment manifest without storing credentials, sessions, private locators, or sensitive raw artifacts in the public repository.
- [ ] Approve source classes, terms, licenses, privacy purposes, retention periods, and redaction rules.
- [ ] Record current canonical terms or license snapshots and validity windows for every permitted source class.
- [ ] Require a bounded-purpose and data-minimization disposition before any retrieval route is enabled.
- [ ] Separate accepted records, rejected evidence, raw source bytes, reports, logs, observation envelopes, authority receipts, and publication artifacts by access class.
- [ ] Verify evidence artifacts cannot leak private locators, source fragments, credentials, stable private-device identifiers, reviewer identities, or operational secrets.
- [ ] Define deletion, correction, withdrawal, expiry, supersession, legal hold, and incident-preservation behavior.
- [ ] Require policy-decision receipts before live or scheduled collection.
- [ ] Define a separate minimized publication profile rather than publishing internal observation envelopes directly.
- [ ] Validate keyboard, zoom/reflow, screen-reader, cognitive-access, and non-color state communication on the exact publication candidate.

## P6 — Draft-candidate disposition

- [x] Reconcile or retire historical P0 candidate PR #2 against current `main`. Closed without merge as preserved provenance on 2026-07-21; PR #14 remains the current preservation-safe reconciliation path. Evidence: `reports/semiweekly-repository-pruning-20260721.md`.
- [ ] Decide whether the action-protocol candidate belongs in QSO-SEEKER, Repository `0`, or should be retired.
- [ ] Decide whether the public/private collection-core candidate proceeds after P0-P5.
- [ ] Decide whether the bounded live checkpoint remains useful after the isolation contract exists.
- [ ] Move or retire experimental genome and spawning responsibilities that overlap QSO-GENOMES and QSO-FABRIC.
- [ ] Hold QSIO integration disabled until shared envelope ownership and conformance are approved.
- [ ] Preserve rejected-candidate evidence and migration notes.

## D0 — Pages and developer documentation

- [x] Add Pages navigation and project overview.
- [x] Document architecture, components, trust boundaries, topology, and record lifecycle.
- [x] Document canonical-record and attribution-sidecar v1.
- [x] Document the candidate source-observation envelope, state machine, fail-closed consumer duties, reason-code domains, migration, and rollback.
- [x] Document source-rights, privacy, retention, correction, withdrawal, deletion, legal-hold, handoff, and publication-review boundaries.
- [x] Document CLI, Python API, security, onboarding, operations, recovery, and governance.
- [x] Add accessible architecture and lifecycle diagrams.
- [x] Add obstruction and gluing analysis.
- [x] Add this punch list and align task, release, and change records.
- [ ] Pass `mkdocs build --strict` on the final documentation head.
- [ ] Validate internal links, terminology, diagrams, scope statements, and exact repository URLs.
- [ ] Retain rendered-site evidence and checksums.
- [ ] Confirm whether and how GitHub Pages publication is approved.

## R0 — Release evidence and rollback

- [ ] Create one final release manifest binding source commit, contract versions, workflows, artifacts, checksums, toolchain, dependency inventory, permissions, and approvals.
- [ ] Complete legal, privacy, attribution, licensing, retention, and source-term review.
- [ ] Perform an end-to-end wrong-subject, stale, replay, correction, revocation, freeze, evidence-preservation, cache-invalidation, rollback, and bounded-recovery exercise.
- [ ] Confirm no unresolved review threads, stale checks, superseded artifacts, or contradictory planning documents.
- [ ] Obtain explicit release and publication approval.
- [ ] Tag or publish only after every blocking gate passes.
