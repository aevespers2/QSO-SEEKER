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
| P0 | Establish a reproducible security and CLI baseline | QSOBuilder | — | REVIEW | Full pytest, security-envelope, CLI JSON, PDF report, workflow, exact-source, and hidden-control checks pass at one submitted immutable head with retained evidence; Architect accepts, rejects, or requests bounded rework; no fetched content executes. |
| P1 | Version the canonical record and attribution-sidecar contract | QSOBuilder | P0 | PROPOSED | Schemas and fixtures define fields, transformations, limits, rejection reasons, provenance, hashes, and independent consumer validation. |
| P2 | Split retrieval and sanitizer into independently permissioned jobs | QSOBuilder | P0 | PROPOSED | Fetch is read-only; sanitizer receives a verified inert artifact, has no network/repository credential, and fails closed on missing or changed digest. |
| P3 | Publish adversarial conformance fixtures | Builder | P1 and P2 | PROPOSED | Hostile and malformed inputs produce deterministic accepted/rejected outputs without execution or provenance loss. |

## P0 baseline candidate — PR #2

**Status:** `REVIEW — EXACT-HEAD BASELINE PASSED; ARCHITECT DISPOSITION REQUIRED`

PR #2 remains the single bounded P0 candidate at submitted head `75e9ebd578898bfba47f24d9619535ba025bc921`. Security Envelope run `29576874153` (#33) completed successfully after checking out and asserting that exact submitted head. Editable installation, capability-envelope verification, adversarial and deterministic tests, and the hidden-control scan passed. GitHub reports the pull request mergeable.

The prior installation failure was reproduced as setuptools flat-layout auto-discovery of `schemas`, `contracts`, and `unicernal_search`. The candidate repair limits package discovery to `unicernal_search*`, preserves the deterministic whitespace and standards-based `tomllib` dependency-envelope corrections, and adds focused packaging-discovery and dependency regression tests. The candidate workflow retains `contents: read` and disables checkout credential persistence.

This closes the installation and source-identity blocker for the candidate, but it does not itself accept P0 or authorize release. The Architect must review the retained exact-head evidence and candidate scope, then accept, reject, or request bounded rework. P1, P2, and P3 remain unaccepted; retrieval and sanitization remain only logically separated until P2 is completed.

**Directive:** hold further branch expansion unless review identifies a bounded P0 defect. If the Architect accepts the candidate, mark P0 `DONE` and decompose P1 and P2 without representing either contract publication or security isolation as implemented. Do not broaden source coverage or begin runtime integration. Product scope and portfolio priority are unchanged.

## Architectural boundary

Until P2 is complete, retrieval and sanitization are only logically separated. Documentation must not call the current single-job workflow process, container, or microVM isolation.

## Builder Log

Record commits, workflow runs, exact test commands/results, fixture and artifact hashes, permission evidence, rejected samples, residual risks, and follow-ups.

- 2026-07-17 — Reviewed PR #2 at head `9e2d83e4156b77e177a4e478de3d46271174f77a`. Local candidate checks and recorded artifact hashes narrowed P0, but the initial Security Envelope run failed during environment installation before the verifier or tests executed. P0 advanced to `IN PROGRESS`; priority remained unchanged.
- 2026-07-17 — Confirmed current-head-associated run `29564563760` also failed during environment installation after checking out PR merge ref `58084e0978bb30970a6cd2e919c96819622ecdf8`. All substantive checks were skipped, PR #2 was non-mergeable, and no exact submitted-head or independent clean-checkout acceptance existed. The next action remained a bounded install/checkout repair and complete replay, not P1/P2 expansion.
- 2026-07-17 — Re-reviewed final submitted head `75e9ebd578898bfba47f24d9619535ba025bc921`. Security Envelope run `29576874153` succeeded with exact-source assertion, editable installation, capability verification, adversarial/deterministic tests, and hidden-control scanning, and GitHub reports the PR mergeable. P0 advanced to `REVIEW` pending Architect disposition; release and the P1-P3 capability claims remain blocked.