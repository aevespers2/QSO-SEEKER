import json

from experimental.qso_spawn import Handoff, Ledger, Manifest, Registry, SpawnPolicy, run_batch, synthesize


def record() -> dict:
    return {
        "objectives": ["map contradictions", "propose repairs"],
        "needs": ["provenance"],
        "curiosities": ["novel topology"],
        "scenarios": ["conflicting evidence arrives"],
        "synthetic_judgments": ["combine graph and temporal evidence"],
        "analytic_judgments": ["reject unsupported causal claims"],
        "priors": {"source_reliability": 0.6},
        "evidence": [{"kind": "observation", "content": "fixture"}],
    }


def test_genome_is_deterministic() -> None:
    handoff = Handoff.parse(record())
    assert synthesize(handoff).genome_id == synthesize(handoff).genome_id


def test_strict_handoff_rejects_unknown_fields() -> None:
    payload = record()
    payload["unexpected"] = True
    try:
        Handoff.parse(payload)
    except ValueError as exc:
        assert "unknown" in str(exc)
    else:
        raise AssertionError("expected strict validation failure")


def test_registry_freezes_at_step_limit() -> None:
    genome = synthesize(Handoff.parse(record()))
    registry = Registry()
    qso = registry.spawn(genome, SpawnPolicy(max_steps=3))
    registry.step(qso.qso_id, 2)
    assert qso.state == "active"
    registry.step(qso.qso_id, 1)
    assert qso.state == "frozen"


def test_manifest_detects_tampering() -> None:
    secret = b"0123456789abcdef0123456789abcdef"
    manifest = Manifest.sign(synthesize(Handoff.parse(record())), secret)
    assert Manifest.verify(manifest, secret)
    manifest["genome"]["version"] = 99
    assert not Manifest.verify(manifest, secret)


def test_batch_records_ledger(tmp_path) -> None:
    secret = b"0123456789abcdef0123456789abcdef"
    ledger = Ledger(tmp_path / "events.jsonl")
    result = run_batch([record()], secret=secret, ledger=ledger)
    assert result["population"] == 1
    rows = [json.loads(line) for line in (tmp_path / "events.jsonl").read_text().splitlines()]
    assert rows[0]["event_type"] == "handoff_collected"
    assert rows[0]["previous_hash"] == "0" * 64
