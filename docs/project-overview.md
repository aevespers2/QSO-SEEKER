# Project overview

## Purpose

QSO-SEEKER provides a deliberately non-executing ingestion boundary for bounded QSO research. Its job is not to decide whether untrusted material is true, useful, or safe to run. Its job is to transform supported input into reviewable data with deterministic validation, sanitization, rejection, provenance, and hash evidence.

## Primary users

- Researchers preparing bounded public-source material for controlled experiments.
- Security reviewers validating hostile-input handling and least-authority boundaries.
- Tool builders consuming canonical records and attribution sidecars by explicit contract version.
- Release reviewers comparing implementation evidence with `taskchain.md`, `release.md`, and `changelog.md`.

## Inputs and outputs

### Input

The current CLI consumes a local JSON array. Every item is treated as hostile and must declare a repository identity, relative path, source URL, text content, and supported source kind. Network retrieval belongs to a separate adapter or job and is not part of the sanitizer process.

### Output

The sanitizer emits:

1. accepted inert records containing normalized text, transformations, flags, and a content hash;
2. audit entries for every accepted or rejected item;
3. an optional JSON evidence report; and
4. an optional PDF rendering of that report.

The repository also provides canonical-record and attribution-sidecar contract v1 builders and validators. Those contracts bind content, provenance, transformations, and attribution to deterministic SHA-256 identities.

## Design principles

1. **Treat all source material as hostile.** Repository content is data, never instructions.
2. **Fail closed.** Unknown fields, malformed records, unsafe paths, unsupported versions, noncanonical collections, or hash mismatches are rejected.
3. **Separate authority.** Retrieval, sanitization, validation, consumption, and publication are distinct responsibilities.
4. **Prefer reproducibility over breadth.** A bounded deterministic contract is more valuable than a broad collector with ambiguous behavior.
5. **Preserve evidence.** Decisions, transformations, rejection reasons, source identity, and hashes must remain inspectable.
6. **Document actual behavior.** Proposed isolation or collection capabilities must not be described as operational until accepted evidence exists.

## Current scope

The accepted baseline includes local schema validation, hostile-input sanitization, audit/report generation, and canonical contract validation. Canonical-record and attribution-sidecar semantics are versioned as `1` and are suitable for inert artifact handoff after independent validation.

## Non-goals

The current repository does not provide or authorize:

- general web or repository crawling;
- authenticated or private-source acquisition;
- browser automation;
- execution, compilation, import, or evaluation of fetched content;
- autonomous truth promotion or autonomous learning;
- repository writes or package publication from source content;
- an approved scheduled collection service;
- direct authority for a QSO runtime or shared-field publisher.

## Portfolio relationships

QSO-SEEKER is upstream of consumers such as QuantumStateObjects only at the contract boundary. Consumers must pin a supported contract version, validate every artifact independently, preserve attribution, and apply their own capability and policy checks. Experimental genome or spawning work is not part of the accepted sanitizer baseline merely because it appears in a separate draft branch or pull request.

## Success criteria

A release candidate is credible only when one immutable head has reproducible tests, exact-source workflow evidence, deterministic fixtures and hashes, independently permissioned handoff boundaries, accurate documentation, retained provenance, rollback evidence, and explicit human approval. Passing one test run does not itself grant operational or publication authority.
