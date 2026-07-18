import json

from qso_seeker.collector import CollectionAdapter
from qso_seeker.envelope import EnvelopeCodec
from qso_seeker.ledger import EventLedger


def record() -> dict:
    return {
        "objectives": ["map contradictions"],
        "needs": ["provenance"],
        "curiosities": ["novel topology"],
        "scenarios": ["conflicting evidence arrives"],
        "synthetic_judgments": ["combine evidence"],
        "analytic_judgments": ["reject unsupported causality"],
        "priors": {"source_reliability": 0.5},
        "evidence": [],
        "metadata": {},
    }


def test_ledger_detects_tampering(tmp_path) -> None:
    path = tmp_path / "events.jsonl"
    ledger = EventLedger(path)
    ledger.append("one", {"value": 1})
    ledger.append("two", {"value": 2})
    assert ledger.verify()
    rows = path.read_text(encoding="utf-8").splitlines()
    altered = json.loads(rows[0])
    altered["payload"]["value"] = 99
    rows[0] = json.dumps(altered)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    assert not ledger.verify()


def test_envelope_authentication() -> None:
    secret = b"0123456789abcdef0123456789abcdef"
    envelope = EnvelopeCodec.create(
        "qso-a", "qso-b", "hypothesis", {"claim": "x"}, secret, nonce="n-1"
    )
    assert EnvelopeCodec.verify(envelope, secret)
    assert not EnvelopeCodec.verify(envelope, b"abcdef0123456789abcdef0123456789")


def test_collection_records_provenance(tmp_path) -> None:
    ledger = EventLedger(tmp_path / "events.jsonl")
    adapter = CollectionAdapter(ledger)
    secret = b"0123456789abcdef0123456789abcdef"
    manifests = adapter.collect([record()], signing_secret=secret)
    written = adapter.write_manifests(manifests, tmp_path / "manifests")
    assert len(written) == 1
    assert written[0].exists()
    assert ledger.verify()
