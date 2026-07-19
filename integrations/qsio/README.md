# QSIO Integration — QSO-SEEKER

Status: Phase 1–3 scaffold, disabled by default.

## Domain mapping

| Local concept | QSIO concept |
|---|---|
| seeker / observer identity | QSO |
| observation, curiosity, or hypothesis proposal | QSI |
| accepted immutable observation record | QSIO |
| observed relationship | Nexis |
| curiosity / objective | Telion |
| evidence and observation history | Memora |
| publishable observation state | Lumen |
| protected evidence commitment | Umbra commitment |
| validation result | Witness record |

Enable with `QSIO_INTEGRATION_ENABLED=true` only after compatibility, replay, and tamper tests pass. Evidence collection, network access, model execution, and tool use remain capability-gated. Hypotheses default to `unverified` and cannot become verified truth without an accepted witnessed QSIO record.

## Rollback

Disable the feature flag, stop QSI submission, retain immutable records, and reconstruct local projections from the last accepted replay checkpoint. Existing observation and curiosity terminology remains available as migration aliases.

## Unsupported

Kernel Canon decisions, Quietus authority, signing-key custody, authoritative persistence, and any inference of sentience or consciousness are outside this adapter.
