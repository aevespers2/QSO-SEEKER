# Task Chain

## Repository role
Read-only retrieval boundary, hostile-input sanitization, canonical-record production, attribution sidecars, and evidence reports for QSO experiments.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0 | Establish a reproducible security and CLI baseline | QSOBuilder | — | READY | The full pytest suite, security-envelope verifier, CLI JSON output, PDF report test, and workflow syntax checks pass or every failure is recorded with a reproducer; no fetched content is executed. |
| P1 | Version the canonical record plus attribution-sidecar contract | QSOBuilder | P0 | PROPOSED | A schema/fixture pair defines required fields, size limits, transformations, rejection reasons, provenance, and content hashes; `QuantumStateObjects` can validate fixtures without importing QSO-SEEKER code. |
| P2 | Split public retrieval and sanitization into separately permissioned workflow jobs | QSOBuilder | P0 | PROPOSED | Fetch job has read-only network credentials; sanitizer job receives only an inert artifact, has no repository/network credential, fails closed on missing hashes, and preserves a verifiable handoff digest. |
| P3 | Publish adversarial conformance fixtures | Builder | P1 and P2 | PROPOSED | Fixtures cover Unicode concealment, prompt injection, executable types, oversized input, binary content, malformed attribution, and deterministic accepted/rejected outputs. |

## Architectural boundary
The existing public-scan workflow is useful but its retrieval and sanitizer steps currently share one job. Until P2 is complete, documentation must describe this as logical separation rather than process or microVM isolation.

## Builder Log
Record commits, workflow runs, test commands/results, fixture hashes, residual risks, and follow-ups.
