# Obstruction and gluing analysis

## Purpose

QSO-SEEKER sits at the boundary between untrusted external material and the rest of A.L.I.S.T.A.I.R.E. Its value depends not only on producing locally valid records, but on those records gluing consistently to retrieval jobs, policy decisions, temporal validation, canonical state, runtime consumers, review interfaces, and correction or revocation flows.

This document treats repositories and services as local sections of a larger system. Contract edges are the gluing maps. Deterministic fixtures, immutable receipts, and replayable evidence are the witnesses that two or more sections agree on their overlap. This is an engineering method inspired by obstruction and homology language; it is not a claim that a completed formal homology computation has been performed.

## Current local section

The accepted QSO-SEEKER section contains:

- inert local hostile-input sanitization;
- fail-closed raw-input validation and stable rejection reasons;
- canonical-record and attribution-sidecar contract version 1;
- deterministic canonical JSON and SHA-256 identities;
- repository-wide consent-capacity controls;
- exact-head workflow evidence for accepted contract and consent candidates.

The following remain proposals or incomplete candidates:

- independently permissioned retrieval and sanitizer jobs;
- live, scheduled, authenticated, or private-source collection;
- publication into a shared field;
- QSO spawning and genome generation;
- QSIO runtime integration;
- automatic downstream consumption or truth promotion.

## Active obstructions

| ID | Obstruction | Affected overlap | Failure mode | Lowest-coupling repair candidate |
|---|---|---|---|---|
| SEEK-O01 | Retrieval and sanitization are conceptually separated but not yet proven as independently permissioned jobs | collector ↔ sanitizer | Credentials, network authority, or repository-write authority may remain reachable from the sanitizer path | Artifact-only handoff with independent jobs, exact digest verification, minimum permissions, and negative capability tests |
| SEEK-O02 | Basic sanitizer records and canonical-record v1 are related but distinct | sanitizer ↔ canonical producer | Consumers may treat incomplete local output as a fully attributed canonical record | Keep a named producer step that constructs v1 records and require independent contract validation |
| SEEK-O03 | Canonical record identity does not by itself establish observation freshness or replay domain | Seeker ↔ temporal validator ↔ consumer | Old but valid records may be replayed as current observations | Add a separately versioned observation envelope owned outside canonical-record v1, with clock, freshness, replay, and subject identity rules |
| SEEK-O04 | `repository`, `path`, and `source_url` identify source location but not a stable observed subject | Seeker ↔ device/data subject owners | Records from renamed, mirrored, forked, or replaced subjects may be misbound | Define an external subject-identity reference and preserve source locator as evidence rather than authority |
| SEEK-O05 | Attribution sidecars can change independently, but correction, supersession, and revocation semantics are not portfolio-wide | Seeker ↔ Bridge ↔ Studio/AionUi | Corrected licensing or provenance may not invalidate caches or downstream displays | Version correction and revocation events with affected record IDs, reason codes, effective time, and propagation receipts |
| SEEK-O06 | QSO-SEEKER, QSO-DIGITALIS, Bridge, and Repository `1` have overlapping claims around evidence validation and canonical handoff | Seeker ↔ Digitalis ↔ Bridge ↔ Repository `1` | Multiple components may each claim canonicalization, validation, or publication authority | Assign Seeker source sanitization, Digitalis evidence interpretation, Bridge transport/packaging, and Repository `1` canonical disposition explicitly |
| SEEK-O07 | Draft QSIO integration maps Seeker fields into runtime concepts without an accepted canonical owner for shared QSO envelopes | Seeker ↔ qsio-kernel ↔ QuantumStateObjects ↔ QSO-GENOMES | Identity, evidence, confidence, mutation, and policy fields may diverge across schemas | Pin a shared contract owner and require producer/consumer fixtures before enabling the adapter |
| SEEK-O08 | Experimental spawning overlaps QSO-GENOMES and QSO-FABRIC responsibilities | Seeker ↔ Genomes ↔ Fabric | Retrieval code may silently become a genome authority or runtime orchestrator | Keep spawning experimental and isolated; move accepted genome contracts to QSO-GENOMES and orchestration to Fabric |
| SEEK-O09 | Open collection candidates disagree on public core, private overlay, live checkpoint, and source-registry authority | public repo ↔ private deployment | Public documentation may imply support for credentials or sources that are deployment-specific | Define a public adapter contract and a private deployment manifest that never enters public artifacts |
| SEEK-O10 | Source terms, privacy, retention, and licensing are not represented as machine-checkable policy decisions | collector ↔ legal/privacy review ↔ publisher | Technically valid artifacts may be stored or published without permitted purpose or duration | Add policy-decision receipts outside content records and fail closed when absent or expired |
| SEEK-O11 | Hash determinism is specified locally, but cross-language canonicalization witnesses are absent | Python producer ↔ non-Python consumer | Different Unicode, number, or JSON implementations may calculate different identities | Publish language-neutral byte fixtures and independent implementations or validators |
| SEEK-O12 | The contract carries `collected_at` but does not define trusted clock source, uncertainty, or ordering semantics | collector ↔ temporal invariants | Comparisons may assume a trustworthy total order that does not exist | Delegate temporal semantics to the temporal-invariants contract and preserve clock provenance and uncertainty |
| SEEK-O13 | Security Envelope, consent lock, and documentation checks prove different properties on potentially different heads | source ↔ evidence bundle ↔ release | A release may combine individually passing but compositionally stale evidence | Require one immutable release head with all mandatory checks and one manifest binding every artifact |
| SEEK-O14 | Downstream interfaces may display confidence or flags as authoritative truth | Seeker ↔ Studio/AionUi ↔ user | Sanitization or evidence scores may be mistaken for adjudication or verified fact | Require status vocabulary that preserves `observed`, `sanitized`, `unverified`, `rejected`, and `unknown` distinctions |
| SEEK-O15 | Emergency freeze, revocation, rollback, and cache invalidation are not defined end to end | incident authority ↔ Seeker ↔ Bridge ↔ consumers | Known-bad records may remain available after local quarantine | Define portfolio-wide freeze and revocation propagation with preservation, bounded restart, and recovery witnesses |
| SEEK-O16 | Path and URL validation do not solve fork, mirror, redirect, or source-history discontinuity | source registry ↔ canonical record | Provenance can remain syntactically valid while pointing at a different history | Bind source revision or immutable content locator where available and record redirect/mirror lineage separately |
| SEEK-O17 | Rejection reports may contain sensitive source fragments or operational metadata | sanitizer ↔ evidence store | Failures can leak private data even when accepted records are inert | Define redaction tiers, retention limits, access classes, and safe representative fixtures |
| SEEK-O18 | No portfolio owner is designated for reason-code vocabulary and compatibility | Seeker ↔ policy ↔ interfaces | Consumers may collapse distinct security, schema, legal, and temporal failures | Establish a namespaced reason-code registry with repository ownership and version negotiation |

## Pairwise gluing matrix

| Edge | Producer responsibility | Consumer responsibility | Required witness |
|---|---|---|---|
| retrieval job → sanitizer | Emit bounded bytes, metadata, declared digest, source-policy reference, and no executable interpretation | Verify digest before parsing; run without source credentials, network, or repository-write authority | Valid handoff, digest mismatch, missing artifact, oversize, truncation, and permission-denial fixtures |
| sanitizer → canonical producer | Emit inert accepted/rejected local result with transformations and flags | Construct complete v1 provenance and identities without inventing missing source facts | Accepted, rejected, Unicode, mutation, and missing-provenance fixtures |
| canonical producer → temporal validator | Emit immutable canonical record and sidecar | Add subject, clock, freshness, replay, and ordering interpretation without rewriting content identity | Current, stale, replay, uncertain-clock, and wrong-subject fixtures |
| canonical producer → Bridge | Emit validated artifacts plus version identifiers and hashes | Preserve exact bytes and identities during authorized packaging or transport | Byte-preservation, unsupported-version, truncation, reorder, and duplicate fixtures |
| Bridge → Repository `1` | Deliver authenticated proposal/evidence envelope | Decide quarantine admission, policy, capability, canonical disposition, correction, or revocation | Accepted, rejected, stale, replay, expected-head, and partial-failure fixtures |
| Repository `1` → Studio/AionUi | Emit canonical decision and evidence references | Display status without creating new authority or hiding uncertainty | Approved, rejected, revoked, corrected, unknown, and unavailable fixtures |
| canonical record → QuantumStateObjects | Provide inert evidence only | Validate contract and apply runtime-specific policy; never treat content as executable authority | Unsupported contract, invalid hash, unverified claim, and policy-denial fixtures |
| canonical record → QSO-GENOMES | Provide attributed evidence candidate | Prevent evidence from silently mutating immutable identity or policy genomes | Evidence-only, proposed mutation, denied mutation, and approved migration fixtures |

## Required triple-overlap witnesses

Pairwise tests are insufficient when three components must agree simultaneously.

### Retrieval → sanitizer → canonical producer

The same artifact digest, byte count, source-policy reference, and rejection outcome must be observed across all three sections. A producer must not create a canonical record from an artifact the sanitizer rejected or never verified.

### Seeker → temporal invariants → Repository `1`

Record identity must remain stable while temporal validity, subject binding, freshness, replay, and policy disposition are evaluated. Repository `1` must not rewrite the Seeker record to encode a later decision.

### Seeker → Bridge → Studio/AionUi

Transport and presentation must preserve contract version, record ID, sidecar hash, decision status, uncertainty, correction state, and revocation state. A display success is not evidence of canonical acceptance.

### Seeker → QSO-GENOMES → QuantumStateObjects

Evidence may inform a proposed genome or runtime state, but the same evidence cannot be promoted to immutable identity, verified belief, or executable policy without the genome and runtime owners applying their own accepted contracts.

### Incident authority → Repository `1` → downstream caches

A freeze or revocation must propagate to Seeker ingestion, canonical disposition, Bridge transport, interfaces, and runtime caches while preserving evidence. Recovery requires an explicit bounded restart sequence and no automatic unlock.

### Public core → private overlay → release evidence

Public code, private deployment configuration, and release evidence must agree on adapter version, allowed source classes, policy identity, permissions, and retention without disclosing credentials or private locators.

## Candidate ownership split

The lowest-overlap working model is:

- **QSO-SEEKER:** source-facing retrieval adapters, hostile-input sanitization, canonical-record v1 construction, attribution sidecars, and local rejection evidence;
- **datarepo-temporal-invariants:** subject, clock, freshness, replay, ordering, and temporal-validity interpretation;
- **QSO-DIGITALIS:** domain-specific evidence interpretation and synthesis proposals, not source sanitization or canonical authority;
- **Bridge:** version-preserving transport and evidence packaging, not independent truth or capability authority;
- **Repository `1`:** quarantine admission, policy disposition, capability, canonical-state, correction, revocation, and recovery receipts;
- **QSO-STUDIO / AionUi:** human review and presentation without implicit approval authority;
- **QSO-GENOMES:** immutable identity, lineage, traits, and policy-genome contracts;
- **QuantumStateObjects / QSO-FABRIC:** bounded runtime and multi-QSO orchestration after independent validation;
- **qsio-kernel:** shared low-level semantics only after ownership and conformance are accepted.

This split is a documentation proposal. It does not activate any adapter, credential, network route, runtime, publication path, or canonical-state authority.

## Release-blocking gluing criteria

QSO-SEEKER should not be presented as a portfolio-ready source boundary until:

1. P2 artifact-only isolation is implemented and independently evidenced;
2. canonical-record v1 has language-neutral fixtures and at least one independent consumer witness;
3. subject, time, freshness, replay, correction, and revocation envelopes are assigned to accepted owners;
4. Seeker, Digitalis, Bridge, and Repository `1` responsibilities are non-overlapping and versioned;
5. private-overlay, policy, legal, privacy, licensing, retention, and redaction rules are approved;
6. triple-overlap fixtures pass against immutable commits;
7. one release manifest binds exact source, workflows, artifacts, checksums, approvals, and rollback evidence;
8. emergency freeze, evidence preservation, revocation propagation, cache invalidation, and bounded recovery are exercised.

## Architectural clarification required

Formal approval remains required for:

- the owner of the cross-repository observation/evidence envelope;
- stable subject identity and source-lineage semantics;
- temporal and replay contract ownership;
- the exact Seeker → Digitalis → Bridge → Repository `1` route;
- canonical reason-code, correction, and revocation vocabularies;
- public/private deployment boundaries and policy-receipt ownership;
- privacy, retention, licensing, incident, emergency-stop, recovery, and publication owners;
- disposition of the broader collection, live checkpoint, spawning, action-protocol, and QSIO draft candidates.
