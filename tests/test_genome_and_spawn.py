from qso_seeker.genome import GenomeSynthesizer
from qso_seeker.models import EvidenceItem, SeekerHandoff, SpawnPolicy
from qso_seeker.spawn import QSOSpawner


def sample_handoff() -> SeekerHandoff:
    return SeekerHandoff(
        objectives=("map contradictions", "propose repairs"),
        needs=("provenance", "bounded autonomy"),
        curiosities=("novel topology",),
        scenarios=("conflicting evidence arrives",),
        synthetic_judgments=("combine graph and temporal evidence",),
        analytic_judgments=("reject unsupported causal claims",),
        priors={"source_reliability": 0.6},
        evidence=(EvidenceItem("sample", "observation", 0.8, "fixture"),),
    )


def test_genome_is_deterministic() -> None:
    synthesizer = GenomeSynthesizer()
    first = synthesizer.synthesize(sample_handoff())
    second = synthesizer.synthesize(sample_handoff())
    assert first.genome_id == second.genome_id
    assert first.provenance_digest == second.provenance_digest


def test_qso_freezes_at_policy_limit() -> None:
    genome = GenomeSynthesizer().synthesize(sample_handoff())
    spawner = QSOSpawner()
    qso = spawner.spawn(genome, SpawnPolicy(freeze_after_steps=3))
    spawner.step(qso.qso_id, 2)
    assert qso.state == "active"
    spawner.step(qso.qso_id, 1)
    assert qso.state == "frozen"


def test_frozen_qso_cannot_spawn_child() -> None:
    genome = GenomeSynthesizer().synthesize(sample_handoff())
    spawner = QSOSpawner()
    parent = spawner.spawn(genome, SpawnPolicy(freeze_after_steps=1))
    spawner.step(parent.qso_id)
    child_genome = GenomeSynthesizer().synthesize(sample_handoff(), version=2, parent_ids=(genome.genome_id,))
    try:
        spawner.spawn_child(parent.qso_id, child_genome)
    except RuntimeError as exc:
        assert "cannot spawn" in str(exc)
    else:
        raise AssertionError("expected frozen parent to be unable to spawn")
