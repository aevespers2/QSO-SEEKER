# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product
- 2026-07-16 — Defined the MVP as a read-only, fail-closed conversion of hostile public input into deterministic inert canonical records and attribution sidecars.
- 2026-07-16 — Prioritized credential-free sanitizer separation and adversarial conformance before broader retrieval coverage or QSO runtime integration.
- 2026-07-17 — Advanced the existing P0 security/CLI baseline from `READY` to `IN PROGRESS` after PR #2 submitted bounded candidate repairs and evidence; portfolio priority and MVP scope were unchanged.
- 2026-07-17 — Retained the same P0 objective after current-head-associated CI repeated the installation failure and exposed that the workflow verified a pull-request merge ref rather than the exact submitted head.
- 2026-07-17 — Advanced P0 from `IN PROGRESS` to `REVIEW` after the final submitted head passed the complete exact-source workflow. Architect disposition is now required; product scope and portfolio priority remain unchanged.

### Architecture
- The security boundary requires artifact-only handoff with verified digest; the current single-job workflow remains logical separation only.
- 2026-07-17 — Exact source identity became an explicit P0 gate: CI must check out and assert the submitted head rather than relying on a synthetic pull-request merge ref.
- 2026-07-17 — The candidate workflow now checks out and asserts the exact pull-request head, retains `contents: read`, and disables checkout credential persistence. This establishes candidate source identity and least-privilege workflow evidence, not P2 retrieval/sanitizer isolation.

### Implementation
- Existing code, tests, CLI, report, and workflow surfaces remain candidate assets pending Architect acceptance and later contract/isolation gates.
- 2026-07-17 — PR #2 candidate repairs deterministic whitespace canonicalization and dependency-envelope parsing with standard-library `tomllib`, and adds focused dependency tests. These are implemented candidate changes, not accepted release capability.
- 2026-07-17 — The editable-install failure was reproduced as setuptools flat-layout auto-discovery of `schemas`, `contracts`, and `unicernal_search`; package discovery is now limited to `unicernal_search*` with a regression test.

### Evidence
- 2026-07-17 — Candidate implementation/test commit `1c55ee45edbb4fe05c27efcb9c4c6d4e375a9321` recorded passing local security-envelope verification, 11 pytest tests, Python compilation, CLI JSON/PDF integrity replay, workflow YAML/read-only permission inspection, hidden-control scanning, and artifact hashes.
- 2026-07-17 — Initial Security Envelope run `29564325393` failed at `Install minimal test environment`; all later verification steps were skipped. The local Contents-API replay did not replace a successful submitted-head or independently reviewed clean-checkout run.
- 2026-07-17 — Run `29564563760` also failed at environment installation after checking out PR merge ref `58084e0978bb30970a6cd2e919c96819622ecdf8`; substantive verification was skipped, no successful artifact bundle was retained, and the PR was then non-mergeable.
- 2026-07-17 — Final submitted head `75e9ebd578898bfba47f24d9619535ba025bc921` passed Security Envelope run `29576874153` (#33), including exact-source assertion, editable installation, capability-envelope verification, adversarial/deterministic tests, and hidden-control scanning. GitHub reported PR #2 mergeable at that reviewed head.

### Release
- The candidate remains blocked from release until the Architect accepts P0 and the versioned contracts, independently permissioned job separation, adversarial conformance, documentation, checksums, provenance, and rollback gates pass.
- 2026-07-17 — The installation and exact-source blockers are resolved at the candidate level. PR #2 is reviewable but not yet accepted, published, deployed, or authoritative for downstream consumers; P1, P2, and P3 remain incomplete.

### Deployment
- No authenticated retrieval, private-source access, executable-content processing, or sanitizer network/credential authority is authorized.

## Entry Format
- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable