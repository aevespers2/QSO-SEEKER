from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .collector import CollectionAdapter
from .experiment import ExperimentPolicy, ExperimentRunner
from .ledger import EventLedger
from .manifest import GenomeManifest
from .models import EthicalCore, Genome, SpawnPolicy


def _genome_from_manifest(manifest: dict) -> Genome:
    data = dict(manifest["genome"])
    data["parent_ids"] = tuple(data["parent_ids"])
    data["scenario_seeds"] = tuple(data["scenario_seeds"])
    data["synthetic_judgments"] = tuple(data["synthetic_judgments"])
    data["analytic_judgments"] = tuple(data["analytic_judgments"])
    data["ethical_core"] = EthicalCore(**data["ethical_core"])
    return Genome(**data)


def dry_run(args: argparse.Namespace) -> int:
    secret_text = os.environ.get(args.secret_env)
    if secret_text is None:
        raise SystemExit(f"missing signing secret in environment variable {args.secret_env}")
    secret = secret_text.encode("utf-8")
    if len(secret) < 32:
        raise SystemExit("signing secret must be at least 32 bytes")

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    ledger = EventLedger(output / "events.jsonl")
    adapter = CollectionAdapter(ledger)
    manifests = adapter.collect_jsonl(args.input, signing_secret=secret)
    manifest_paths = adapter.write_manifests(manifests, output / "manifests")

    genomes = []
    for manifest in manifests:
        if not GenomeManifest.verify(manifest, secret):
            raise SystemExit("generated manifest failed verification")
        genomes.append(_genome_from_manifest(manifest))

    report = ExperimentRunner().run(
        genomes,
        spawn_policy=SpawnPolicy(freeze_after_steps=args.freeze_after),
        experiment_policy=ExperimentPolicy(
            max_population=args.max_population,
            max_total_steps=args.max_steps,
            step_batch=args.step_batch,
        ),
    )
    report_payload = {
        "qso_ids": report.qso_ids,
        "total_steps": report.total_steps,
        "frozen_ids": report.frozen_ids,
        "stopped_reason": report.stopped_reason,
        "manifest_paths": [str(path) for path in manifest_paths],
        "ledger_verified": ledger.verify(),
    }
    (output / "experiment-report.json").write_text(
        json.dumps(report_payload, indent=2, sort_keys=True), encoding="utf-8"
    )
    ledger.append("dry_run_completed", report_payload)
    print(json.dumps(report_payload, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="qso-seeker")
    subparsers = parser.add_subparsers(dest="command", required=True)
    command = subparsers.add_parser("dry-run", help="ingest a JSONL handoff batch and run a bounded experiment")
    command.add_argument("--input", required=True)
    command.add_argument("--output", required=True)
    command.add_argument("--secret-env", default="QSO_SEEKER_SIGNING_SECRET")
    command.add_argument("--max-population", type=int, default=16)
    command.add_argument("--max-steps", type=int, default=1000)
    command.add_argument("--step-batch", type=int, default=1)
    command.add_argument("--freeze-after", type=int, default=100)
    command.set_defaults(handler=dry_run)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
