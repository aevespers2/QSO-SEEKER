# Source review record

## Status and purpose

Status: `DOCUMENTED_NOT_AUTHORIZED`

This guide defines a machine-readable, documentation-only record for checking whether a requested source operation matches a reviewed purpose, consumer, privacy class, validity window, and authority boundary. The record and validator are review aids. They do not grant retrieval, processing, retention, handoff, publication, credential, network, or repository-write authority.

The record exists to make contradictions visible before any separately authorized source route is considered. It complements the [source rights and privacy review](source-rights-and-privacy-review.md); it does not replace legal, privacy, security, retention, publication, or human review.

## Bounded artifact set

The documentation milestone contains three mutually checked artifacts:

1. `docs/examples/source-review-record-v1.json` — a synthetic fixture with no private locator or real personal data;
2. `scripts/validate_source_review_record.py` — a standard-library-only, side-effect-free validator;
3. `tests/test_source_review_record.py` — hostile contradiction tests.

The fixture deliberately remains `REVIEW_REQUIRED`. Every authority flag is false, its maximum retention is zero days, and its uncertainty field states that no source-specific permission exists.

## Record structure

| Section | Purpose | Required safety property |
|---|---|---|
| `schema`, `version`, `status` | Bind the record vocabulary and non-authorizing state | Must equal `qso-seeker.source-review-record`, version `1`, and `DOCUMENTED_NOT_AUTHORIZED` |
| `source` | Describe source class, locator policy, terms snapshot, and license reference | Must contain no private locator and must bind a lowercase SHA-256 terms digest |
| `request` | State the bounded purpose, consumer, operation, requested privacy class, and publication request | Must use a supported operation and explicit privacy class |
| `decision` | Record state, reviewed scope, consumers, operations, privacy floor, validity, and human roles | Request and decision scope must agree; inactive decisions cannot retain permissions |
| `retention` | Bound retention and identify deletion and legal-hold roles | Duration must be explicit and non-negative |
| `authority` | Prevent documentation from becoming operational permission | Every authority flag in the synthetic fixture must remain `false` |
| `provenance` | Bind source, decision evidence, and policy references | Digests must be lowercase SHA-256 values |
| `supersession` | Preserve correction and replacement relationships | Historical records are linked rather than silently overwritten |
| `uncertainty` and `fail_closed_condition` | State limitations and the condition keeping the route closed | Both must be explicit and non-empty |

## Fail-closed consistency rules

The validator rejects a record when any of these conditions occurs:

- the requested purpose differs from the approved purpose;
- the requested consumer is absent from the reviewed consumer set;
- the requested operation is not approved by an active decision;
- the output privacy class would be less restrictive than the requested privacy floor;
- publication is requested without explicit publication approval;
- publication is marked approved without `publish` in the allowed operations;
- `REVIEW_REQUIRED`, `BLOCKED`, `WITHDRAWN`, `EXPIRED`, `SUPERSEDED`, or `PUBLICATION_REVIEW_REQUIRED` retains an allowed operation;
- a withdrawn, expired, or superseded record retains a consumer;
- withdrawal state and withdrawal time disagree;
- a current-time check finds an expired record that is not marked `EXPIRED`, or a prematurely expired record;
- an unknown field, unsupported state, malformed timestamp, invalid digest, duplicate list value, private locator, or authority-bearing flag appears.

These checks test record coherence only. A coherent record is not proof that the underlying facts, terms, identity, source, decision owner, or legal interpretation are valid.

## Hostile fixture coverage

The focused regression suite exercises:

- a valid synthetic documentation fixture;
- expired evidence without an `EXPIRED` state;
- a withdrawal timestamp attached to a non-withdrawn decision;
- wrong-purpose substitution;
- wrong-consumer substitution;
- privacy-class downgrade;
- publication without approval;
- attempted network-authority gain;
- an inactive decision that still permits sanitization.

Future fixtures should add wrong terms version, corrected or superseded source evidence, legal hold, consumer withdrawal acknowledgment, malformed source identity, stale reviewer role, and independently reproduced cross-language validation. Those additions require their own bounded proposal and must not activate a source route.

## Review sequence

A reviewer using this documentation should:

1. read the source-rights and privacy guide and identify the unresolved decision owners;
2. inspect the synthetic fixture and confirm that it contains no private locator, credentials, real personal data, or authority-bearing value;
3. run the validator against the fixture;
4. run the hostile regression suite;
5. inspect the exact workflow source, submitted commit, toolchain, logs, hashes, and retained artifact;
6. confirm that a passing record is described only as structurally coherent and documentation-only;
7. reject any attempt to use this fixture as permission for retrieval, processing, retention, handoff, publication, credentials, network access, or repository mutation.

## Local validation

```bash
python scripts/validate_source_review_record.py \
  docs/examples/source-review-record-v1.json \
  --now 2026-07-24T00:00:00+00:00

python -m unittest -v tests.test_source_review_record
mkdocs build --strict
```

The exact-head workflow runs these checks independently, records their outcomes even on failure, retains the rendered documentation and deterministic hashes, and fails only after evidence has been uploaded.

## Accessibility and comprehension

The record uses explicit text states and does not rely on color. Field names are described in the table above, validation failures use stable plain-language reason tokens, and the synthetic fixture is available as readable JSON. Any future rendered review interface must be assessed for keyboard operation, visible focus, zoom and reflow, screen-reader interpretation, cognitive clarity, non-color status communication, and understandable error recovery on the exact artifact.

## FYSA-120 capability map

This bounded improvement applies:

- `009-B`, `009-D`, and `009-E` — benchmark selection, error classification, repair verification, non-deceptive reporting, evaluation provenance, and calibration;
- `012-A`, `012-B`, `012-D`, and `012-E` — information architecture, requirements writing, documentation testing, terminology control, and lifecycle synchronization;
- `017-C`, `017-D`, and `017-E` — decision and artifact provenance, substitution detection, audit packaging, hashing, supersession, and correction propagation;
- `018-B` and `018-E` — record classification, responsibility mapping, retention, access governance, and contested-history preservation;
- `022-A`, `022-C`, `022-D`, and `022-E` — environment capture, deterministic workflows, independent reruns, failure diagnosis, and artifact preservation;
- `031-A`, `031-D`, and `031-E` — invariant definition, hostile integration testing, regression prevention, and assurance maintenance;
- `033-A` and `033-E` — purpose limitation, minimization, linkability controls, retention governance, consent provenance, and privacy assurance.

Refined non-authoritative subdivision: **`018-F — Source-rights, privacy, and publication-disposition records`**, extended to include machine-readable review-state contradiction testing and request-to-decision scope binding. Taxonomy membership records the intended capability area; it is not evidence that a legal, privacy, security, or publication decision has been competently made.

## Approval and rollback boundary

The files may support documentation and test review immediately. They do not implement a source registry, policy engine, durable review store, deletion service, legal-hold mechanism, credential handler, retrieval adapter, consumer route, or publication workflow.

Rollback is ordinary branch or commit reversion. If the fixture, validator, documentation, or tests conflict with an accepted future contract, preserve the current exact-head artifact as historical evidence, withdraw the unsupported record version, restore the last accepted documentation generation, and require fresh exact-head validation before making any replacement claim.
