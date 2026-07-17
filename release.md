# Release Plan

## Current Decision

Status: `BLOCKED — PR #2 P0 DISPOSITION, RETAINED EVIDENCE, CONTRACT ISOLATION, AND SECURITY/LEGAL GATES REQUIRED`

QSO-SEEKER has one bounded hostile-input P0 candidate in PR #2. Current head `306dfa4104c12594b23dda8111e1c80edb0be397` is open and mergeable. Security Envelope run `29580240905` passed exact submitted-head checkout/assertion, editable installation, capability-envelope verification, adversarial/deterministic tests, and hidden-control scanning. No workflow artifacts were retained, Architect disposition remains pending, and P1-P3 canonical-contract/isolation/conformance work is incomplete; no release is eligible.

Draft PR #5 at head `49f07a4d79c78cc2832dc7a4e9930db7b7d3c51f` is a separate later proposal for public source registries, adapters, deterministic fixture collection, private deployment overlays, scheduled collection CI, a draft source-available license, and Digital Consciousness Field publication envelopes. It does not supersede PR #2 and is excluded from the first release until a separately approved architecture, security, legal/license, privacy, retention, scheduling, provenance, rollback, and downstream-contract cycle passes.

## Versioning

- Semantic Versioning applies to the CLI, canonical-record schema, attribution sidecar, sanitizer handoff, and later source-adapter contracts.
- First eligible hostile-input candidate remains `0.1.0-alpha.1`.
- Security-boundary, required-field, transformation, canonicalization, isolation, hash, retention, or publisher-envelope changes require explicit compatibility review and migration fixtures.
- Broader collection/private-overlay/field-publication work requires a separately versioned later candidate and may not enter `0.1.0-alpha.1` implicitly.
- No tag may be created until one immutable head passes tests, security, documentation, provenance, artifacts, rollback, legal/privacy, and approval gates.

## Release Scope

- Reproducible pytest, security-envelope, CLI JSON/PDF, exact-source, hidden-control, and minimum-permission baseline.
- Versioned canonical-record and attribution-sidecar schemas with deterministic accepted/rejected fixtures and hashes.
- Separate read-only retrieval and credential-free, network-free sanitizer jobs with artifact-only handoff and digest verification.
- Adversarial fixtures for Unicode concealment, prompt injection, executable/binary types, oversized input, malformed attribution, dependency drift, and digest mismatch.
- Accurate trust-boundary documentation, security reports, checksums, provenance, rollback, and approved privacy/license notices.

### Explicitly excluded from the first candidate

- Draft PR #5 source-registry expansion, private overlays, scheduled collection, live retrieval, draft ecosystem license, Digital Consciousness Field publication contracts, and downstream field integration.
- General crawling, authenticated/private-source acquisition, browser automation, executable processing, runtime authority, or autonomous conclusions.

## Selected Candidate Work

PR #2 remains the sole P0 candidate. Its current exact-head pass is review evidence, not release authority. P0 may move to `DONE` only after Architect disposition of the exact head and an accepted retained-evidence strategy. P1-P3 must then publish and independently validate the canonical record, attribution, permission split, artifact-digest handoff, adversarial fixtures, documentation, provenance, and rollback behavior.

## Planned Changelog Entries

- `Fixed`: deterministic normalization, standards-based dependency parsing, bounded package discovery, and exact submitted-head workflow identity after independent acceptance.
- `Added`: versioned canonical-record and attribution contracts, deterministic fixtures/hashes, and independently permissioned artifact handoff.
- `Security`: credential-free/network-free sanitizer, fail-closed digest verification, least privilege, hidden-control scan, and adversarial conformance.
- `Documentation`: actual isolation, supported contracts, privacy/license/source obligations, retention, limitations, consumer guidance, and recovery.
- `Release`: source/package artifacts, CLI/PDF samples, reports, SBOM where applicable, checksums, provenance, rollback evidence, and approval.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Canonical P0 | REVIEW | PR #2 exact current head passed run `29580240905`; Architect disposition and retained-evidence requirements remain. |
| Task completion | FAIL | P0 accepted as `DONE`; P1-P3 completed with linked immutable evidence. |
| Contract determinism | INCOMPLETE | Versioned schemas/fixtures reproduce identical transformations, decisions, rejection reasons, provenance, and hashes. |
| Security isolation | FAIL | Retrieval and sanitizer are independently permissioned; sanitizer has no credentials/network and verifies artifact digests before processing. |
| Adversarial validation | PARTIAL | Baseline tests pass at the reviewed head; complete versioned contract/handoff fixture matrix remains unaccepted. |
| Workflow integrity | REVIEW | Exact-head/read-only/no-persisted-credentials behavior passed; retained release artifacts and split-job controls remain absent. |
| Scope integrity | PASS | Draft PR #5 is explicitly deferred and may not activate scheduled/live/private or field-publication capability. |
| Documentation | PARTIAL | P0 setup/root cause exist; contract versions, actual isolation, source/license/privacy/retention boundaries, failure recovery, and consumer guidance remain incomplete. |
| Legal/privacy/license | BLOCKED | Draft PR #5 license and source/private-overlay model require explicit legal, source-terms, privacy, retention, and publication approval before later use. |
| Provenance | PARTIAL | Current exact-head run is recorded; retained artifacts, release checksums, attestations, complete fixture identities, and rollback drill remain absent. |
| Deployment readiness | BLOCKED | No live, private, scheduled, or field-publication target is approved; first target must remain fixture-only and network-disabled. |
| Approval | PENDING | Architect P0 disposition followed by explicit release approval after every blocking gate passes. |

## Artifact Requirements

- Versioned canonical-record and attribution schemas plus positive, negative, adversarial, boundary, dependency, and digest-mismatch fixtures with expected hashes.
- Source/package artifact, CLI sample, JSON/PDF evidence, independently permissioned workflows, exact-head logs, and retained artifacts.
- Complete clean-checkout, security-envelope, hidden-control, permissions, isolation, privacy/license/source-terms, documentation, health, rollback, and post-validation reports.
- SBOM where applicable, checksums, provenance manifest/attestation, rejected-candidate records, and tested rollback evidence.

## Deployment Readiness, Health, Observability, Rollback, and Post-Validation

No deployment, schedule, live/private retrieval, or Digital Consciousness Field publication is authorized. A future first verification target must be disposable, fixture-only, credential-free, network-disabled for sanitization, read-only for retrieval, and use a digest-verified artifact handoff. Health requires exact source identity, deterministic accepted/rejected outputs and hashes, no execution, minimum permissions, visible failures, and no private data or credentials in artifacts. Observability must record source/configuration identity, decisions/rejections, transformations, hashes, permission boundaries, handoff digests, limits, denied capabilities, cleanup, and post-validation without storing secrets or prohibited source material. Roll back on source drift, nondeterminism, execution, missing digest verification, permission/network/credential leakage, source/license/privacy violation, or misleading isolation claims; preserve evidence, restore the prior accepted state, disable schedules/adapters, verify no external mutation, and rerun the complete fixture suite. Post-validation repeats deterministic replay, verifies artifacts/hashes and cleanup, confirms disablement/revocation, and archives human disposition.

## Unresolved Blockers

- Architect disposition of PR #2 exact head and an accepted retained-artifact strategy.
- P1 canonical-record/attribution schemas, P2 independent permission split/digest handoff, and P3 complete adversarial conformance.
- Complete security, documentation, provenance, rollback, privacy/license, and consumer-acceptance evidence.
- Draft PR #5 requires separate architecture, legal/license/source, privacy, retention, schedule, security, provenance, rollback, and downstream-contract approval and remains excluded.
- QuantumStateObjects cannot consume an authoritative QSO-SEEKER contract until P1-P3 are accepted and published by version/hash.

## Release Log

- 2026-07-16 — Aligned the candidate with the secure read-only hostile-input MVP.
- 2026-07-17 — PR #2 current head `306dfa4104c12594b23dda8111e1c80edb0be397` passed Security Envelope run `29580240905`; no artifacts were retained and release remained blocked.
- 2026-07-17 — Classified draft PR #5 as a later public-collection/private-overlay/field-publication proposal outside P0-P3 and the first release; no scheduled or live capability was authorized.
