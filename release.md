# Release Plan

## Current Decision

Status: `BLOCKED — CURRENT-HEAD P0 DISPOSITION, SECURITY ISOLATION, AND CONTRACT EVIDENCE REQUIRED`

QSO-SEEKER has a defined read-only hostile-input boundary and a bounded P0 candidate in PR #2. Exact-submitted-head Security Envelope replays have demonstrated reproducible checkout, editable installation, capability-envelope verification, adversarial and deterministic tests, hidden-control scanning, and least-privilege workflow settings. Those results are head-specific provenance only: P0 may move from `REVIEW` to `DONE` only when the then-current PR head has a successful attached full replay and the Architect accepts that exact state.

The prior installation defect was reproduced as setuptools flat-layout auto-discovery of `schemas`, `contracts`, and `unicernal_search`. The candidate limits discovery to `unicernal_search*` and adds regression coverage. This resolves the installation and source-identity defect in the reviewed candidate line, but retrieval and sanitization remain only logically separated, the versioned canonical-record and attribution contracts are not accepted, the complete P1-P3 evidence set is absent, successful workflow runs have retained no release artifacts, and no release is eligible.

## Versioning

- Scheme: Semantic Versioning for the CLI, canonical-record schema, attribution sidecar, and workflow contract.
- First eligible candidate: `0.1.0-alpha.1`.
- Compatible fields and rejection reasons may be minor changes.
- Security-boundary, required-field, transformation, canonicalization, isolation, or hash changes require explicit compatibility review and migration fixtures.
- No tag may be created until one immutable candidate head passes all tests, security, documentation, provenance, artifact, rollback, and approval gates.

## Release Scope

- Reproducible pytest, security-envelope, CLI JSON, PDF report, workflow, exact-source, and hidden-control baseline from a clean checkout.
- Versioned canonical-record and attribution-sidecar schemas with deterministic accepted/rejected fixtures and hashes.
- Separate read-only retrieval and credential-free, network-free sanitizer jobs with artifact-only handoff and digest verification.
- Adversarial fixtures for Unicode concealment, prompt injection, executable/binary types, oversized input, malformed attribution, dependency drift, and digest mismatch.
- Accurate trust-boundary documentation, security reports, checksums, provenance, and rollback.

## Selected Candidate Work

PR #2 contains bounded candidate repairs for deterministic whitespace collapse, standards-based TOML dependency parsing, setuptools package discovery, exact submitted-head workflow identity, minimum permissions, tests, and evidence reporting. Previous exact-head P0 replays succeeded, but none of this work is accepted release capability until the current head passes the same replay, the Architect approves P0, and the later contract and isolation tasks pass.

## Planned Changelog Entries

- `Fixed`: deterministic whitespace collapse, standards-based TOML dependency-envelope parsing, and bounded setuptools package discovery, after independent acceptance.
- `Added`: versioned canonical-record and attribution contracts, deterministic fixtures, and hashes.
- `Security`: credential-free sanitizer job, artifact-only handoff, fail-closed digest verification, least-privilege workflows, hidden-control scan, and adversarial conformance suite.
- `Changed`: exact submitted-head checkout/assertion and documentation describing actual rather than implied isolation.
- `Release`: source/package artifacts, CLI/PDF samples, reports, SBOM where applicable, checksums, provenance, rollback evidence, and approval.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0 is accepted as `DONE`, and P1-P3 are completed with linked commits, commands, workflow runs, and retained artifacts. |
| P0 tests/CLI/reports | REVIEW | The current PR head must have a successful attached full Security Envelope replay before Architect acceptance; prior-head passes are provenance only. |
| Candidate repairs | REVIEW | Installation, dependency parsing, package discovery, exact-source assertion, verifier, tests, and hidden-control scan must pass at the exact accepted head; release authority is not implied. |
| Head stability | REVIEW | Any commit after a successful run resets exact-head acceptance until the complete replay passes again at the new head. |
| Contract determinism | INCOMPLETE | Schemas and fixtures must reproduce identical transformations, decisions, rejection reasons, provenance, and hashes across supported environments. |
| Security isolation | FAIL | Retrieval and sanitizer must be independently permissioned; sanitizer must have no credentials or network and must verify the artifact digest before processing. |
| Adversarial validation | PARTIAL | P0 adversarial/deterministic tests have passed on reviewed heads, but the versioned P1/P2 contract and handoff fixture matrix is not complete or accepted. |
| Workflow integrity | REVIEW | Exact submitted-head checkout/assertion, editable install, minimum permissions, tests, and scans must pass on the accepted head; later split-job workflow integrity remains unimplemented. |
| Documentation | PARTIAL | P0 setup and root cause are recorded; supported contract versions, actual isolation, failure recovery, and consumer guidance remain incomplete. |
| Provenance | PARTIAL | Prior successful exact-head workflow evidence is recorded; runs retained no release artifacts, and release checksums, attestations, complete fixture identities, and rollback drill remain absent. |
| Approval | PENDING | Architect P0 disposition followed by explicit release approval after every blocking gate passes. |

## Artifact Requirements

- Versioned canonical-record and attribution-sidecar schemas.
- Positive, negative, adversarial, boundary, dependency-envelope, and digest-mismatch fixtures with expected outputs and hashes.
- Source/package artifact, CLI sample, JSON audit/evidence records, PDF evidence report, and independently permissioned workflow definitions.
- Complete clean-checkout test, security-envelope, hidden-control, workflow-permission, isolation, and documentation reports.
- Successful exact-head workflow logs and retained artifacts; prior failure and superseded-head logs remain part of the provenance record.
- SBOM where applicable, SHA-256 checksums, provenance manifest, attestation, and tested rollback evidence.

## Rollback Criteria

Reject or roll back the candidate if Architect review finds an unbounded P0 scope change; the submitted head changes without a fresh exact-head replay; installation ceases to be reproducible; CI verifies a different state than the reviewed head; fetched material executes; sanitizer credentials or network access are introduced; artifact digests are not verified; accepted/rejected results become nondeterministic; provenance is lost; reports diverge from canonical records; dependencies exceed the approved envelope; hidden controls pass undetected; or documentation overstates isolation. Restore the prior reviewed state and retain rejected artifacts, logs, hashes, and reports for comparison.

## Unresolved Blockers

- The then-current PR #2 head must pass the complete attached Security Envelope replay before Architect disposition; prior-head passes cannot authorize a changed head.
- Architect must accept, reject, or request bounded rework for the exact replayed P0 state.
- P1 versioned canonical-record and attribution-sidecar contracts are incomplete.
- P2 independently permissioned retrieval/sanitizer separation and digest-verified artifact handoff are incomplete.
- P3 complete adversarial conformance fixtures and expected outputs are incomplete.
- Retrieval and sanitization still share a logical/workflow boundary rather than independently permissioned jobs.
- Successful runs have retained no release artifacts; complete release artifact, checksum, attestation, and rollback evidence remains absent.
- Complete contract, isolation, documentation, provenance, and consumer-acceptance evidence remains absent.
- QuantumStateObjects cannot consume an authoritative canonical-record contract until P1-P3 are published and independently accepted.

## Release Log

- 2026-07-16 — Aligned the candidate with the secure read-only retrieval MVP; release remained blocked by isolation and deterministic contract evidence.
- 2026-07-17 — Recorded the initial bounded P0 candidate and preserved failed installation/source-identity evidence from runs `29564325393` and `29564563760`.
- 2026-07-17 — Recorded successful exact-submitted-head P0 replays, including runs `29576874153` and `29579705145`, as provenance for the bounded candidate line.
- 2026-07-17 — Made acceptance head-stable: any subsequent commit must complete a fresh exact-head replay before Architect disposition. Release remains blocked by P0 approval, absent retained artifacts, and incomplete P1-P3 contract, isolation, adversarial, provenance, and rollback gates.