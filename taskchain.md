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
| P0 | Establish a reproducible security and CLI baseline | QSOBuilder | — | IN PROGRESS | Full pytest, security-envelope, CLI JSON, PDF report, and workflow checks pass or failures have retained reproducers; no fetched content executes. Local candidate checks pass and evidence is recorded at `reports/p0-security-cli-baseline-20260717.md`; attached workflow run `29564325393` failed during environment installation before verification. |
| P1 | Version the canonical record and attribution-sidecar contract | QSOBuilder | P0 | PROPOSED | Schemas and fixtures define fields, transformations, limits, rejection reasons, provenance, hashes, and independent consumer validation. |
| P2 | Split retrieval and sanitizer into independently permissioned jobs | QSOBuilder | P0 | PROPOSED | Fetch is read-only; sanitizer receives a verified inert artifact, has no network/repository credential, and fails closed on missing or changed digest. |
| P3 | Publish adversarial conformance fixtures | Builder | P1 and P2 | PROPOSED | Hostile and malformed inputs produce deterministic accepted/rejected outputs without execution or provenance loss. |

## Architectural boundary

Until P2 is complete, retrieval and sanitization are only logically separated. Documentation must not call the current single-job workflow process, container, or microVM isolation.

## Builder Log

Record commits, workflow runs, exact test commands/results, fixture and artifact hashes, permission evidence, rejected samples, residual risks, and follow-ups.

- 2026-07-17 — Claimed P0 on `builder/p0-security-cli-baseline-20260717` from source base `f9b6d696587450c0e279e81c15011a571b61952e`. Corrected deterministic whitespace collapse and the security verifier's one-line dependency parsing; added focused dependency-envelope tests. Candidate implementation/test commit `1c55ee45edbb4fe05c27efcb9c4c6d4e375a9321` passed the security verifier, 11 pytest tests, Python compilation, CLI JSON/PDF integrity replay, workflow YAML/permission inspection, and the hidden-control scan under CPython 3.13.5. Full evidence and hashes are in `reports/p0-security-cli-baseline-20260717.md`.
- 2026-07-17 — Opened PR #2. Security Envelope run `29564325393` checked out the PR merge ref with read-only token permissions but failed at `Install minimal test environment`; all verification steps were skipped. P0 remains `IN PROGRESS` pending diagnosis, a successful submitted-head rerun, and retained logs.
