# Release Plan

## Current Decision

Status: `BLOCKED — CI INSTALLATION, SECURITY ISOLATION, AND CONTRACT EVIDENCE REQUIRED`

QSO-SEEKER has a defined read-only hostile-input boundary and an active bounded P0 candidate, but no retrieval/sanitization release is eligible. PR #2 at head `9e2d83e4156b77e177a4e478de3d46271174f77a` records local candidate evidence for deterministic whitespace canonicalization, safer TOML dependency parsing, the security-envelope verifier, 11 pytest tests, Python compilation, CLI JSON/audit/evidence/PDF replay, workflow YAML and permission inspection, hidden-control scanning, and candidate artifact hashes.

That work is not accepted release evidence. Security Envelope run `29564563760`, associated with the current PR head, checked out the pull-request merge ref and failed at `Install minimal test environment`; the capability verifier, adversarial/deterministic tests, and hidden-control scan were skipped, and the run retained no artifacts. GitHub currently reports PR #2 non-mergeable. P0 remains `IN PROGRESS`, every contract/isolation follow-on remains incomplete, and no exact submitted-head or independently reviewed clean-checkout replay has succeeded.

## Versioning

- Scheme: Semantic Versioning for the CLI, canonical-record schema, attribution sidecar, and workflow contract.
- First eligible candidate: `0.1.0-alpha.1`.
- Compatible fields/rejection reasons may be minor changes.
- Security-boundary, required-field, transformation, canonicalization, isolation, or hash changes require explicit compatibility review and migration fixtures.
- No tag may be created until one immutable candidate head passes all tests, security, documentation, provenance, artifact, and rollback gates.

## Release Scope

- Reproducible pytest, security-envelope, CLI JSON, PDF report, workflow, and hidden-control baseline from a clean checkout.
- Versioned canonical-record and attribution-sidecar schemas with deterministic accepted/rejected fixtures and hashes.
- Separate read-only retrieval and credential-free, network-free sanitizer jobs with artifact-only handoff and digest verification.
- Adversarial fixtures for Unicode concealment, prompt injection, executable/binary types, oversized input, malformed attribution, dependency drift, and digest mismatch.
- Accurate trust-boundary documentation, security reports, checksums, provenance, and rollback.

## Selected Completed Work

None accepted for release. PR #2 contains bounded candidate repairs and a detailed local evidence report, but the submitted workflow path fails before verification, uses the pull-request merge ref rather than proving the exact submitted head, retains no artifacts, and has no independent clean-checkout acceptance replay. The candidate may be selected only after the installation defect is corrected, the complete suite succeeds at one immutable reviewed head, and the evidence bundle is retained.

## Planned Changelog Entries

- `Fixed`: deterministic whitespace collapse and standards-based TOML dependency-envelope parsing, after independent acceptance.
- `Added`: versioned canonical-record/attribution contracts, deterministic fixtures, and hashes.
- `Security`: credential-free sanitizer job, artifact-only handoff, fail-closed digest verification, least-privilege workflows, hidden-control scan, and adversarial conformance suite.
- `Changed`: workflow checkout/install behavior and documentation describing actual rather than implied isolation.
- `Release`: source/package artifacts, CLI/PDF samples, reports, SBOM where applicable, checksums, provenance, and approval.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0, P1, and P2 are `DONE` with linked commits, commands, workflow runs, and retained artifacts. |
| Tests/CLI/reports | FAIL | Current-head-associated run `29564563760` fails during installation and skips the verifier, pytest, and hidden-control steps; the full CLI/PDF replay must pass from a clean exact-head checkout. |
| Candidate repairs | REVIEW | Local evidence reports 11 passing tests, verifier/compile/CLI/PDF checks, TOML parsing tests, and hashes; independent exact-head acceptance remains absent. |
| Contract determinism | INCOMPLETE | Schemas and fixtures must reproduce identical transformations, decisions, rejection reasons, provenance, and hashes across supported environments. |
| Security isolation | FAIL | Retrieval and sanitizer are independently permissioned; sanitizer has no credentials or network and verifies the artifact digest before processing. |
| Adversarial validation | NO EVIDENCE | Hostile/malformed inputs produce deterministic accepted/rejected outputs without execution or provenance loss in retained CI and clean-checkout evidence. |
| Workflow integrity | FAIL | Correct installation, exact submitted-head checkout, pinned runtimes/actions, minimum permissions, successful checks, and retained logs/artifacts are required. |
| Documentation | PARTIAL | Boundaries and local candidate evidence are documented, but setup, failure cause, supported environments, isolation truthfulness, and recovery are not independently verified. |
| Provenance | PARTIAL | Candidate commits, commands, local hashes, and failed workflow metadata are recorded; successful exact-head logs, artifacts, checksums, attestations, and rollback evidence are absent. |
| Approval | PENDING | Explicit release approval after all blocking gates pass. |

## Artifact Requirements

- Versioned canonical-record and attribution-sidecar schemas.
- Positive, negative, adversarial, boundary, dependency-envelope, and digest-mismatch fixtures with expected outputs and hashes.
- Source/package artifact, CLI sample, JSON audit/evidence records, PDF evidence report, and independently permissioned workflow definitions.
- Complete clean-checkout test, security-envelope, hidden-control, workflow-permission, isolation, and documentation reports.
- Successful exact-head workflow logs and retained artifacts; failure logs remain part of the provenance record.
- SBOM where applicable, SHA-256 checksums, provenance manifest, attestation, and tested rollback evidence.

## Rollback Criteria

Reject or roll back the candidate if installation is not reproducible; CI verifies a synthetic or different state than the reviewed head; fetched material executes; sanitizer credentials or network access are introduced; artifact digests are not verified; accepted/rejected results become nondeterministic; provenance is lost; reports diverge from canonical records; dependencies exceed the approved envelope; hidden controls pass undetected; or documentation overstates isolation. Restore the prior verified state and retain rejected artifacts, logs, hashes, and reports for comparison.

## Unresolved Blockers

- PR #2 workflow run `29564563760` fails at environment installation; all substantive verification steps are skipped and no artifacts are retained.
- The workflow checks the pull-request merge ref rather than establishing a successful exact submitted-head replay; no independent clean-checkout replay exists.
- GitHub currently reports PR #2 non-mergeable.
- P0 baseline acceptance, P1 versioned contracts, and P2 independently permissioned retrieval/sanitizer separation are incomplete.
- Retrieval and sanitization still share a logical/workflow boundary rather than independently permissioned jobs.
- Complete deterministic, adversarial, dependency, security, documentation, provenance, checksum, attestation, and rollback evidence remains absent.
- QuantumStateObjects cannot consume a verified canonical-record contract until P1 is published and independently accepted.

## Release Log

- 2026-07-16: Aligned the candidate with the secure read-only retrieval MVP; release remained blocked by isolation and deterministic contract evidence.
- 2026-07-17: Recorded PR #2 as a bounded P0 candidate with local verifier, 11-test, CLI/PDF, workflow-inspection, and hash evidence. Release remains blocked because current-head-associated run `29564563760` fails during installation, skips all substantive checks, retains no artifacts, and does not provide exact submitted-head or independent clean-checkout acceptance.