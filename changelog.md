# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product
- 2026-07-16 — Defined the MVP as a read-only, fail-closed conversion of hostile public input into deterministic inert canonical records and attribution sidecars.
- 2026-07-16 — Prioritized credential-free sanitizer separation and adversarial conformance before broader retrieval coverage or QSO runtime integration.
- 2026-07-17 — Advanced the existing P0 security/CLI baseline from `READY` to `IN PROGRESS` after PR #2 submitted bounded candidate repairs and evidence; portfolio priority and MVP scope are unchanged.
- 2026-07-17 — Retained the same P0 objective after current-head-associated CI repeated the installation failure and exposed that the workflow verifies a pull-request merge ref rather than the exact submitted head.

### Architecture
- The security boundary requires artifact-only handoff with verified digest; the current single-job workflow remains logical separation only.
- 2026-07-17 — Exact source identity is now an explicit P0 gate: CI must check out and assert the submitted head rather than relying on a synthetic pull-request merge ref.

### Implementation
- Existing code, tests, CLI, report, and workflow surfaces remain candidate assets pending current reproducible evidence.
- 2026-07-17 — PR #2 candidate repairs deterministic whitespace canonicalization and dependency-envelope parsing with standard-library `tomllib`, and adds focused dependency tests. These are implemented candidate changes, not accepted release capability.

### Evidence
- 2026-07-17 — Candidate implementation/test commit `1c55ee45edbb4fe05c27efcb9c4c6d4e375a9321` records passing local security-envelope verification, 11 pytest tests, Python compilation, CLI JSON/PDF integrity replay, workflow YAML/read-only permission inspection, hidden-control scanning, and artifact hashes.
- 2026-07-17 — Initial Security Envelope run `29564325393` failed at `Install minimal test environment`; all later verification steps were skipped. The local Contents-API replay does not replace a successful submitted-head or independently reviewed clean-checkout run.
- 2026-07-17 — Current-head-associated run `29564563760` also failed at environment installation after checking out PR merge ref `58084e0978bb30970a6cd2e919c96819622ecdf8`; substantive verification was skipped, no successful artifact bundle was retained, and GitHub reports PR #2 non-mergeable.

### Release
- The candidate remains blocked until baseline checks, versioned contracts, job separation, adversarial fixtures, documentation, checksums, and provenance pass.
- 2026-07-17 — PR #2 is not release-acceptable: the installation failure remains unresolved, the current workflow does not establish exact submitted-head identity, and no independent clean-checkout replay exists. The next work is a bounded install/checkout repair and complete retained replay, not P1/P2 expansion.

### Deployment
- No authenticated retrieval, private-source access, or executable-content processing is authorized.

## Entry Format
- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable
