# Developer onboarding

## Prerequisites

- Python 3.11 or later
- Git
- A virtual environment
- Optional: MkDocs for local documentation preview

## Clone and install

```bash
git clone https://github.com/aevespers2/QSO-SEEKER.git
cd QSO-SEEKER
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest mkdocs
```

On Windows PowerShell, use `.venv\Scripts\Activate.ps1` instead of the POSIX activation command.

## Repository map

```text
unicernal_search/       Runtime package
  cli.py                Console entry point and evidence summary
  schema.py             Strict raw and sanitized models
  gateway.py            Rejection, sanitization, flags, and audit
  canonicalize.py       Shared text canonicalization helpers
  contracts.py          Canonical-record and sidecar v1 contracts
  report.py             JSON loading and PDF rendering
contracts/              Human-readable contract specifications
schemas/                Machine-readable schemas and examples, where present
tests/                  Deterministic and adversarial tests
tools/                  Security and repository verification tools
security/               Threat and capability documentation
reports/                Review and release evidence records
docs/                   GitHub Pages source
taskchain.md             Ordered product and architecture work
release.md               Release gates and current decision
changelog.md             Notable repository changes
```

Not every branch contains every proposed directory. Review the current base and do not treat draft pull-request content as accepted repository scope.

## Run the test suite

```bash
python -m pytest
```

Before submitting a contract or security-boundary change, also run the repository verifier when present:

```bash
python tools/verify_security_envelope.py
```

Tests should cover deterministic replay, malformed fields, unknown fields, boundary sizes, path and URL rejection, Unicode edge cases, mutation, hash mismatch, package discovery, dependency drift, and prohibited capabilities.

## Run the CLI

```bash
unicernal-search sanitize examples/input.json \
  --output build/accepted.json \
  --audit build/audit.json \
  --report build/report.json \
  --pdf build/report.pdf
```

Inspect both accepted and audit output. A successful process exit does not mean every input was accepted.

## Build the documentation

```bash
mkdocs build --strict
mkdocs serve
```

Strict mode is required so missing pages, malformed navigation, and broken internal references are visible before review. Documentation should use relative links and committed static diagrams rather than assuming a particular local path.

## Contribution workflow

1. Read `taskchain.md`, `release.md`, and the latest `changelog.md` entries.
2. Identify the smallest bounded change that advances an accepted task.
3. Create a branch from current `main`.
4. Preserve the sanitizer's non-executing and least-authority boundaries.
5. Add or update deterministic fixtures and negative tests.
6. Update documentation in the same change when behavior, fields, limits, errors, or trust boundaries change.
7. Record exact test commands and results in the pull request.
8. Keep the pull request draft until its final head has complete evidence.
9. Rerun checks after every material head change.
10. Require human acceptance before merge, release, or downstream use.

## Coding guidance

- Prefer standard-library primitives when they are sufficient.
- Keep parsing strict and explicit.
- Reject ambiguous values rather than coercing them.
- Keep deterministic functions independent of clocks, network, and local machine state.
- Sort collections before hashing when the contract requires canonical order.
- Return defensive copies from validators.
- Preserve stable rejection reasons because downstream evidence may depend on them.
- Do not add imports, subprocesses, dynamic evaluation, package installation, or network access based on source content.

## Documentation guidance

Every page should distinguish among:

- implemented behavior on `main`;
- accepted contracts;
- target architecture not yet evidenced; and
- separate draft proposals.

Use precise terms such as “logical separation,” “recommended boundary,” or “proposed” until implementation and exact-head evidence justify stronger claims.

## Pull-request checklist

- [ ] Scope matches an active task or approved clarification.
- [ ] Implementation surface did not expand implicitly.
- [ ] Tests include expected failures, not only happy paths.
- [ ] Contract and migration implications are documented.
- [ ] Security and capability boundaries are unchanged or explicitly reviewed.
- [ ] `taskchain.md`, `release.md`, and `changelog.md` agree.
- [ ] Pages build succeeds in strict mode.
- [ ] Final-head workflow evidence is attached or linked.
- [ ] No secrets or private source material are committed.
- [ ] Rollback instructions are practical and bounded.
