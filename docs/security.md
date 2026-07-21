# Security model

## Security objective

QSO-SEEKER reduces the chance that untrusted repository material crosses into a QSO experiment as executable or unaudited content. It does this by enforcing bounded schemas, rejecting unsupported material, neutralizing selected active constructs, recording transformations and flags, and requiring independent contract validation before handoff.

The system does not claim that sanitized text is safe code, true information, or harmless instructions. Output remains untrusted data.

## Threat model

The repository is designed to encounter:

- malformed or oversized JSON records;
- path traversal and unsafe source identifiers;
- NUL bytes, hidden controls, bidirectional overrides, and ANSI sequences;
- binary-looking content and executable or archive file types;
- embedded script-like, frame, object, SVG, MathML, event-handler, or dangerous-URI constructs;
- prompt-injection and code-execution phrases;
- credential-access strings;
- altered content, provenance, attribution, or hashes;
- dependency or package-discovery drift;
- misleading claims that logical separation is equivalent to verified process isolation.

## Controls

### Strict schema boundary

Raw input uses strict Pydantic models with extra fields forbidden, bounded lengths, repository-shape checks, URL parsing, source-kind constraints, and relative-path validation.

### Rejection before transformation

Executable, archive, binary-looking, and schema-invalid records are rejected and preserved as audit decisions. QSO-SEEKER does not attempt to unpack or inspect executable containers.

### Bounded neutralization

Accepted text is Unicode-normalized, selected controls are removed, HTML entities are decoded, selected active blocks and event handlers are removed, dangerous URI schemes are neutralized, and output length is bounded. These controls reduce risk but do not prove semantic safety.

### Classification without execution

Pattern detection records flags for prompt-injection, execution-request, and credential-access indicators. It does not follow or execute the text.

### Content-addressed contracts

Canonical-record v1 binds content, transformations, flags, source identity, and provenance into deterministic hashes. Attribution sidecars have independent hashes. Mutations fail validation.

### Dependency and package boundary

The package declares a small dependency surface and scopes package discovery to `unicernal_search*`. Security verification checks declared dependencies and repository content for prohibited capability drift.

### Consent-capacity policy

`QSO-CONSENT-CAPACITY-LOCK-v1` is a repository-wide fail-closed policy. Documentation changes do not weaken or bypass it, and any future feature within its scope must remain explicitly bound to that policy and separate human review.

## Capability boundaries

The sanitizer should run without:

- source credentials;
- repository-write tokens;
- shell or subprocess authority for source material;
- import or evaluation paths for source content;
- package installation driven by source text;
- direct downstream publisher authority.

A future source reader should be read-only and independently permissioned. Handoff should use a bounded artifact plus an independently verified digest.

## Residual risk

QSO-SEEKER cannot determine whether text is factually correct, legally reusable, privacy-safe, or socially harmless. Pattern lists are incomplete and can produce false positives or miss novel attacks. HTML neutralization is not a general-purpose browser sanitizer. A valid hash proves identity, not truth. A valid contract proves shape and integrity, not permission to use the record.

## Consumer obligations

Every consumer must:

1. pin and validate an explicit contract version;
2. reject unknown fields, versions, and hash mismatches;
3. treat `content` as inert data;
4. enforce its own source, licensing, privacy, retention, and capability policy;
5. preserve record and sidecar identity through storage and transformation;
6. avoid granting new authority based only on successful sanitization;
7. retain reviewable evidence for failures and exceptions.

## Reporting a security issue

Do not place secrets, private source material, or exploit payloads in public issues. Use the repository owner's private security contact or GitHub private vulnerability reporting when enabled. A report should identify the affected version or commit, input class, expected fail-closed behavior, observed behavior, reproduction steps using non-sensitive fixtures, and potential downstream impact.

## Security review checklist

- Exact submitted head identified and checked out.
- Minimum workflow permissions and no persisted checkout credentials.
- Clean installation and import smoke test.
- Dependency-envelope and package-discovery verification.
- Complete deterministic, mutation, malformed-input, and adversarial fixtures.
- Hidden-control scan.
- Canonical record and attribution hash replay.
- No source credentials or prohibited output in retained evidence.
- Rollback path tested.
- Documentation matches the implemented boundary.
- Human approval recorded after all evidence is final.
