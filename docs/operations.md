# Operations and recovery

## Operational posture

QSO-SEEKER is presently documented as a local, bounded processing component. No production service, scheduled collector, private-source connector, or shared-field publisher is approved by this documentation. Operational procedures therefore focus on reproducible local runs, evidence preservation, failure containment, and rollback.

## Pre-run checklist

1. Record the repository commit SHA and configuration identity.
2. Confirm the input source and usage terms have been separately reviewed.
3. Verify the sanitizer environment has no source credentials or repository-write token.
4. Confirm input is a bounded local JSON artifact.
5. Record the artifact digest before processing.
6. Use a clean environment with the expected Python and dependency versions.
7. Confirm available storage is sufficient for accepted, audit, report, and temporary files.
8. Select an output directory that does not contain earlier evidence.

## Standard run

```bash
set -euo pipefail
mkdir -p build/run-001
sha256sum input.json > build/run-001/input.sha256
unicernal-search sanitize input.json \
  --output build/run-001/accepted.json \
  --audit build/run-001/audit.json \
  --report build/run-001/report.json \
  --pdf build/run-001/report.pdf
sha256sum build/run-001/accepted.json \
  build/run-001/audit.json \
  build/run-001/report.json \
  build/run-001/report.pdf > build/run-001/outputs.sha256
```

The shell example is for an operator-controlled environment; source content is never interpolated into shell commands.

## Health checks

A healthy bounded run has:

- a recorded exact code revision;
- an input digest that matches the supplied artifact;
- valid JSON accepted and audit outputs;
- one audit decision per input record;
- no unhandled source-content execution path;
- expected counts for accepted, flagged, and rejected records;
- reproducible content hashes for repeated identical inputs;
- no secrets or private material in logs or reports;
- successful independent validation for any canonical handoff artifact.

## Observability

Record only the information needed to understand behavior:

- code revision and tool version;
- start and completion timestamps;
- input artifact identity and size;
- counts by decision and rejection reason;
- transformation and flag counts;
- output artifact identities;
- denied capabilities and environment boundary;
- test and validator results;
- reviewer disposition.

Do not log credentials, private source contents, prohibited records, or unnecessary full text. Use hashes and bounded fixture identifiers where possible.

## Failure classes

| Failure | Response |
|---|---|
| Invalid top-level JSON | Stop; preserve the error and input digest; do not create a partial handoff |
| Individual schema rejection | Preserve the audit entry; continue only if the run policy permits partial results |
| Binary or unsupported file type | Reject; do not unpack, inspect, or execute it |
| Hash or contract mismatch | Quarantine the artifact; stop downstream handoff |
| Output write or PDF failure | Mark evidence generation incomplete; do not present the run as complete |
| Nondeterministic accepted content hash | Stop; preserve both runs and open an integrity investigation |
| Unexpected network, credential, subprocess, or write capability | Stop immediately; isolate the environment and treat the run as a security incident |
| Documentation or evidence mismatch | Block release and correct the record before approval |

## Rollback

Because the current component is local and artifact-oriented, rollback means returning to the last accepted code revision and invalidating evidence produced by the rejected candidate.

1. Stop processing and prevent downstream use of candidate artifacts.
2. Preserve the failed input digest, exact code revision, outputs, logs, and validator findings.
3. Mark affected artifacts as rejected or quarantined; do not overwrite them.
4. Restore the previous accepted revision in a clean environment.
5. Revoke any temporary permissions that exceeded the accepted boundary.
6. Rerun the complete deterministic and adversarial suite.
7. Replay representative fixtures and compare expected hashes.
8. Record the rollback result in the pull request, release record, and changelog.
9. Resume only after human review confirms the accepted boundary is restored.

## Incident response

### Contain

Disable the affected workflow or operator path, preserve exact-head evidence, and prevent artifacts from reaching consumers.

### Assess

Determine whether the issue affects input validation, sanitization, contract identity, attribution, retained evidence, permissions, dependencies, documentation, or downstream consumers.

### Repair

Use the smallest bounded change, add a regression fixture, and avoid combining unrelated new capability with the repair.

### Verify

Run clean installation, tests, security verification, hidden-control checks, contract replay, documentation build, and rollback validation against the final submitted head.

### Communicate

Record impact, affected versions or commits, artifact identities, consumer actions, and residual risk without publishing secrets or harmful payloads.

## Retention and disposal

Retention is deployment-specific and requires separate approval. At minimum, preserve accepted release evidence and rejected-candidate identities long enough to audit decisions and support rollback. Delete temporary raw material and local working copies according to source terms, privacy requirements, and the approved retention policy. Hashes should not be assumed anonymous when they can be linked to sensitive source material.

## Publication gate

Before publishing a release or Pages site as authoritative, confirm:

- current `main` matches the documented contract and status;
- all links and Pages navigation build in strict mode;
- release gates contain exact evidence rather than aspirational claims;
- artifacts, checksums, provenance, and rollback results are retained;
- legal, privacy, licensing, and source obligations are approved;
- a human reviewer explicitly authorizes the release.
