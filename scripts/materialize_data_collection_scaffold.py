"""Materialize the QSO-SEEKER data-collection scaffold.

Phase: collection pipeline development.
Stages: contracts, adapters, sanitization, storage, Digitalis publication, verification, release.
Tasks: validate the plan, create missing files, preserve existing work, generate unique roadmaps, and require exact-head review.
Steps: dry-run, inspect, write, diff, test, approve.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "roadmap" / "data-collection-plan.json"


def roadmap(path: Path) -> dict[str, object]:
    area = path.parent.as_posix() or "repository root"
    return {
        "file": path.as_posix(),
        "purpose": f"Address bounded data-collection responsibility {path.stem} within {area}.",
        "phase": "planned",
        "stages": ["contract", "implementation", "verification", "integration", "release"],
        "tasks": [
            "Define typed inputs, outputs, source authority, invariants, and failure behavior.",
            "Implement read-only bounded behavior with no raw payload exposure to QSOs.",
            "Add positive, negative, boundary, retry, replay, privacy, and tamper tests.",
            "Connect content addressing, provenance, retention, and Digitalis publication.",
            "Document compatibility, rollback, operations, and human-review evidence."
        ],
        "steps": [
            "Review source, privacy, and field contracts.",
            "Implement or document the collection responsibility.",
            "Add fail-closed schemas and fixtures.",
            "Run dry-run collection and provenance replay.",
            "Record exact-head CI and human acceptance evidence."
        ],
        "status": "scaffold"
    }


def render(path: Path) -> str:
    item = roadmap(path)
    suffix = path.suffix.lower()
    body = "\n".join([
        f"Roadmap: {item['file']}",
        f"Purpose: {item['purpose']}",
        f"Phase: {item['phase']}",
        "Stages: contract -> implementation -> verification -> integration -> release",
        "Tasks:",
        *[f"- {task}" for task in item["tasks"]],
        "Steps:",
        *[f"{index}. {step}" for index, step in enumerate(item["steps"], 1)],
    ])
    if suffix == ".json":
        return json.dumps({"roadmap": item}, indent=2) + "\n"
    if suffix == ".py":
        return f'"""\n{body}\n"""\n\nfrom __future__ import annotations\n\n# TODO: replace scaffold with tested implementation.\n'
    if suffix in {".yml", ".yaml", ".toml"}:
        return "# " + body.replace("\n", "\n# ") + "\n"
    return f"# {path.stem.replace('-', ' ').title()}\n\n{body}\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    for folder, names in plan["groups"].items():
        for name in names:
            relative = Path(folder) / name
            target = ROOT / relative
            print(("replace" if target.exists() else "create") + ": " + relative.as_posix())
            if not args.write or (target.exists() and not args.force):
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(relative), encoding="utf-8")


if __name__ == "__main__":
    main()
