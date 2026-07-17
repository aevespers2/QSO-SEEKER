# Changelog

All notable product, architecture, implementation, release, and deployment changes are recorded here.

## Unreleased

### Product
- 2026-07-16 — Defined the MVP as a read-only, fail-closed conversion of hostile public input into deterministic inert canonical records and attribution sidecars.
- 2026-07-16 — Prioritized credential-free sanitizer separation and adversarial conformance before broader retrieval coverage or QSO runtime integration.
- 2026-07-17 — Advanced the existing P0 security/CLI baseline from `READY` to `IN PROGRESS` after PR #2 submitted bounded candidate repairs and evidence; portfolio priority and MVP scope were unchanged.
- 2026-07-17 — Retained the same P0 objective after current-head-associated CI repeated the installation failure and exposed that the workflow verified a pull-request merge ref rather than the exact submitted head.
- 2026-07-17 — Advanced P0 from `IN PROGRESS` to `REVIEW` after the final submitted head passed the complete exact-source workflow. Architect disposition is now required; product scope and portfolio priority remain unchanged.
- 2026-07-17 — Preserved PR #2 as the sole P0 acceptance path after PR #3 opened with a superseded deployment narrative. PR #3 is a documentation record to reconcile or close after P0 disposition, not a competing implementation or release candidate.

### Architecture
- The security boundary requires artifact-only handoff with verified digest; the current single-job workflow remains logical separation only.
- 2026-07-17 — Exact source identity became an explicit P0 gate: CI must check out and assert the submitted head rather than relying on a synthetic pull-request merge ref.
- 2026-07-17 — The candidate workflow now checks out and asserts the exact pull-request head, retains `contents: read`, and disables checkout credential persistence. This establishes candidate source identity and least-privilege workflow evidence, not P2 retrieval/sanitizer isolation.
- 2026-07-17 — Required deployment and release records to follow the immutable P0 candidate rather than become a parallel branch of product truth. Any PR #3 reconciliation must use the accepted head, run, artifacts, limitations, and rollback disposition.

### Implementation
- Existing code, tests, CLI, report, and workflow surfaces remain candidate assets pending Architect acceptance and later contract/isolation gates.
- 2026-07-17 — PR #2 candidate repairs deterministic whitespace canonicalization and dependency-envelope parsing with standard-library `tomllib`, and adds focused dependency tests. These are implemented candidate changes, not accepted release capability.
- 2026-07-17 — The editable-install failure was reproduced as setuptools flat-layout auto-discovery of `schemas`, `contracts`, and `unicernal_search`; package discovery is now limited to `unicernal_search*` with a regression test.
- 2026-07-17 — PR #3 adds deployment and release documentation only. It does not add retrieval, sanitizer isolation, credentials, networking, publication, deployment, or downstream authority.

### Evidence
- 2026-07-17 — Candidate implementation/test commit `1c55ee45edbb4fe05c27efcb9c4c6d4e375a9321` recorded passing local security-envelope verification, 11 pytest tests, Python compilation, CLI JSON/PDF integrity replay, workflow YAML/read-only permission inspection, hidden-control scanning, and artifact hashes.
- 2026-07-17 — Initial Security Envelope run `29564325393` failed at `Install minimal test environment`; all later verification steps were skipped. The local Contents-API replay did not replace a successful submitted-head or independently reviewed clean-checkout run.
- 2026-07-17 — Run `29564563760` also failed at environment installation after checking out PR merge ref `58084e0978bb30970a6cd2e919c96819622ecdf8`; substantive verification was skipped, no successful artifact bundle was retained, and the PR was then non-mergeable.
- 2026-07-17 — Final submitted head `75e9ebd578898bfba47f24d9619535ba025bc921` passed Security Envelope run `29576874153` (#33), including exact-source assertion, editable installation, capability-envelope verification, adversarial/deterministic tests, and hidden-control scanning. GitHub reports PR #2 mergeable.
- 2026-07-17 — Current PR #2 head `306dfa4104c12594b23dda8111e1c80edb0be397` passed Security Envelope run `29580240905`; checkout, exact-source assertion, installation, capability-envelope verification, adversarial/deterministic tests, and hidden-control scanning passed. GitHub reports the PR mergeable with no unresolved inline review threads, but the run retained no artifacts.
- 2026-07-17 — At review start, PR #3 head `ab7f25e8461a278985c81d7e62092e443eb9a281` was non-mergeable and its narrative referenced superseded PR #2 state. The evidence-record correction supersedes that PR #3 head and requires a new exact-head replay if the branch remains open for merge.

### Release
- The candidate remains blocked from release until the Architect accepts P0 and the versioned contracts, independently permissioned job separation, adversarial conformance, documentation, checksums, provenance, and rollback gates pass.
- 2026-07-17 — The installation and exact-source blockers are resolved at the candidate level. PR #2 is reviewable but not yet accepted, published, deployed, or authoritative for downstream consumers; P1, P2, and P3 remain incomplete.
- 2026-07-17 — Missing retained workflow artifacts remain an explicit release-evidence gap. PR #3 cannot resolve that gap by restating an older run or candidate head.

### Deployment
- No authenticated retrieval, private-source access, executable-content processing, or sanitizer network/credential authority is authorized.
- 2026-07-17 — No deployment was attempted through PR #3. Keep all deployment, publication, tagging, integration, and downstream pinning fail-closed until PR #2 is dispositioned and the later contract, isolation, provenance, and rollback gates pass.
- 2026-07-17 — PR #3 must not merge ahead of PR #2. After P0 disposition, it should be closed/superseded or reconciled as a documentation-only record against one accepted immutable candidate.

## Entry Format
- Date
- Category: Product / Architecture / Added / Changed / Fixed / Security / Release / Deployment
- Summary
- Evidence: issue, PR, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable