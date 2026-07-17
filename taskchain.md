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
| P0 | Establish a reproducible security and CLI baseline | QSOBuilder | — | REVIEW | Security-envelope verification, editable installation, pytest, CLI JSON/PDF evidence, hidden-control scanning, minimum permissions, and exact submitted-head identity pass at one immutable candidate; Architect disposition remains. |
| P1 | Version the canonical record and attribution-sidecar contract | QSOBuilder | P0 | PROPOSED | Schemas and fixtures define fields, transformations, limits, rejection reasons, provenance, hashes, and independent consumer validation. |
| P2 | Split retrieval and sanitizer into independently permissioned jobs | QSOBuilder | P0 | PROPOSED | Fetch is read-only; sanitizer receives a verified inert artifact, has no network/repository credential, and fails closed on missing or changed digest. |
| P3 | Publish adversarial conformance fixtures | Builder | P1 and P2 | PROPOSED | Hostile and malformed inputs produce deterministic accepted/rejected outputs without execution or provenance loss. |

## P0 baseline candidate — PR #2

**Status:** `REVIEW — EXACT-HEAD CI PASSED; ARCHITECT DISPOSITION PENDING`

PR #2 is the single bounded P0 candidate. The editable-install failure was reproduced as setuptools flat-layout auto-discovery of `schemas`, `contracts`, and `unicernal_search`; package discovery is now limited to `unicernal_search*`, with a focused regression test excluding non-package repository areas. The workflow checks out `github.event.pull_request.head.sha`, asserts the actual checkout equals that submitted head, keeps `persist-credentials: false`, and runs the existing installation and verification sequence with repository permission limited to `contents: read`.

Security Envelope run `29576736138` passed at submitted remediation/merge head `e5439b0d86abb8b80b31cc14ea8421a11a44bf5b`. Checkout, exact-source assertion, Python setup, editable installation, capability-envelope verification, all adversarial/deterministic tests, and the hidden-control scan completed successfully. GitHub reports PR #2 mergeable after current `main` was reconciled through merge commit `e5439b0d86abb8b80b31cc14ea8421a11a44bf5b` without force-rewriting reviewed history.

**Directive:** keep P1/P2 unaccepted until the Architect dispositions P0 and confirms the final documentation-only head retains an attached pass. Product scope and portfolio priority are unchanged.

## Architectural boundary

Until P2 is complete, retrieval and sanitization are only logically separated. Documentation must not call the current single-job workflow process, container, or microVM isolation.

## Builder Log

Record commits, workflow runs, exact test commands/results, fixture and artifact hashes, permission evidence, rejected samples, residual risks, and follow-ups.

- 2026-07-17 — Reviewed PR #2 at head `9e2d83e4156b77e177a4e478de3d46271174f77a`. Local candidate checks and recorded artifact hashes narrowed P0, but the initial Security Envelope run failed during environment installation before the verifier or tests executed.
- 2026-07-17 — Confirmed current-head-associated run `29564563760` also failed during environment installation after checking out PR merge ref `58084e0978bb30970a6cd2e919c96819622ecdf8`. All substantive checks were skipped and no exact submitted-head acceptance existed.
- 2026-07-17 — Reproduced the editable-install failure as setuptools flat-layout auto-discovery of `schemas`, `contracts`, and `unicernal_search`. Commit `cfb7a22480b60ba6198a4f7d622c002378e1c061` scopes package discovery to `unicernal_search*` and adds `tests/test_packaging_config.py`; the bounded reproducer changed from deterministic failure to a successful editable build/install.
- 2026-07-17 — Commit `c7176bb274f7840926738cc3200931cf8eea91d9` configures the Security Envelope workflow to check out and assert the exact submitted pull-request head before installation.
- 2026-07-17 — Merge commit `e5439b0d86abb8b80b31cc14ea8421a11a44bf5b` reconciled current `main` into PR #2 without rewriting reviewed history and restored mergeability.
- 2026-07-17 — Security Envelope run `29576736138` passed at exact submitted head `e5439b0d86abb8b80b31cc14ea8421a11a44bf5b`; every substantive workflow step passed. P0 moved to `REVIEW` for Architect disposition.