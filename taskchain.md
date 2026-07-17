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

**Status:** `REVIEW — CURRENT EXACT-HEAD CI PASSED; ARCHITECT DISPOSITION AND RETAINED EVIDENCE PENDING`

PR #2 remains the single bounded P0 candidate. Its current submitted head is `306dfa4104c12594b23dda8111e1c80edb0be397`. Security Envelope run `29580240905` passed checkout, exact-source assertion, Python setup, editable installation, capability-envelope verification, adversarial/deterministic tests, and the hidden-control scan. GitHub reports PR #2 mergeable, and no unresolved inline review threads remain.

The run retained no workflow artifacts. This does not invalidate the configured checks, but it leaves the release, provenance, and independent-review record incomplete. P0 remains `REVIEW`, not `DONE`; P1-P3 are not accepted, retrieval and sanitization remain logically rather than independently isolated, and downstream consumers must not pin or claim authority from the candidate before Architect disposition and retained non-secret evidence are complete.

**Directive:** preserve PR #2 as the sole P0 candidate; do not add unrelated changes; obtain Architect acceptance or rejection against the current immutable head; retain hashed non-secret logs/reports or explicitly disposition the artifact-retention gap; and require a fresh exact-head replay after any subsequent commit. Product scope and portfolio priority are unchanged.

## Deployment-record scope gate — PR #3

**Status:** `REVIEW — STALE, NON-MERGEABLE DOCUMENTATION BRANCH; NOT A COMPETING P0 PATH`

PR #3 was opened to record deployment and release blockers, but its submitted narrative references superseded PR #2 head `de9784e3ffa3cde1d9784c11fba0e6760fe8b071`, a former non-mergeable state, and a formerly unresolved review thread. At review start, GitHub reported PR #3 itself non-mergeable at head `ab7f25e8461a278985c81d7e62092e443eb9a281`, while PR #2 had advanced to the mergeable exact-head-passing state recorded above. No deployment was attempted, and no separate implementation, release, or authority path is accepted through PR #3.

**Directive:** do not merge PR #3 ahead of PR #2 or treat its stale deployment record as current release evidence. Keep PR #2 the sole P0 acceptance path. After Architect disposition of PR #2, either close/supersede PR #3 or reconcile it as a documentation-only record against the accepted immutable head, current run, retained artifacts, release gates, and rollback decision. Because this evidence correction changes PR #3's submitted head, any earlier status on that branch is superseded and a fresh exact-head replay is required if the branch remains a merge candidate.

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
- 2026-07-17 — Current PR #2 head `306dfa4104c12594b23dda8111e1c80edb0be397` passed Security Envelope run `29580240905`, remains mergeable, and has no unresolved inline review threads. No workflow artifacts were retained, so P0 remains `REVIEW` pending Architect disposition and evidence-retention treatment.
- 2026-07-17 — Classified PR #3 as a stale, non-mergeable deployment-record branch rather than a competing P0 candidate. It must be closed/superseded or reconciled only after PR #2 disposition; no priority or product scope changed.