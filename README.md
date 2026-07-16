# QSO-SEEKER

A deliberately non-executing search and ingestion layer for bounded QSO experiments.

## Documentation

- [Project guide and release boundaries](docs/index.md)
- [Security architecture and handoff contract](docs/security-architecture.md)
- [Task chain](taskchain.md)
- [Release plan](release.md)
- [Changelog](changelog.md)

## Security model

The gateway treats every repository response as hostile data.

It:
- accepts only JSON input produced by an external fetch adapter
- validates every record against a strict schema
- strips Unicode control and bidirectional override characters
- rejects NUL bytes, oversized fields, binary-looking payloads, and executable file types
- removes HTML/script blocks and Markdown command-link schemes
- detects common code-execution and prompt-injection patterns
- never imports, evaluates, shells out to, compiles, or executes fetched content
- emits canonical JSON records with SHA-256 content hashes
- records every rejection and transformation

The gateway does **not** claim that sanitization makes arbitrary code safe. Its output remains untrusted text and must never be executed by a QSO.

## Input format

```json
[
  {
    "repository": "owner/repo",
    "path": "README.md",
    "url": "https://example.invalid/owner/repo/README.md",
    "content": "Plain text retrieved by a separate read-only adapter"
  }
]
```

## Run

```bash
python -m unicernal_search.cli input.json --output sanitized.json --audit audit.json
```

## Recommended deployment boundary

The network-enabled fetcher should be a separate process or microVM. It passes bounded JSON records to this gateway. QSOs receive only the gateway's canonical output, never raw network responses, archives, Git objects, package files, or repository credentials.

The current public-scan workflow may still perform retrieval and sanitization within one job. Until separately permissioned jobs and a verified artifact handoff are implemented, documentation must describe the separation as logical rather than process or microVM isolation.
