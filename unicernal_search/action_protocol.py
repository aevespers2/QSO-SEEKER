from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


VALID_STATES = {"PROPOSED", "READY", "IN_PROGRESS", "BLOCKED", "REVIEW", "DONE"}
TERMINAL_OUTCOMES = {"completed", "blocked", "decision_required"}


class ActionProtocolError(ValueError):
    """Raised when an action chain violates the fail-closed protocol."""


@dataclass(frozen=True)
class ActionItem:
    action_id: str
    priority: int
    owner: str
    state: str
    depends_on: tuple[str, ...]
    description: str

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "ActionItem":
        required = {"id", "priority", "owner", "state", "depends_on", "description"}
        missing = required - value.keys()
        if missing:
            raise ActionProtocolError(f"missing action fields: {sorted(missing)}")
        state = str(value["state"])
        if state not in VALID_STATES:
            raise ActionProtocolError(f"invalid action state: {state}")
        priority = value["priority"]
        if not isinstance(priority, int) or priority < 0:
            raise ActionProtocolError("priority must be a non-negative integer")
        dependencies = value["depends_on"]
        if not isinstance(dependencies, list) or not all(isinstance(item, str) for item in dependencies):
            raise ActionProtocolError("depends_on must be a list of action ids")
        return cls(
            action_id=str(value["id"]),
            priority=priority,
            owner=str(value["owner"]),
            state=state,
            depends_on=tuple(dependencies),
            description=str(value["description"]),
        )


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def action_chain_digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def load_action_chain(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ActionProtocolError("action chain must be a JSON object")
    if value.get("protocol") != "QSO-SEEKER-ACTION-PROTOCOL-v1":
        raise ActionProtocolError("unsupported action protocol")
    actions = value.get("actions")
    if not isinstance(actions, list):
        raise ActionProtocolError("actions must be a list")
    parsed = [ActionItem.from_mapping(item) for item in actions]
    identifiers = [item.action_id for item in parsed]
    if len(identifiers) != len(set(identifiers)):
        raise ActionProtocolError("duplicate action id")
    known = set(identifiers)
    for item in parsed:
        unknown = set(item.depends_on) - known
        if unknown:
            raise ActionProtocolError(f"unknown dependency for {item.action_id}: {sorted(unknown)}")
        if item.action_id in item.depends_on:
            raise ActionProtocolError(f"self dependency for {item.action_id}")
    return value


def select_action(actions: Iterable[ActionItem], actor: str) -> ActionItem | None:
    items = list(actions)
    by_id = {item.action_id: item for item in items}
    candidates = []
    for item in items:
        if item.owner not in {actor, "Builder", "QSOBuilder"}:
            continue
        if item.state != "READY":
            continue
        if any(by_id[dependency].state != "DONE" for dependency in item.depends_on):
            continue
        candidates.append(item)
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: (item.priority, item.action_id))[0]


def build_claim(chain: dict[str, Any], actor: str, head_sha: str, max_steps: int, max_files: int) -> dict[str, Any]:
    if len(head_sha) != 40 or any(character not in "0123456789abcdef" for character in head_sha.lower()):
        raise ActionProtocolError("head_sha must be a full hexadecimal commit id")
    if max_steps != 1:
        raise ActionProtocolError("bounded execution requires exactly one implementation step")
    if max_files < 1 or max_files > 8:
        raise ActionProtocolError("max_files must be between 1 and 8")
    actions = [ActionItem.from_mapping(item) for item in chain["actions"]]
    selected = select_action(actions, actor)
    payload: dict[str, Any] = {
        "protocol": chain["protocol"],
        "chain_sha256": action_chain_digest(chain),
        "head_sha": head_sha.lower(),
        "actor": actor,
        "budget": {"implementation_steps": max_steps, "files": max_files},
        "selected": None,
    }
    if selected is not None:
        payload["selected"] = {
            "id": selected.action_id,
            "priority": selected.priority,
            "description": selected.description,
            "transition": ["READY", "IN_PROGRESS"],
        }
    payload["claim_sha256"] = action_chain_digest(payload)
    return payload


def validate_progress(progress: dict[str, Any]) -> None:
    outcome = progress.get("outcome")
    if outcome not in TERMINAL_OUTCOMES | {"in_progress"}:
        raise ActionProtocolError("invalid progress outcome")
    changed_files = progress.get("changed_files", [])
    if not isinstance(changed_files, list) or not all(isinstance(path, str) for path in changed_files):
        raise ActionProtocolError("changed_files must be a list of paths")
    budget = progress.get("budget", {})
    if len(changed_files) > budget.get("files", 0):
        raise ActionProtocolError("file budget exceeded")
    evidence = progress.get("evidence", [])
    if outcome == "completed" and not evidence:
        raise ActionProtocolError("completed work requires evidence")
    if outcome == "blocked" and not progress.get("blocker"):
        raise ActionProtocolError("blocked work requires a blocker")
    if outcome == "decision_required" and not progress.get("decision"):
        raise ActionProtocolError("decision-required work requires a decision record")


def notification_required(progress: dict[str, Any]) -> bool:
    validate_progress(progress)
    return progress["outcome"] in TERMINAL_OUTCOMES


def plan_command(args: argparse.Namespace) -> int:
    chain = load_action_chain(args.chain)
    claim = build_claim(chain, args.actor, args.head_sha, args.max_steps, args.max_files)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(claim, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if claim["selected"] is not None else 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic fail-closed QSO-SEEKER action planner")
    parser.add_argument("chain", type=Path)
    parser.add_argument("--actor", default="QSOBuilder")
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--max-steps", type=int, default=1)
    parser.add_argument("--max-files", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    parser.set_defaults(func=plan_command)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
