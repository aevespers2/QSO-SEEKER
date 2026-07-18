from qso_seeker.evolution import GenomeMutator, GenomeSelector
from qso_seeker.experiment import ExperimentPolicy, ExperimentRunner
from qso_seeker.genome import GenomeSynthesizer
from qso_seeker.ingest import HandoffValidationError, parse_handoff
from qso_seeker.manifest import GenomeManifest
from qso_seeker.models import SpawnPolicy


def payload() -> dict:
    return {
        "objectives": ["map contradictions", "propose repairs"],
        "needs": ["provenance"],
        "curiosities": ["novel topology"],
        "scenarios": ["conflicting evidence arrives"],
        "synthetic_judgments": ["combine graph and temporal evidence"],
        "analytic_judgments": ["reject unsupported causal claims"],
        "priors": {"source_reliability": 0.6},
        "evidence": [{
            "content": "sample",
            "kind": "observation",
            "confidence": 0.8,
            "source": "fixture",
        }],
        "metadata": {"batch": "test"},
    }


def test_ingestion_rejects_unknown_fields() -> None:
    sample = payload()
    sample["unexpected"] = True
    try:
        parse_handoff(sample)
    except HandoffValidationError as exc:
        assert "unknown" in str(exc)
    else:
        raise AssertionError("expected strict ingestion failure")


def test_mutation_preserves_ethics_and_increments_version() -> None:
    genome = GenomeSynthesizer().synthesize(parse_handoff(payload()))
    mutant = GenomeMutator().mutate_weights(genome, objective_delta={"map contradictions": 0.5})
    assert mutant.version == genome.version + 1
    assert mutant.ethical_core == genome.ethical_core
    assert genome.genome_id in mutant.parent_ids


def test_selector_prefers_objective_coverage() -> None:
    genome = GenomeSynthesizer().synthesize(parse_handoff(payload()))
    mutant = GenomeMutator().mutate_weights(genome, objective_delta={"map contradictions": 1.0})
    selected = GenomeSelector().select([genome, mutant], ["map contradictions"])
    assert selected[0] == mutant


def test_manifest_round_trip() -> None:
    genome = GenomeSynthesizer().synthesize(parse_handoff(payload()))
    secret = b"0123456789abcdef0123456789abcdef"
    manifest = GenomeManifest.sign(genome, secret)
    assert GenomeManifest.verify(manifest, secret)
    manifest["genome"]["version"] = 999
    assert not GenomeManifest.verify(manifest, secret)


def test_experiment_respects_total_step_budget() -> None:
    genome = GenomeSynthesizer().synthesize(parse_handoff(payload()))
    report = ExperimentRunner().run(
        [genome],
        spawn_policy=SpawnPolicy(freeze_after_steps=100),
        experiment_policy=ExperimentPolicy(max_total_steps=5, step_batch=2),
    )
    assert report.total_steps == 5
    assert report.stopped_reason == "step_budget_exhausted"
