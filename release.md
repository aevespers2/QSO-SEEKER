# Release Plan

## Current Decision
Status: `BLOCKED`

No retrieval or sanitization work is currently eligible for release. P0 is only `READY`, every punch-list and quality-gate item is unchecked, the current public-scan design does not yet separate retrieval and sanitization into independently permissioned jobs, and reviewed commit `e390be468ba99585ba3467cd8b0473d2090fd3b4` has no reported commit-status checks.

## Versioning
- Scheme: Semantic Versioning for the CLI, canonical-record schema, attribution sidecar, and workflow contract.
- First eligible candidate: `0.1.0-alpha.1`.
- Backward-compatible fields and rejection reasons may be minor changes; security-boundary, required-field, transformation, or hash changes require explicit compatibility review and migration fixtures.

## Candidate Scope
- Reproducible pytest, security-envelope, CLI JSON, PDF report, and workflow-syntax baseline.
- Versioned canonical-record and attribution-sidecar schemas with deterministic fixtures and hashes.
- Separate read-only fetch and credential-free sanitizer jobs with artifact-only handoff and verified digest.
- Adversarial fixtures for Unicode concealment, prompt injection, executable types, oversized input, binaries, and malformed attribution.
- Minimum-permission, pinned-runtime workflows and accurate isolation claims.

## Selected Completed Work
None. The repository boundaries are defined, but no test, contract, workflow-split, or adversarial-fixture work has completed acceptance evidence.

## Planned Changelog Entries
- `Added`: versioned canonical-record and attribution-sidecar contracts, fixtures, and deterministic hashes.
- `Security`: credential-free sanitizer job, artifact-only handoff, fail-closed digest verification, and adversarial conformance suite.
- `Changed`: workflow permissions and documentation describing actual rather than implied isolation.
- `Fixed`: deterministic transformation, rejection, provenance, or report-generation defects found during baseline testing.
- `Documentation`: hostile-input model, exact commands, limitations, failure modes, and consumer validation guidance.

## Acceptance Gates
| Gate | Status | Requirement |
|---|---|---|
| Task completion | FAIL | P0, P1, and P2 are `DONE` with linked commits and workflow evidence. |
| Tests/CLI/reports | NO EVIDENCE | Full pytest, envelope verifier, CLI JSON, PDF report, and syntax checks pass. |
| Contract determinism | NO EVIDENCE | Schemas and fixtures reproduce identical transformations, decisions, and hashes. |
| Security isolation | FAIL | Retrieval and sanitizer currently share a job; credential-free artifact-only separation is required. |
| Adversarial validation | NO EVIDENCE | Hostile-input fixtures produce deterministic accepted/rejected outputs without execution. |
| Documentation | NO EVIDENCE | Trust boundary, transformations, rejection reasons, provenance, limits, and actual isolation are documented. |
| Provenance | NO EVIDENCE | Commit, workflow runs, tool versions, fixture hashes, reports, checksums, and attestations recorded. |
| Approval | PENDING | Release approval after all blocking gates pass. |

## Artifact Requirements
- Versioned canonical-record and attribution-sidecar schemas.
- Positive and adversarial fixture bundle with deterministic expected outputs and hashes.
- CLI/package or source archive, PDF evidence report sample, and workflow definitions.
- Test, security, and workflow-permission reports.
- SBOM where packaged, checksums, and provenance manifest.

## Rollback Criteria
Rollback if fetched material is executed, sanitizer credentials or network access are introduced, artifact digests are not verified, accepted/rejected results become nondeterministic, provenance is lost, report outputs diverge from canonical records, or documentation overstates isolation. Restore the prior verified tag and retain rejected artifacts for forensic comparison.

## Unresolved Blockers
- P0 baseline, P1 contracts, and P2 workflow separation are incomplete.
- Retrieval and sanitization still lack independently permissioned process separation.
- No test, CLI, PDF, deterministic fixture, adversarial, security, documentation, or provenance evidence is recorded.
- `QuantumStateObjects` cannot validate canonical-record fixtures until P1 is complete.
- No CI status is attached to the reviewed commit.

## Release Log
- 2026-07-16: QSO-SEEKER candidate evaluated and held `BLOCKED`; no completed work selected.