from __future__ import annotations

import json
from pathlib import Path

import pytest

from unicernal_search.action_protocol import (
    ActionItem,
    ActionProtocolError,
    action_chain_digest,
    build_claim,
    load_action_chain,
    notification_required,
    select_action,
    validate_progress,
)


HEAD = "a" * 40


def _chain() -> dict:
    return {
        "protocol": "QSO-SEEKER-ACTION-PROTOCOL-v1",
        "actions": [
            {
                "id": "P0",
                "priority": 0,
                "owner": "Architect",
                "state": "DONE",
                "depends_on": [],
                "description": "architect disposition",
            },
            {
                "id": "P1-B",
                "priority": 1,
                "owner": "QSOBuilder",
                "state": "READY",
                "depends_on": ["P0"],
                "description": "second lexical candidate",
            },
            {
                "id": "P1-A",
                "priority": 1,
                "owner": "QSOBuilder",
                "state": "READY",
                "depends_on": ["P0"],
                "description": "first lexical candidate",
            },
            {
                "id": "P2",
                "priority": 2,
                "owner": "QSOBuilder",
                "state": "READY",
                "depends_on": ["P1-A"],
                "description": "blocked dependency",
            },
        ],
    }


def test_selects_highest_priority_unblocked_with_stable_tie_break() -> None:
    actions = [ActionItem.from_mapping(item) for item in _chain()["actions"]]
    selected = select_action(actions, "QSOBuilder")
    assert selected is not None
    assert selected.action_id == "P1-A"


def test_claim_binds_chain_head_actor_and_budget() -> None:
    chain = _chain()
    claim = build_claim(chain, "QSOBuilder", HEAD, 1, 4)
    assert claim["chain_sha256"] == action_chain_digest(chain)
    assert claim["head_sha"] == HEAD
    assert claim["selected"]["id"] == "P1-A"
    assert len(claim["claim_sha256"]) == 64


def test_claim_fails_closed_on_unbounded_work() -> None:
    with pytest.raises(ActionProtocolError, match="exactly one"):
        build_claim(_chain(), "QSOBuilder", HEAD, 2, 4)
    with pytest.raises(ActionProtocolError, match="between 1 and 8"):
        build_claim(_chain(), "QSOBuilder", HEAD, 1, 9)


def test_completed_progress_requires_evidence_and_budget_compliance() -> None:
    progress = {
        "outcome": "completed",
        "budget": {"files": 2},
        "changed_files": ["a.py"],
        "evidence": ["pytest: pass"],
    }
    validate_progress(progress)
    assert notification_required(progress) is True
    with pytest.raises(ActionProtocolError, match="requires evidence"):
        validate_progress({**progress, "evidence": []})
    with pytest.raises(ActionProtocolError, match="budget exceeded"):
        validate_progress({**progress, "changed_files": ["a", "b", "c"]})


def test_silent_in_progress_and_explicit_blocker_or_decision() -> None:
    in_progress = {
        "outcome": "in_progress",
        "budget": {"files": 1},
        "changed_files": [],
        "evidence": [],
    }
    assert notification_required(in_progress) is False
    with pytest.raises(ActionProtocolError, match="requires a blocker"):
        validate_progress({**in_progress, "outcome": "blocked"})
    with pytest.raises(ActionProtocolError, match="requires a decision"):
        validate_progress({**in_progress, "outcome": "decision_required"})


def test_loader_rejects_duplicate_and_unknown_dependencies(tmp_path: Path) -> None:
    chain = _chain()
    chain["actions"][1]["id"] = "P0"
    path = tmp_path / "chain.json"
    path.write_text(json.dumps(chain), encoding="utf-8")
    with pytest.raises(ActionProtocolError, match="duplicate action id"):
        load_action_chain(path)

    chain = _chain()
    chain["actions"][1]["depends_on"] = ["MISSING"]
    path.write_text(json.dumps(chain), encoding="utf-8")
    with pytest.raises(ActionProtocolError, match="unknown dependency"):
        load_action_chain(path)
