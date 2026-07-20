# Changelog

All notable product, architecture, implementation, documentation, evidence, release, and deployment changes are recorded here.

## Unreleased

### Product

- 2026-07-16 — Defined the MVP as a read-only, fail-closed conversion of hostile public input into deterministic inert records and audit evidence.
- 2026-07-16 — Prioritized credential-free sanitizer separation and adversarial conformance before broader retrieval coverage or QSO runtime integration.
- 2026-07-17 — Advanced the historical P0 security/CLI candidate to Architect review after exact-head checks passed; retained final-release evidence remained incomplete.
- 2026-07-17 — Classified broader collection, private overlays, scheduling, and shared-field publication as separate later work.
- 2026-07-18 — Accepted canonical-record and attribution-sidecar contract version 1 through merged PR #10.
- 2026-07-19 — Reframed the next objective around current-main replay, independent retrieval/sanitizer handoff, adversarial conformance, and documentation acceptance.

### Architecture

- The security boundary requires artifact-only handoff with an independently verified digest; logical separation alone is not documented as enforced process isolation.
- 2026-07-17 — Exact submitted-head identity and minimum workflow permissions became explicit evidence requirements.
- 2026-07-18 — Contract v1 established exact canonical JSON, field sets, content/source/record/sidecar hash semantics, path and URL rules, and fail-closed consumer validation.
- 2026-07-18 — Repository-wide consent-capacity policy and CI enforcement were added.
- 2026-07-19 — Documented the system context, component model, record lifecycle, trust boundaries, failure behavior, target job separation, and extension rules without changing implementation scope.
- 2026-07-20 — Reconciled the documentation candidate with the merged repository-wide consent-lock repair and retained the distinction between accepted controls and still-proposed runtime isolation.

### Implementation

- Existing local CLI, schema, gateway, report, contract, test, and verification surfaces remain bounded repository assets.
- 2026-07-17 — Candidate repairs addressed Unicode whitespace canonicalization, standards-based dependency parsing, bounded package discovery, and exact submitted-head workflow identity.
- 2026-07-18 — Added canonical-record and attribution-sidecar v1 builders, validators, canonical JSON helpers, SHA-256 helpers, and deterministic mutation tests through PR #10.
- 2026-07-19 — No runtime, schema, dependency, permission, retrieval, consumer, or publisher behavior was changed by the Pages documentation milestone.
- 2026-07-20 — Documentation-branch reconciliation carried the accepted consent validator, regression tests, and pinned exact-head workflow from current `main`; no new implementation capability was introduced.

### Documentation

- 2026-07-19 — Added a GitHub Pages-ready MkDocs site with a landing page and navigation.
- 2026-07-19 — Added project overview, architecture, canonical-contract design, API/CLI reference, security model, developer onboarding, operations/recovery, and governance guides.
- 2026-07-19 — Added static architecture and record-lifecycle diagrams with accessible titles and descriptions.
- 2026-07-19 — Expanded the README and reconciled `taskchain.md` and `release.md` with merged contract v1, open draft candidates, and the still-blocked release posture.
- 2026-07-20 — Updated task, release, and change records after PR #11 merged so Pages no longer describes the consent repair as pending.

### Evidence

- 2026-07-17 — Historical P0 candidates recorded clean installation, dependency verification, tests, hidden-control checks, and exact-source workflow results on specific submitted heads.
- 2026-07-18 — PR #10 exact-head verification completed before canonical contract v1 was merged.
- 2026-07-20 — PR #11 exact-head consent-lock evidence was accepted on `main`; strict MkDocs, consent-lock, and Security Envelope evidence must be regenerated for the reconciled documentation head.

### Security

- Untrusted content remains inert data and must never be imported, evaluated, compiled, executed, or treated as authority.
- 2026-07-19 — Documented threat classes, schema and rejection controls, bounded neutralization, classification limits, content-addressed validation, consent-capacity policy, residual risk, consumer duties, and security-review checks.
- 2026-07-20 — Recorded the merged repository-wide consent validator, duplicate-key and bypass rejection, immutable lock semantics, pinned Actions, least privilege, and exact-head evidence as accepted controls.

### Release

- Release remains blocked until current-main P0 acceptance, P2 independent permission separation, P3 conformance, retained artifacts, strict documentation validation, provenance, rollback, legal/privacy review, and explicit human approval are complete.
- 2026-07-18 — Contract v1 acceptance did not authorize live retrieval, scheduling, credentials, runtime use, publication, or autonomous learning.
- 2026-07-19 — The documentation foundation remains a review candidate and does not mark any blocking release gate as passed without evidence.
- 2026-07-20 — Consent-capacity control moved from repair review to accepted current-main status; this does not unblock release without final composition replay.

### Deployment

- No production service, authenticated retrieval, private-source access, source-content execution, scheduled collection, runtime handoff, or shared-field publication is authorized.
- 2026-07-19 — Added bounded local run, health, observability, failure, rollback, incident-response, retention, and publication-gate procedures.

## Entry format

- Date
- Category: Product / Architecture / Implementation / Documentation / Evidence / Security / Release / Deployment
- Summary
- Evidence: issue, pull request, commit, workflow, artifact, or deployment record
- Impact and migration notes where applicable
