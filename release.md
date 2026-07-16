# Release Plan

## Current Decision

Status: `BLOCKED — SECURITY ISOLATION AND CONTRACT EVIDENCE REQUIRED`

QSO-SEEKER has a defined read-only hostile-input boundary, but no retrieval/sanitization release is eligible. P0 remains `READY`, every punch-list item is unchecked, retrieval and sanitization are not yet independently permissioned, and candidate head `d4b2a4933fc5426e26c139d628efec293813f8c4` lacks current pytest, CLI, PDF, workflow, deterministic-contract, adversarial, security, documentation, provenance, checksum, and rollback evidence.

## Versioning

- Scheme: Semantic Versioning for the CLI, canonical-record schema, attribution sidecar, and workflow contract.
- First eligible candidate: `0.1.0-alpha.1`.
- Compatible fields/rejection reasons may be minor changes.
- Security-boundary, required-field, transformation, canonicalization, or hash changes require explicit compatibility review and migration fixtures.

## Release Scope

- Reproducible pytest, security-envelope, CLI JSON, PDF report, and workflow baseline.
- Versioned canonical-record and attribution-sidecar schemas with deterministic accepted/rejected fixtures and hashes.
- Separate read-only retrieval and credential-free, network-free sanitizer jobs with artifact-only handoff and digest verification.
- Adversarial fixtures for Unicode concealment, prompt injection, executable/binary types, oversized input, malformed attribution, and digest mismatch.
- Accurate trust-boundary documentation, security reports, checksums, provenance, and rollback.

## Selected Completed Work

None. Existing boundaries, source, and documentation are candidate inputs, but P0-P2 have no accepted evidence and the required isolation model is not implemented.

## Planned Changelog Entries

- `Added`: versioned canonical-record/attribution contracts, deterministic fixtures, and hashes.
- `Security`: credential-free sanitizer job, artifact-only handoff, fail-closed digest verification, and adversarial conformance suite.
- `Changed`: workflow permissions and documentation describing actual rather than implied isolation.
- `Fixed`: transformation, rejection, provenance, digest, or report-generation defects found during verification.
- `Release`: source/package artifacts, reports, SBOM where applicable, checksums, provenance, and approval.

## Acceptance Gates

| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0, P1, and P2 are `DONE` with linked commits, commands, and workflow evidence. |
| Tests/CLI/reports | NO EVIDENCE | Full pytest, envelope verifier, CLI JSON, PDF report, and workflow syntax checks pass. |
| Contract determinism | NO EVIDENCE | Schemas and fixtures reproduce identical transformations, decisions, rejection reasons, and hashes. |
| Security isolation | FAIL | Retrieval and sanitizer are independently permissioned; sanitizer has no credentials or network and verifies the artifact digest. |
| Adversarial validation | NO EVIDENCE | Hostile/malformed inputs produce deterministic accepted/rejected outputs without execution or provenance loss. |
| Documentation | NO EVIDENCE | Trust boundary, transformations, limits, rejection reasons, provenance, commands, and actual isolation are verified. |
| Provenance | NO EVIDENCE | Commit, workflow runs, tool versions, fixture/report hashes, artifacts, checksums, and attestations are retained. |
| Approval | PENDING | Explicit release approval after all blocking gates pass. |

## Artifact Requirements

- Versioned canonical-record and attribution-sidecar schemas.
- Positive, negative, adversarial, boundary, and digest-mismatch fixtures with expected outputs and hashes.
- Source/package artifact, CLI sample, PDF evidence report, and independently permissioned workflow definitions.
- Complete test, security, workflow-permission, and documentation reports.
- SBOM where applicable, SHA-256 checksums, provenance manifest, and rollback evidence.

## Rollback Criteria

Rollback if fetched material executes, sanitizer credentials or network access are introduced, artifact digests are not verified, accepted/rejected results become nondeterministic, provenance is lost, reports diverge from canonical records, or documentation overstates isolation. Restore the prior verified state and retain rejected artifacts and reports for comparison.

## Unresolved Blockers

- P0 baseline, P1 contracts, and P2 workflow separation are incomplete.
- Retrieval and sanitization still share a logical/workflow boundary rather than independently permissioned jobs.
- No current test, CLI, PDF, deterministic fixture, adversarial, security, documentation, provenance, checksum, or rollback evidence exists.
- QuantumStateObjects cannot consume a verified canonical-record contract until P1 is published.

## Release Log

- 2026-07-16: Aligned the candidate with the secure read-only retrieval MVP; release remains blocked by isolation and deterministic contract evidence.