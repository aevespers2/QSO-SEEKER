# Task Chain

## Repository role

Read-only retrieval boundary, hostile-input sanitization, canonical-record production, attribution sidecars, and evidence reports for QSO experiments.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Accept or reject the exact current PR #2 security/CLI baseline, then version the canonical-record and attribution contracts before broader collection work.
- **User outcome:** A researcher can transform supported untrusted public input into deterministic accepted/rejected inert records with provenance and hashes, while sanitization has no credentials, network access, repository-write permission, or content-execution path.
- **MVP scope:** exact-head baseline; versioned canonical-record and attribution schemas; independently permissioned retrieval and sanitizer jobs with digest-verified artifact-only handoff; adversarial fixtures for concealment, injection, executable/binary inputs, malformed attribution, oversize, and dependency drift.
- **Priority:** PR #2 P0 disposition and accepted P1-P3 contracts/isolation precede source-registry expansion, live/private overlays, scheduled collection, Digital Consciousness Field publication, or runtime integration.
- **Success criteria:** complete checks pass at one immutable accepted head; outputs/hashes are repeatable; sanitizer is credential-free and network-free; missing/changed digests fail closed; no fetched material executes; documentation, licensing, retention, and privacy statements match actual behavior.
- **Non-goals:** general crawling, authenticated/private-source acquisition, autonomous learning, executable processing, browser automation, scheduled live collection, runtime authority, or publication into a shared field before separate approval.
- **Release rationale:** QSO-SEEKER is the portfolio hostile-input boundary; expanding collection before the canonical contract and isolation gates are accepted would increase risk and create competing release paths.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0 | Establish and disposition the reproducible security/CLI baseline | QSOBuilder / Architect | — | REVIEW | PR #2 exact current head passes clean install, verifier, tests, hidden-control scan, exact-source assertion, minimum permissions, and Architect disposition with retained evidence expectations recorded. |
| P1 | Version the canonical record and attribution-sidecar contract | QSOBuilder | P0 | PROPOSED | Schemas and fixtures define fields, transformations, limits, rejection reasons, provenance, hashes, migration, and independent consumer validation. |
| P2 | Split retrieval and sanitizer into independently permissioned jobs | QSOBuilder | P0 | PROPOSED | Fetch is read-only; sanitizer receives a verified inert artifact, has no network/repository credential, and fails closed on missing or changed digest. |
| P3 | Publish adversarial conformance fixtures | Builder | P1 and P2 | PROPOSED | Hostile and malformed inputs produce deterministic accepted/rejected outputs without execution or provenance loss. |
| P4 | Evaluate broader public collection/private-overlay proposal | Architect / Security / Legal | P0-P3 accepted | BLOCKED | Draft PR #5 receives separate scope, source/legal/privacy/license/retention/schedule review and cannot supersede P0 or activate live/scheduled collection. |

## P0 baseline candidate — PR #2

**Status:** `REVIEW — CURRENT EXACT-HEAD CI PASSED; ARCHITECT DISPOSITION AND RETAINED ARTIFACT STRATEGY PENDING`

PR #2 remains the single bounded P0 path. Current head `306dfa4104c12594b23dda8111e1c80edb0be397` is open and mergeable. Security Envelope run `29580240905` passed exact submitted-head checkout/assertion, editable installation, capability-envelope verification, adversarial/deterministic tests, and hidden-control scanning. No workflow artifacts were retained, and P1-P3 remain incomplete; therefore P0 is review evidence, not a release.

## Deferred expansion candidate — draft PR #5

Draft PR #5 head `49f07a4d79c78cc2832dc7a4e9930db7b7d3c51f` proposes source registries, reference adapters, deterministic fixture collection, private deployment overlays, a scheduled workflow, a draft source-available license, and Digital Consciousness Field publication envelopes. The proposal is mergeable but remains outside the accepted hostile-input MVP. It must stay inert until P0-P3 are accepted and a separate architecture, security, legal/license, privacy, retention, provenance, scheduling, rollback, and downstream-contract review authorizes a bounded later version.

## Architectural boundary

Until P2 is accepted, retrieval and sanitization are only logically separated. Documentation must not claim process/container/microVM isolation, safe live collection, or authorized field publication. Private overlays and credentials are deployment-specific and may not enter public artifacts or candidate CI.

## Builder Log

Record commits, workflow runs, exact test commands/results, fixture and artifact hashes, permissions, source/license review, rejected samples, residual risks, rollback evidence, and follow-ups.

- 2026-07-17 — PR #2 current head `306dfa4104c12594b23dda8111e1c80edb0be397` passed Security Envelope run `29580240905`; no artifacts were retained and Architect disposition remains pending.
- 2026-07-17 — Classified draft PR #5 as a later collection/deployment-overlay proposal outside P0-P3; no schedule, live retrieval, private source, license, or Digital Consciousness Field publication capability is authorized.
