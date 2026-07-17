# Release Plan

## Current Decision

Status: `BLOCKED — ARCHITECT P0 DISPOSITION, LIVE REVIEW RECONCILIATION, SECURITY ISOLATION, AND CONTRACT EVIDENCE REQUIRED`

QSO-SEEKER has a defined read-only hostile-input boundary and a reproducible P0 candidate. PR #2 at submitted head `de9784e3ffa3cde1d9784c11fba0e6760fe8b071` passed Security Envelope run `29579705145` (#40). The run checked out and asserted the exact submitted head, completed editable installation, passed the capability-envelope verifier, adversarial and deterministic tests, and the hidden-control scan, and retained least-privilege workflow settings.

The live pull-request state does not yet support acceptance: GitHub currently reports PR #2 open and non-mergeable, and one unresolved inline review thread states that the primary P0 baseline report and dependent records still identify superseded heads/runs rather than one final exact-head evidence spine. The successful run retained no workflow artifacts. P0 therefore remains `REVIEW` pending evidence reconciliation and Architect disposition. Retrieval and sanitization are still only logically separated, the versioned canonical-record and attribution contracts are not accepted, the complete P1-P3 evidence set is absent, and no release is eligible.

## Versioning

- Scheme: Semantic Versioning for the CLI, canonical-record schema, attribution sidecar, and workflow contract.
- First eligible candidate: `0.1.0-alpha.1`.
- Compatible fields and rejection reasons may be minor changes.
- Security-boundary, required-field, transformation, canonicalization, isolation, or hash changes require explicit compatibility review and migration fixtures.
- No tag may be created until one immutable candidate head passes all tests, security, documentation, provenance, artifact, rollback, deployment-preparation, and approval gates.

## Release Scope

- Reproducible pytest, security-envelope, CLI JSON, PDF report, workflow, exact-source, and hidden-control baseline from a clean checkout.
- Versioned canonical-record and attribution-sidecar schemas with deterministic accepted/rejected fixtures and hashes.
- Separate read-only retrieval and credential-free, network-free sanitizer jobs with artifact-only handoff and digest verification.
- Adversarial fixtures for Unicode concealment, prompt injection, executable/binary types, oversized input, malformed attribution, dependency drift, and digest mismatch.
- Accurate trust-boundary documentation, security reports, checksums, provenance, deployment preparation, and rollback.

## Selected Candidate Work

PR #2 contains bounded candidate repairs for deterministic whitespace collapse, standards-based TOML dependency parsing, setuptools package discovery, exact submitted-head workflow identity, minimum permissions, tests, and evidence reporting. The exact-head P0 workflow succeeded, but none of this work is accepted release capability until the evidence records are synchronized, the live pull request is mergeable with material threads resolved, the Architect approves P0, and the later contract and isolation tasks pass.

## Planned Changelog Entries

- `Fixed`: deterministic whitespace collapse, standards-based TOML dependency-envelope parsing, and bounded setuptools package discovery, after independent acceptance.
- `Added`: versioned canonical-record and attribution contracts, deterministic fixtures, and hashes.
- `Security`: credential-free sanitizer job, artifact-only handoff, fail-closed digest verification, least-privilege workflows, hidden-control scan, and adversarial conformance suite.
- `Changed`: exact submitted-head checkout/assertion and documentation describing actual rather than implied isolation.
- `Release`: source/package artifacts, CLI/PDF samples, reports, SBOM where applicable, checksums, provenance, rollback evidence, deployment record, and approval.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0 is accepted as `DONE`, and P1-P3 are completed with linked commits, commands, workflow runs, and retained artifacts. |
| P0 tests/CLI/reports | REVIEW | Head `de9784e3ffa3cde1d9784c11fba0e6760fe8b071` passed run `29579705145`, but the primary baseline report and dependent records must identify this same immutable evidence spine before Architect disposition. |
| Candidate repairs | REVIEW | Installation, dependency parsing, package discovery, exact-source assertion, verifier, tests, and hidden-control scan pass at the submitted head; release authority is not implied. |
| Head/review stability | FAIL | The live PR is non-mergeable and one exact-head provenance thread is unresolved. Restore one mergeable immutable head, resolve or disposition the thread, and rerun after any change. |
| Contract determinism | INCOMPLETE | Schemas and fixtures must reproduce identical transformations, decisions, rejection reasons, provenance, and hashes across supported environments. |
| Security isolation | FAIL | Retrieval and sanitizer must be independently permissioned; sanitizer must have no credentials or network and must verify the artifact digest before processing. |
| Adversarial validation | PARTIAL | P0 adversarial/deterministic tests pass, but the versioned P1/P2 contract and handoff fixture matrix is not complete or accepted. |
| Workflow integrity | REVIEW | Exact submitted-head checkout/assertion, editable install, minimum permissions, tests, and scans pass; later split-job workflow integrity remains unimplemented. |
| Documentation | FAIL | P0 setup and root cause are recorded, but exact-head evidence records are inconsistent and supported contract versions, actual isolation, failure recovery, and consumer guidance remain incomplete. |
| Provenance | FAIL | Current head and workflow success are observable, but the primary report is stale, the run retained no artifacts, and release checksums, attestations, complete fixture identities, and rollback drill are absent. |
| Deployment | BLOCKED | `deploy.md` records the fail-closed review. No deployment target, release artifact, production permission, package publication, integration, or downstream pin is authorized. |
| Approval | PENDING | Architect P0 disposition followed by explicit release approval after every blocking gate passes. |

## Artifact Requirements

- Versioned canonical-record and attribution-sidecar schemas.
- Positive, negative, adversarial, boundary, dependency-envelope, and digest-mismatch fixtures with expected outputs and hashes.
- Source/package artifact, CLI sample, JSON audit/evidence records, PDF evidence report, and independently permissioned workflow definitions.
- Complete clean-checkout test, security-envelope, hidden-control, workflow-permission, isolation, documentation, and deployment-preparation reports.
- Successful exact-head workflow logs and retained artifacts tied to the same head recorded in every acceptance document; prior failure and superseded-run logs remain part of the provenance record.
- SBOM where applicable, SHA-256 checksums, provenance manifest, attestation, and tested rollback evidence.

## Rollback Criteria

Reject or roll back the candidate if Architect review finds an unbounded P0 scope change; the submitted head changes without a fresh exact-head replay; the reviewed, reported, and tested heads differ; the pull request remains non-mergeable; material review threads remain unresolved; installation ceases to be reproducible; fetched material executes; sanitizer credentials or network access are introduced; artifact digests are not verified; accepted/rejected results become nondeterministic; provenance is lost; reports diverge from canonical records; dependencies exceed the approved envelope; hidden controls pass undetected; or documentation overstates isolation. Restore the prior reviewed state and retain rejected artifacts, logs, hashes, reports, and review dispositions for comparison.

## Unresolved Blockers

- Architect must accept, reject, or request bounded rework for P0 at submitted head `de9784e3ffa3cde1d9784c11fba0e6760fe8b071` only after evidence reconciliation.
- The live PR is non-mergeable despite candidate text stating otherwise.
- One unresolved review thread requires the baseline report and dependent records to use one final exact-head run consistently.
- Successful run `29579705145` retained no artifacts.
- P1 versioned canonical-record and attribution-sidecar contracts are incomplete.
- P2 independently permissioned retrieval/sanitizer separation and digest-verified artifact handoff are incomplete.
- P3 complete adversarial conformance fixtures and expected outputs are incomplete.
- Retrieval and sanitization still share a logical/workflow boundary rather than independently permissioned jobs.
- Complete release artifact, checksum, attestation, rollback, deployment-target, and consumer-acceptance evidence remains absent.
- QuantumStateObjects cannot consume an authoritative canonical-record contract until P1-P3 are published and independently accepted.

## Release Log

- 2026-07-16 — Aligned the candidate with the secure read-only retrieval MVP; release remained blocked by isolation and deterministic contract evidence.
- 2026-07-17 — Recorded the initial bounded P0 candidate and preserved failed installation/source-identity evidence from runs `29564325393` and `29564563760`.
- 2026-07-17 — Recorded superseded exact-head success at head `75e9ebd578898bfba47f24d9619535ba025bc921` in run `29576874153`.
- 2026-07-17 — Current head `de9784e3ffa3cde1d9784c11fba0e6760fe8b071` passed exact-head Security Envelope run `29579705145`, but live review found the PR non-mergeable, one unresolved stale-provenance thread, and no retained artifacts. Added `deploy.md`; no deployment, publication, tag, integration, or downstream pin was attempted.
