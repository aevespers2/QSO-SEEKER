# Semiweekly Repository Redesign and Pruning — 2026-07-21

## Scope

Reviewed active pull-request architecture, planning state, CI evidence, dependency and workflow boundaries, duplicated responsibilities, and recent defect history across `aevespers2/QSO-SEEKER`, `aevespers2/QuantumStateObjects`, and `aevespers2/QSO-GENOMES`.

This pass selected exactly one bounded candidate. No source code, dependency, workflow, branch, artifact, or historical evidence was deleted.

## Candidate ranking

Scores use 1–10, where higher correctness, complexity reduction, integration/accessibility, maintenance savings, and reversibility are beneficial; higher blast radius and verification cost are adverse.

| Candidate | Correctness | Complexity reduction | Integration / accessibility | Maintenance savings | Reversibility | Blast radius | Verification cost | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Retire QSO-SEEKER historical P0 PR #2 | 8 | 9 | 8 | 9 | 10 | 1 | 1 | **Selected** |
| Retire QuantumStateObjects documentation PR #1 behind PR #12 | 5 | 7 | 5 | 6 | 10 | 1 | 1 | Queue |
| Reconcile QuantumStateObjects PR #7 with current `main` | 10 | 7 | 10 | 9 | 8 | 7 | 9 | Builder P0, not pruning |
| Reconcile QSO-GENOMES PRs #2/#12/#13 | 10 | 9 | 10 | 10 | 7 | 9 | 10 | Blocked architectural decision |
| Consolidate repository-wide consent validators | 8 | 9 | 9 | 9 | 7 | 8 | 9 | Semiweekly queue |
| Retire overlapping QSO-SEEKER experimental branches | 7 | 10 | 8 | 9 | 10 | 5 | 6 | Requires per-branch disposition |

## Selected pruning

QSO-SEEKER PR #2 was closed without merge and retitled `superseded: historical P0 security and CLI baseline`.

### Reason

PR #2 predates the accepted canonical-record and attribution-sidecar v1 contract, the merged repository-wide consent-capacity controls, and retained current-head evidence. PR #14 is the preservation-safe current composition and has exact-head Documentation, Security Envelope, and Consent Capacity Lock evidence with retained artifacts.

Keeping PR #2 open falsely represented two active P0 paths and increased the risk that automated planning, review, or release logic would select stale evidence.

### Before

- PR #2: open draft, nonmergeable, 23 commits, 11 changed files, 267 additions, 63 deletions.
- Historical exact head: `306dfa4104c12594b23dda8111e1c80edb0be397`.
- Historical workflow evidence retained no release artifact.
- Planning still required reconciliation or retirement of PR #2.

### After

- PR #2: closed without merge; branch, commits, comments, and workflow history preserved.
- Active P0 review ambiguity reduced from two candidate paths to one current reconciliation path, PR #14.
- Reopening remains the rollback procedure and does not require history reconstruction.
- Runtime behavior, dependencies, packages, workflows, schemas, and accepted `main` content are unchanged.

## Verification

The pruning is metadata-only. Equivalent evidence consists of:

1. PR #2 reports `state=closed`, `merged=false`, and retains head `306dfa4104c12594b23dda8111e1c80edb0be397`.
2. PR #14 remains the current preservation-safe reconciliation candidate.
3. PR #14 exact head `3ae6e0274841dceca4403b6812240bee948feb31` previously passed Documentation run `29872741201`, Security Envelope run `29872741223` with 32 tests, and Consent Capacity Lock run `29872741213`, with three retained artifacts.
4. This planning/evidence update changes the PR #14 head and therefore requires fresh exact-head workflows before review or merge acceptance.

## Quantified effect

- Production code removed: `0` lines.
- Dependencies removed: `0`.
- Active pull requests removed from the review queue: `1`.
- Stale candidate surface retired: 23 commits / 11 changed files / 267 additions / 63 deletions, preserved as history rather than deleted.
- Estimated Seeker Development Benchmark effect: Delivery Efficiency `+2`, Integration & Accessibility `+1`, Learning & Capability Growth `+1`; no correctness credit until the updated planning head passes exact-head workflows.
- AGI Progress relevance: modest improvement to self-correction, evidence discipline, and governed planning; no new general-intelligence capability claimed.

## Risks and rollback

Risk is low: closing the pull request changes review-queue state only. The branch remains accessible. Rollback is to reopen PR #2 if a specific historical regression investigation requires it. Reopening must not restore PR #2 as a current release candidate without reconciliation and fresh exact-head evidence.
