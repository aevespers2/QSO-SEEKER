# Repository governance

## Source-of-truth documents

QSO-SEEKER uses three coordinated records:

- `taskchain.md` defines ordered objectives, dependencies, ownership, and acceptance criteria.
- `release.md` records the current release decision, scope, gates, artifacts, and blockers.
- `changelog.md` records notable product, architecture, implementation, evidence, release, and deployment changes.

A documentation or implementation pull request is incomplete when these records disagree about accepted capability or current status.

## Decision hierarchy

1. **Repository purpose and non-goals** constrain every task.
2. **Accepted contracts** define cross-component semantics.
3. **Task-chain status** determines which work is eligible to advance.
4. **Exact-head evidence** demonstrates behavior for a specific candidate.
5. **Human review** accepts or rejects the candidate and its residual risk.
6. **Release approval** authorizes publication only after every blocking gate passes.

A passing workflow is evidence, not an automatic architecture or release decision.

## Current accepted baseline

The repository contains a local hostile-input sanitizer, audit and evidence reporting, canonical-record v1, attribution-sidecar v1, and repository security controls. The version-1 canonical contract was merged after exact-head verification. The broader collection, private-overlay, scheduled workflow, experimental genome, spawning, QSIO integration, and shared-field proposals remain separate candidates unless and until merged through their own accepted task dependencies.

## Change classification

| Change | Required treatment |
|---|---|
| Documentation correction with no semantic change | Documentation review and strict Pages build |
| New example consistent with v1 | Fixture review and deterministic validation |
| New transformation or rejection rule | Security review, tests, changelog, and compatibility analysis |
| New canonical field or hash input | New contract version or explicitly approved migration |
| New source kind | Raw-schema and canonical-contract compatibility decision |
| New dependency | Dependency-envelope and supply-chain review |
| New network, credential, scheduling, repository-write, consumer, or publisher capability | Separate architecture, security, privacy, legal, operations, and rollback approval |
| New downstream integration | Version-pinned contract, independent validation, capability review, and consumer acceptance |

## Pull-request status

Draft status should be retained while evidence, architecture, or dependencies are incomplete. A candidate may become ready for review only when its final head is stable, checks have been rerun on that exact head, documentation is aligned, and known blockers are stated plainly. Mergeability alone does not mean the candidate is eligible for merge.

## Architectural records

Material decisions should be captured as architecture decision records when they affect:

- trust boundaries;
- contract versioning or hashing;
- retrieval and sanitizer separation;
- source and licensing policy;
- evidence retention;
- downstream consumer authority;
- release and rollback ownership.

An ADR should state context, decision, alternatives, consequences, compatibility, verification, migration, rollback, and supersession rules.

## Documentation ownership

Every code owner is also responsible for the documentation of fields, limits, errors, evidence, and boundaries they change. Security and release reviewers are responsible for rejecting wording that overstates isolation, safety, authority, or release readiness.

## Milestone definition

A substantial documentation milestone includes a coherent set of user-facing and developer-facing pages, architecture and lifecycle diagrams, aligned repository governance records, and a reviewable pull request. Small wording edits, link repairs, and formatting cleanup should be accumulated without sending milestone notifications unless they resolve an architectural blocker.

## Required clarification cases

Pause and request an architecture decision when documentation cannot be made internally consistent without choosing among competing repository roles, canonical identities, contract semantics, authority owners, or release targets. Do not invent a decision merely to complete a page.
