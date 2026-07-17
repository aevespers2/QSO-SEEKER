# P0 Security and CLI Baseline — 2026-07-17

## Scope

This report records the bounded QSO-SEEKER P0 baseline for tests, the independent security-envelope verifier, CLI JSON output, PDF evidence generation, Python compilation, and workflow syntax/permission inspection.

- Repository: `aevespers2/QSO-SEEKER`
- Source base: `f9b6d696587450c0e279e81c15011a571b61952e`
- Candidate branch: `builder/p0-security-cli-baseline-20260717`
- Implementation/test commit: `1c55ee45edbb4fe05c27efcb9c4c6d4e375a9321`
- Environment: Linux x86_64; CPython 3.13.5; pytest 9.0.2; pydantic 2.13.4; PyYAML 6.0.3

Direct GitHub cloning was unavailable in the verification runner because DNS resolution failed. The replay used a local mirror assembled from the exact UTF-8 contents fetched from the source base and candidate branch through the GitHub Contents API. This is candidate evidence, not an independent clean-checkout or attached GitHub Actions acceptance run.

## Baseline findings and bounded repairs

### 1. Whitespace canonicalization

The existing security test expected all whitespace runs to collapse deterministically. NFKC converted non-breaking space to ordinary space, but the regular expression excluded ordinary spaces, producing repeated spaces and failing `test_whitespace_is_canonicalized`.

Repair: canonicalization now uses `re.compile(r"\s+")`, so ordinary and Unicode whitespace runs collapse to one space.

### 2. Dependency-envelope parsing

The verifier parsed the dependency list with string slicing and line splitting. The checked-in one-line declaration `dependencies = ["pydantic>=2.6"]` was therefore read as empty and falsely reported the approved dependency as missing.

Repair: the verifier now uses Python's standard-library `tomllib`, and two focused tests cover the one-line approved dependency and an unapproved `requests>=2` dependency.

## Commands and results

```text
python tools/verify_security_envelope.py
PASS — {"status": "pass", "findings": []}

python -m pytest -q
PASS — 11 tests passed

python -m compileall -q unicernal_search tools tests
PASS — exit code 0

python -m unicernal_search.cli sanitize <input> --output <sanitized> --audit <audit> --report <evidence> --pdf <pdf>
PASS — one flagged inert record accepted, one archive record rejected, JSON outputs parsed, content digest replayed, and PDF header/EOF verified

PyYAML safe-load plus structural assertions for .github/workflows/security-envelope.yml and .github/workflows/public-scan.yml
PASS — both workflows parsed; each has a jobs map and top-level contents: read permission

Tracked-text hidden-control scan using the workflow's forbidden-code-point set
PASS — no forbidden hidden controls in the mirrored tracked text
```

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

## Residual gates

- No GitHub Actions workflow run or commit-status check was attached to the observed source base when this task began.
- The candidate branch still requires exact-head GitHub Actions or an independent clean-checkout replay with retained logs.
- P1 contract publication and P2 independently permissioned retrieval/sanitizer jobs remain separate follow-on tasks.
- This task adds no network, credential, execution, repository-write, or autonomous decision authority.
