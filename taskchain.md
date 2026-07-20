# Task Chain

## Repository role

Read-only hostile-input boundary for bounded QSO research: strict local record validation, inert text sanitization, canonical-record production, attribution sidecars, audit evidence, and independently validated artifact handoff.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** replay the accepted canonical-record v1 and repository-wide consent-control baseline on one immutable current head, then implement the independently permissioned retrieval-to-sanitizer artifact handoff and complete adversarial conformance.
- **User outcome:** a researcher can convert supported untrusted public input into deterministic accepted or rejected inert records with provenance and hashes while the sanitizer has no source credentials, network dependency, repository-write permission, or content-execution path.
- **Accepted scope:** local CLI processing; strict schemas; sanitization and rejection; audit and report output; canonical-record and attribution-sidecar contract v1; repository security and consent-capacity controls.
- **Priority:** P0 baseline disposition and P2-P3 isolation/conformance precede source-registry expansion, live or scheduled collection, private overlays, experimental spawning, QSIO runtime integration, shared-field publication, or downstream authority.
- **Success criteria:** one immutable accepted head has reproducible tests, deterministic contract fixtures and hashes, credential-free sanitizer isolation, digest-verified handoff, retained evidence, accurate Pages documentation, provenance, rollback, legal/privacy review, and explicit human approval.
- **Non-goals:** general crawling, authenticated/private-source acquisition, executable processing, browser automation, autonomous truth promotion, unsupervised learning, repository mutation from source content, or publication before separate approval.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0 | Disposition the reproducible security and CLI baseline | QSOBuilder / Architect | — | REVIEW | Current baseline, including contract v1 and the merged consent-lock repair, is replayed on a final immutable head with clean install, complete tests, verifier, hidden-control scan, exact-source assertion, minimum permissions, retained evidence, and Architect acceptance. |
| P1 | Version canonical record and attribution-sidecar semantics | QSOBuilder | P0 evidence basis | DONE | Contract identifiers, exact fields, canonical JSON, content/source/record/sidecar hashes, fail-closed validation, compatibility rules, and deterministic mutation tests were merged in PR #10. |
| P2 | Split retrieval and sanitizer into independently permissioned jobs | QSOBuilder | P0 | PROPOSED | Source reading is read-only; sanitizer receives a bounded artifact plus digest, has no source credentials/network/repository-write token, and fails closed on a missing or changed digest. |
| P3 | Publish adversarial conformance and consumer fixtures | Builder | P1 and P2 | PROPOSED | Versioned fixtures cover concealment, injection, executable/binary input, malformed attribution, oversize, dependency drift, digest mismatch, mutation, and independent consumer validation. |
| D0 | Establish Pages and developer documentation foundation | Documentation / Architect | P1 | REVIEW | Pages navigation, project overview, architecture and lifecycle diagrams, contracts, API/CLI, security, onboarding, operations, and governance build in strict mode and match current `main`, this task chain, release status, and changelog. |
| P4 | Evaluate broader collection and private-overlay proposal | Architect / Security / Legal | P0-P3 accepted | BLOCKED | Collection sources, source terms, privacy, retention, schedule, permissions, provenance, rollback, licensing, and publisher contracts receive a separate bounded review. |
| P5 | Evaluate experimental genome, spawning, and QSIO candidates | Architect / Security / Research | P0-P3 accepted | BLOCKED | Research claims, capability limits, consent policy, freeze behavior, lineage, evidence, kernel ownership, migrations, and rollback are independently approved without changing the sanitizer baseline implicitly. |

## Accepted contract baseline

PR #10 merged canonical-record and attribution-sidecar contract version 1 after exact-head verification. Version 1 defines strict UTF-8 canonical JSON, exact field sets, deterministic SHA-256 identities, normalized relative paths, HTTPS source URLs, canonical collections, fail-closed validators, and an explicit inert-data authority boundary.

This acceptance does not prove or authorize independent retrieval/sanitizer isolation, live collection, source credentials, repository writes, scheduled operation, runtime use, publication, or autonomous learning.

## Accepted consent-control baseline

PR #11 merged the repository-wide consent-capacity validator, focused regression tests, pinned Actions, exact-head checkout assertion, minimum `contents: read` permissions, credential persistence disabled, and retained SHA-256 evidence. The control is accepted on `main`, but release acceptance still requires one final replay of the complete current composition.

## P0 baseline status

PR #2 remains an open historical P0 candidate, but later `main` changes mean its earlier exact-head evidence cannot serve as final release evidence for the current composition. P0 stays `REVIEW` until the accepted contract and consent-control baseline are replayed together as one immutable head with retained artifacts and no unresolved findings.

## Separate draft candidates

Open proposals for broader collection, a bounded live checkpoint, experimental genome and spawning behavior, QSIO integration, and action orchestration remain separate pull-request candidates. They must not be described as accepted repository capability or used to bypass P0-P3 dependencies.

## Architectural boundary

Retrieval and sanitization are conceptually separate, but documentation may claim independently enforced job or process isolation only after P2 implementation and exact-head evidence. The basic sanitizer output is not automatically a canonical-record v1 artifact; a producer must construct complete provenance and contract identity, and every consumer must validate independently.

## Builder log

Record commits, workflow runs, exact test commands and results, fixture and artifact hashes, permissions, source/license review, rejection samples, residual risks, documentation build output, rollback evidence, and human decisions.

- 2026-07-17 — Historical PR #2 baseline reached Architect review after exact-head workflow evidence; retained release artifacts and final current-main acceptance remained absent.
- 2026-07-17 — Broader collection and private-overlay work was classified outside the first hostile-input release.
- 2026-07-18 — PR #10 merged canonical-record and attribution-sidecar contract v1 after exact-head verification.
- 2026-07-18 — Repository-wide consent-capacity policy and CI enforcement were added.
- 2026-07-19 — Pages, architecture, contracts, API/CLI, security, onboarding, operations, and governance documentation foundation proposed under D0 without changing runtime scope.
- 2026-07-20 — PR #11 merged the exact-head repository-wide consent-lock repair; the documentation branch was reconciled to carry the accepted workflow, validator, tests, and current governance status.
