# Task Chain

Architect owns task dependencies, sequencing, acceptance criteria, and boundaries. Builders execute one highest-priority unblocked task at a time, preserve tests and rollback paths, and record evidence.

States: `PROPOSED` · `READY` · `IN PROGRESS` · `BLOCKED` · `REVIEW` · `DONE`

| Priority | Task | Owner | Depends on | Status | Acceptance criteria |
|---|---|---|---|---|---|
| P0 | Repository health baseline | Architect | — | READY | Workflows, tests, dependencies, and known defects are inventoried. |
| P1 | Define next bounded implementation task | Architect | P0 | PROPOSED | Scope names files, tests, constraints, and rollback guidance. |

## Builder Log
Record commits, verification commands/results, risks, and follow-ups.
