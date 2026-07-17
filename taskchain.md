# Task Chain

## Repository role

Read-only retrieval boundary, hostile-input sanitization, canonical-record production, attribution sidecars, and evidence reports for QSO experiments.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

## Product directive

- **Next objective:** Prove a read-only, fail-closed path from untrusted public input to an inert canonical record and attribution sidecar.
- **User outcome:** A researcher can retrieve supported public content and receive deterministic accepted/rejected artifacts with provenance and hashes, while the sanitizer has no credentials, repository write permission, or content-execution path.
- **MVP scope:** reproduce tests/CLI/PDF/security baseline; version canonical-record and attribution schemas; split retrieval and sanitizer into separately permissioned jobs with artifact-only handoff; verify digest; publish adversarial fixtures for prompt injection, Unicode concealment, executables, binaries, malformed attribution, and oversized input.
- **Priority:** Security isolation and deterministic contract publication precede broader source coverage or integration with the QSO runtime.
- **Success criteria:** full checks pass at one immutable commit; accepted/rejected outputs and hashes are repeatable; sanitizer job is credential-free and network-free; missing or changed digests fail closed; no fetched material is executed; documentation describes actual rather than implied isolation.
- **Non-goals:** general web crawling, authenticated/private-source acquisition, autonomous learning, executable artifact processing, browser automation, or runtime decision authority.
- **Release rationale:** QSO-SEEKER is the hostile-input boundary for the portfolio. Its contract must be independently trustworthy before retrieved material can enter experiments.

## Active chain

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0 | Establish a reproducible security and CLI baseline | QSOBuilder | — | IN PROGRESS | Full pytest, security-envelope, CLI JSON, PDF report, and workflow checks pass or failures have retained reproducers; no fetched content executes. |
| P1 | Version the canonical record and attribution-sidecar contract | QSOBuilder | P0 | PROPOSED | Schemas and fixtures define fields, transformations, limits, rejection reasons, provenance, hashes, and independent consumer validation. |
| P2 | Split retrieval and sanitizer into independently permissioned jobs | QSOBuilder | P0 | PROPOSED | Fetch is read-only; sanitizer receives a verified inert artifact, has no network/repository credential, and fails closed on missing or changed digest. |
| P3 | Publish adversarial conformance fixtures | Builder | P1 and P2 | PROPOSED | Hostile and malformed inputs produce deterministic accepted/rejected outputs without execution or provenance loss. |

## P0 baseline candidate — PR #2

**Status:** `REVIEW — INSTALLATION AND SOURCE-IDENTITY FAILURE BLOCK ACCEPTANCE`

PR #2 remains the single bounded P0 candidate at head `9e2d83e4156b77e177a4e478de3d46271174f77a`. It records local candidate evidence from implementation/test commit `1c55ee45edbb4fe05c27efcb9c4c6d4e375a9321`: the security-envelope verifier, 11 pytest tests, Python compilation, CLI JSON/audit/evidence/PDF replay, workflow YAML and read-only permission inspection, and the tracked-text hidden-control scan passed in the documented local environment. The candidate also repairs deterministic whitespace collapse and replaces fragile dependency-string parsing with standard-library `tomllib` plus focused tests.

Security Envelope run `29564563760` is associated with the current PR head but checked out pull-request merge ref `58084e0978bb30970a6cd2e919c96819622ecdf8`, not the submitted head itself. The run failed at `Install minimal test environment`; the capability verifier, adversarial/deterministic tests, and hidden-control scan were skipped, and no successful artifact bundle was retained. GitHub reports PR #2 non-mergeable. The earlier local Contents-API replay remains useful candidate evidence but does not replace a successful exact submitted-head or independently reviewed clean-checkout replay.

**Directive:** preserve PR #2 as the single P0 path; diagnose the installation failure from the retained job logs; make only the bounded dependency/build/workflow correction required; configure CI to check out and assert the exact submitted head rather than a synthetic merge ref; rerun the complete suite with retained logs and artifacts; and keep P1/P2 work from being treated as accepted until P0 is independently reproducible. Product scope and portfolio priority are unchanged.

## Architectural boundary

Until P2 is complete, retrieval and sanitization are only logically separated. Documentation must not call the current single-job workflow process, container, or microVM isolation.

## Builder Log

Record commits, workflow runs, exact test commands/results, fixture and artifact hashes, permission evidence, rejected samples, residual risks, and follow-ups.

- 2026-07-17 — Reviewed PR #2 at head `9e2d83e4156b77e177a4e478de3d46271174f77a`. Local candidate checks and recorded artifact hashes narrow P0, but the initial Security Envelope run failed during environment installation before the verifier or tests executed. P0 advanced to `IN PROGRESS`; priority remained unchanged.
- 2026-07-17 — Confirmed current-head-associated run `29564563760` also failed during environment installation after checking out PR merge ref `58084e0978bb30970a6cd2e919c96819622ecdf8`. All substantive checks were skipped, PR #2 is non-mergeable, and no exact submitted-head or independent clean-checkout acceptance exists. The next action is a bounded install/checkout repair and complete replay, not P1/P2 expansion.
