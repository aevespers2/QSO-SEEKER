# Release Plan

## Current Decision

Status: `BLOCKED — ARCHITECT P0 DISPOSITION, SECURITY ISOLATION, AND CONTRACT EVIDENCE REQUIRED`

QSO-SEEKER has a defined read-only hostile-input boundary and a reproducible P0 candidate. PR #2 at submitted head `de9784e3ffa3cde1d9784c11fba0e6760fe8b071` passed Security Envelope run `29579705145` (#40). The run checked out and asserted the exact submitted head, completed editable installation, passed the capability-envelope verifier, adversarial and deterministic tests, and the hidden-control scan, and retained least-privilege workflow settings. GitHub reports the pull request mergeable, and no unresolved inline review threads are present.

The prior installation defect was reproduced as setuptools flat-layout auto-discovery of `schemas`, `contracts`, and `unicernal_search`. The candidate limits discovery to `unicernal_search*` and adds regression coverage. This resolves the installation and source-identity blocker for the current candidate, but P0 remains `REVIEW` until Architect disposition. Retrieval and sanitization are still only logically separated, the versioned canonical-record and attribution contracts are not accepted, the complete P1-P3 evidence set is absent, the successful workflow retained no release artifacts, and no release is eligible.

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

PR #2 contains bounded candidate repairs for deterministic whitespace collapse, standards-based TOML dependency parsing, setuptools package discovery, exact submitted-head workflow identity, minimum permissions, tests, and evidence reporting. The exact-head P0 replay succeeded, but none of this work is accepted release capability until the Architect approves P0 and the later contract and isolation tasks pass.

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
| P0 tests/CLI/reports | REVIEW | Current head `de9784e3ffa3cde1d9784c11fba0e6760fe8b071` passed run `29579705145`; Architect acceptance or bounded rework remains required. |
| Candidate repairs | REVIEW | Installation, dependency parsing, package discovery, exact-source assertion, verifier, tests, and hidden-control scan pass at the submitted head; release authority is not implied. |
| Head stability | REVIEW | Current exact-head evidence is valid only for `de9784e3ffa3cde1d9784c11fba0e6760fe8b071`; any further head change requires a fresh full replay and renewed disposition. |
| Contract determinism | INCOMPLETE | Schemas and fixtures must reproduce identical transformations, decisions, rejection reasons, provenance, and hashes across supported environments. |
| Security isolation | FAIL | Retrieval and sanitizer must be independently permissioned; sanitizer must have no credentials or network and must verify the artifact digest before processing. |
| Adversarial validation | PARTIAL | P0 adversarial/deterministic tests pass, but the versioned P1/P2 contract and handoff fixture matrix is not complete or accepted. |
| Workflow integrity | REVIEW | Exact submitted-head checkout/assertion, editable install, minimum permissions, tests, and scans pass; later split-job workflow integrity remains unimplemented. |
| Documentation | PARTIAL | P0 setup, root cause, and evidence are recorded; supported contract versions, actual isolation, failure recovery, and consumer guidance remain incomplete. |
| Provenance | PARTIAL | Current head and successful workflow evidence are recorded; the run retained no artifacts, and release checksums, attestations, complete fixture identities, and rollback drill remain absent. |
| Approval | PENDING | Architect P0 disposition followed by explicit release approval after every blocking gate passes. |

## Artifact Requirements

- Versioned canonical-record and attribution-sidecar schemas.
- Positive, negative, adversarial, boundary, dependency-envelope, and digest-mismatch fixtures with expected outputs and hashes.
- Source/package artifact, CLI sample, JSON audit/evidence records, PDF evidence report, and independently permissioned workflow definitions.
- Complete clean-checkout test, security-envelope, hidden-control, workflow-permission, isolation, and documentation reports.
- Successful exact-head workflow logs and retained artifacts; prior failure logs remain part of the provenance record.
- SBOM where applicable, SHA-256 checksums, provenance manifest, attestation, and tested rollback evidence.

## Rollback Criteria

Reject or roll back the candidate if Architect review finds an unbounded P0 scope change; the submitted head changes without a fresh exact-head replay; installation ceases to be reproducible; CI verifies a different state than the reviewed head; fetched material executes; sanitizer credentials or network access are introduced; artifact digests are not verified; accepted/rejected results become nondeterministic; provenance is lost; reports diverge from canonical records; dependencies exceed the approved envelope; hidden controls pass undetected; or documentation overstates isolation. Restore the prior reviewed state and retain rejected artifacts, logs, hashes, and reports for comparison.

## Unresolved Blockers

- Architect must accept, reject, or request bounded rework for P0 at current submitted head `de9784e3ffa3cde1d9784c11fba0e6760fe8b071`.
- P1 versioned canonical-record and attribution-sidecar contracts are incomplete.
- P2 independently permissioned retrieval/sanitizer separation and digest-verified artifact handoff are incomplete.
- P3 complete adversarial conformance fixtures and expected outputs are incomplete.
- Retrieval and sanitization still share a logical/workflow boundary rather than independently permissioned jobs.
- Successful run `29579705145` retained no artifacts; complete release artifact, checksum, attestation, and rollback evidence remains absent.
- Complete contract, isolation, documentation, provenance, and consumer-acceptance evidence remains absent.
- QuantumStateObjects cannot consume an authoritative canonical-record contract until P1-P3 are published and independently accepted.

## Release Log

- 2026-07-16 — Aligned the candidate with the secure read-only retrieval MVP; release remained blocked by isolation and deterministic contract evidence.
- 2026-07-17 — Recorded the initial bounded P0 candidate and preserved failed installation/source-identity evidence from runs `29564325393` and `29564563760`.
- 2026-07-17 — Reconciled the release plan after superseded head `75e9ebd578898bfba47f24d9619535ba025bc921` passed exact-head Security Envelope run `29576874153`.
- 2026-07-17 — Reconciled the current candidate after head `de9784e3ffa3cde1d9784c11fba0e6760fe8b071` passed exact-head Security Envelope run `29579705145`. P0 is reviewable and the pull request is mergeable with no unresolved inline review threads, but release remains blocked by Architect disposition, absent retained artifacts, and incomplete P1-P3 contract, isolation, adversarial, provenance, and rollback gates.