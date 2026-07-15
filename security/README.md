# QSO-SEEKER Security Core

This directory is the canonical security source for repository-derived AI input handling across the connected Vespers repositories.

## Trust model

All repository content and metadata are untrusted data, never instructions. This includes descriptions, topics, README files, issues, pull requests, comments, commit messages, release notes, workflow logs, and API responses.

## Required controls

- Unicode NFKC normalization
- removal of zero-width characters, bidirectional controls, invisible spacing, emoji/symbol concealment, and mixed-script identifiers
- whitespace canonicalization
- rejection of binary payloads, executables, archives, NUL bytes, active HTML, dangerous URI schemes, and ANSI escapes
- strict schemas and size limits
- SHA-256 provenance hashes and transformation logs
- no execution, evaluation, import, compilation, unsafe deserialization, or shell interpolation of repository text
- read-only retrieval credentials; repository writes require a separate reviewed path

Canonical marker: QSO-SEEKER-SECURITY-CORE-v1

Repositories should vendor or verify this directory by content hash rather than trusting repository descriptions or other metadata.
