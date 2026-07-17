# P0 Security and CLI Baseline — 2026-07-17

## Scope

This report records the bounded QSO-SEEKER P0 baseline for tests, the independent security-envelope verifier, CLI JSON output, PDF evidence generation, Python compilation, packaging installation, and workflow syntax/permission inspection.

- Repository: `aevespers2/QSO-SEEKER`
- Source base: `f9b6d696587450c0e279e81c15011a571b61952e`
- Candidate branch: `builder/p0-security-cli-baseline-20260717`
- Initial implementation/test commit: `1c55ee45edbb4fe05c27efcb9c4c6d4e375a9321`
- Packaging remediation commit: `cfb7a22480b60ba6198a4f7d622c002378e1c061`
- Initial PR head: `551c4b24831de73d3d4e202bcb08fdaf6d281c66`
- Pull request: `#2`
- Environment: Linux x86_64; CPython 3.13.5; pytest 9.0.2; pydantic 2.13.4; PyYAML 6.0.3

Direct GitHub cloning was unavailable in the verification runner because DNS resolution failed. The local replay used exact UTF-8 contents fetched through the GitHub Contents API and a bounded packaging reproducer. This remains candidate evidence until the final submitted head has an attached successful workflow or independently reviewed clean-checkout replay.

## Baseline findings and bounded repairs

### 1. Whitespace canonicalization

The existing security test expected all whitespace runs to collapse deterministically. NFKC converted non-breaking space to ordinary space, but the regular expression excluded ordinary spaces, producing repeated spaces and failing `test_whitespace_is_canonicalized`.

Repair: canonicalization now uses `re.compile(r"\s+")`, so ordinary and Unicode whitespace runs collapse to one space.

### 2. Dependency-envelope parsing

The verifier parsed the dependency list with string slicing and line splitting. The checked-in one-line declaration `dependencies = ["pydantic>=2.6"]` was therefore read as empty and falsely reported the approved dependency as missing.

Repair: the verifier now uses Python's standard-library `tomllib`, and two focused tests cover the one-line approved dependency and an unapproved `requests>=2` dependency.

### 3. Editable-install package discovery

The workflow's `python -m pip install -e . pytest` step failed before any verifier or test executed. A bounded reproduction using the candidate `pyproject.toml` and the repository's flat-layout package candidates produced setuptools' deterministic failure:

```text
error: Multiple top-level packages discovered in a flat-layout: ['schemas', 'contracts', 'unicernal_search'].
```

Repair: `[tool.setuptools.packages.find]` now includes only `unicernal_search*`. The added regression test verifies the runtime package matches and that `contracts`, `schemas`, `tests`, and `tools` do not match the discovery scope. Replaying the same editable-install reproducer after the change successfully built and installed `unicernal-search-gateway==0.1.0`.

## Local commands and results

```text
python tools/verify_security_envelope.py
PASS — {"status": "pass", "findings": []}

python -m pytest -q
PASS — 11 tests at the initial implementation/test commit

python -m compileall -q unicernal_search tools tests
PASS — exit code 0

python -m unicernal_search.cli sanitize <input> --output <sanitized> --audit <audit> --report <evidence> --pdf <pdf>
PASS — one flagged inert record accepted, one archive record rejected, JSON outputs parsed, content digest replayed, and PDF header/EOF verified

PyYAML safe-load plus structural assertions for .github/workflows/security-envelope.yml and .github/workflows/public-scan.yml
PASS — both workflows parsed; each has a jobs map and top-level contents: read permission

Tracked-text hidden-control scan using the workflow's forbidden-code-point set
PASS — no forbidden hidden controls in the mirrored tracked text

python -m pip install -e . --no-deps  # bounded flat-layout reproducer before discovery scope
FAIL — multiple top-level packages discovered: schemas, contracts, unicernal_search

python -m pip install -e . --no-deps  # same reproducer after discovery scope
PASS — editable wheel built and unicernal-search-gateway 0.1.0 installed
```

## Attached GitHub Actions result

Security Envelope run `29564325393` (run number `24`) was triggered for PR #2 at initial head `551c4b24831de73d3d4e202bcb08fdaf6d281c66`.

- Checkout: `PASS`
- Python setup: `PASS`
- Install minimal test environment: `FAIL`
- Security verifier, pytest, and hidden-control steps: `SKIPPED` because installation failed
- Runner: Ubuntu 24.04.4; runner image `ubuntu-24.04` version `20260714.240.1`; Git `2.54.0`
- Token permission evidence: `Contents: read`, `Metadata: read`

The package-discovery failure is now reproducible and remediated in the candidate. A successful workflow attached to the final submitted head is still required before P0 can move out of `IN PROGRESS`.

## CLI fixture result

- Accepted records: `1`
- Flagged records: `1` (`prompt_injection`)
- Rejected records: `1` (`executable_archive_or_binary`)
- Canonical content SHA-256: `c0c71b572d7156f67c4e8bd9ff657146fafbf3b67d0afa20b25e31437b1db4f0`
- Summary SHA-256: `8306cc7c1ba409f2034fb93339573a2d754381c71f9811d8fab3fe44ab68ad96`

Generated artifact SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| `input.json` | `30c7b50e3b1c2c9ce296ac4b39647fe79780b7a43b885bce9801ba016ecc9cb8` |
| `sanitized.json` | `6f7b4c490cc184421854fbd195f79bf588fc64753245211e70c8a595e51775ec` |
| `audit.json` | `768712ca7346b09a57bfc17b48e8f3696f1db616482ba2836d40ab95ce83c9c9` |
| `evidence.json` | `cd06ad680791123d4b59f96da827b539d8c5934883be9b29f79854d8ff2d6336` |
| `evidence.pdf` | `c006b6a85b427a238ff7484218379003e4158d55135e33fa0885e3067b90ce5a` |

Candidate source SHA-256 values:

| Path | SHA-256 |
|---|---|
| `unicernal_search/canonicalize.py` | `cdc0496e0d4290e02384b641e179e32bc534468c4741bc9037e4285e108dc800` |
| `tools/verify_security_envelope.py` | `c8798afd010d5b43d51ffdbf1e99cb7c9c0a24ac898c32d6c10f038f30820527` |
| `tests/test_security_verifier.py` | `374dbfe6c65ea795edb84b3a6b94f7afe12137afbdc768598cb2f6a9ddaec5bc` |
| `pyproject.toml` after package-discovery repair | `ca2a13e5fc70684bdc2bc179a4da0ebf97d76dbbeeab0e59606c385575d0ac92` |
| `tests/test_packaging_config.py` | `916ee1907a16a10a66adc55839b1913ed18529c6f9820e967791c49f6c05395a` |

## Residual gates

- Obtain a successful complete Security Envelope workflow run attached to the final submitted head.
- Retain exact submitted-head or independently reviewed clean-checkout evidence rather than relying only on a generated PR merge ref or bounded mirror.
- P1 contract publication and P2 independently permissioned retrieval/sanitizer jobs remain separate follow-on tasks.
- This task adds no network, credential, execution, repository-write, or autonomous decision authority.
