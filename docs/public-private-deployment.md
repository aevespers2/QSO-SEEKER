# Public Core and Private Deployment Boundary

## Objective
QSO-SEEKER should remain broadly useful: the collection framework, adapter interfaces, schemas, validation routines, fixture datasets, deterministic dry runs, Digital Consciousness Field contracts, and security tests may remain public and reusable.

Only deployment-specific sensitive material should be private.

## Public assets
- Adapter interfaces and reference adapters for public, unauthenticated sources.
- Source-registry schemas and non-sensitive example registries.
- Sanitization, canonicalization, hashing, deduplication, provenance, and rejection logic.
- Fixture-based collection workflows and deterministic replay evidence.
- Digital Consciousness Field envelope and capability contracts.
- Tests, threat models, compatibility fixtures, and implementation documentation.
- Aggregated performance and quality findings that disclose no sensitive source data.

## Private assets
- Credentials, tokens, cookies, private keys, and authenticated session material.
- Private or proprietary source locators.
- Personal, medical, legal, biometric, financial, or otherwise sensitive records.
- Unpublished research corpora and restricted-license material.
- Live collection outputs whose disclosure is not explicitly authorized.
- Deployment-specific allowlists, retention exceptions, and reviewer identities.

## Deployment model
1. Fork or consume the public QSO-SEEKER core.
2. Supply a deployment registry from a private repository, secret store, encrypted object, or protected GitHub environment.
3. Run the same public validators against that private registry.
4. Store raw retrieval artifacts only in the private deployment boundary.
5. Publish only sanitized, policy-approved canonical records or aggregate metadata into the Digital Consciousness Field.
6. Preserve content hashes and provenance links without exposing private source locators to unauthorized subscribers.

## Community benefit
Public improvements to adapters, validators, schemas, safety tests, and field contracts can be contributed upstream. Private deployments benefit from those improvements without disclosing their sources or data, while public-source deployments may share canonical records when licensing and policy permit.

## Safety rule
Repository visibility is not itself the security boundary. Secrets and sensitive data must never be committed, even to a private repository, when a protected secret store or encrypted deployment artifact is available.
