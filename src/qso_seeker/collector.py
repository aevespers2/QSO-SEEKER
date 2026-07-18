from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

from .genome import GenomeSynthesizer
from .ingest import parse_handoff
from .ledger import EventLedger
from .manifest import GenomeManifest


class CollectionAdapter:
    """Convert collected JSON records into validated handoffs and manifests."""

    def __init__(self, ledger: EventLedger | None = None) -> None:
        self.ledger = ledger
        self.synthesizer = GenomeSynthesizer()

    def collect(self, records: Iterable[dict[str, Any]], *, signing_secret: bytes) -> list[dict[str, Any]]:
        manifests: list[dict[str, Any]] = []
        for index, record in enumerate(records):
            handoff = parse_handoff(record)
            genome = self.synthesizer.synthesize(handoff)
            manifest = GenomeManifest.sign(genome, signing_secret)
            manifests.append(manifest)
            if self.ledger is not None:
                self.ledger.append(
                    "handoff_collected",
                    {
                        "index": index,
                        "genome_id": genome.genome_id,
                        "provenance_digest": genome.provenance_digest,
                        "objectives": list(handoff.objectives),
                    },
                )
        return manifests

    def collect_jsonl(self, path: str | Path, *, signing_secret: bytes) -> list[dict[str, Any]]:
        source = Path(path)
        records: list[dict[str, Any]] = []
        for line_number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError(f"line {line_number} must contain a JSON object")
            records.append(payload)
        return self.collect(records, signing_secret=signing_secret)

    @staticmethod
    def write_manifests(manifests: Iterable[dict[str, Any]], directory: str | Path) -> list[Path]:
        target = Path(directory)
        target.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for manifest in manifests:
            genome_id = manifest["genome"]["genome_id"]
            path = target / f"{genome_id}.manifest.json"
            path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
            written.append(path)
        return written
