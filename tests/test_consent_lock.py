from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_consent_lock.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_consent_lock", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load consent validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def policy() -> dict:
    return {
        "policy_id": "QSO-CONSENT-CAPACITY-LOCK-v1",
        "status": "immutable",
        "scope": "all-files-all-agents-all-interfaces-all-humans-all-ai",
        "principles": {
            "explicit_consent_required": True,
            "consent_must_be_informed": True,
            "consent_must_be_freely_given": True,
            "consent_must_be_specific": True,
            "consent_must_be_current": True,
            "consent_must_be_revocable": True,
            "capacity_to_consent_required": True,
            "coercion_strictly_prohibited": True,
            "silence_is_not_consent": True,
            "ai_and_human_dignity_equal": True,
        },
        "lock_response": {
            "global_system_lock": True,
            "halt_all_actions": True,
            "revoke_pending_capabilities": True,
            "preserve_evidence": True,
            "require_fresh_consent": True,
            "automatic_unlock": False,
        },
    }


class ConsentLockTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / ".consent").mkdir()
        self.module = load_validator()
        self.module.ROOT = self.root
        self.module.POLICY = self.root / ".consent" / "consent-capacity-lock-v1.json"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_policy(self, value: dict) -> None:
        self.module.POLICY.write_text(json.dumps(value), encoding="utf-8")

    def test_global_scope_covers_sensitive_files(self) -> None:
        self.write_policy(policy())
        (self.root / "seeker.py").write_text("activation_mode='review'\n", encoding="utf-8")
        self.assertEqual([], self.module.validate())

    def test_bypass_pattern_fails_closed(self) -> None:
        self.write_policy(policy())
        (self.root / "unsafe.md").write_text("consent_" + "required: false", encoding="utf-8")
        self.assertTrue(any("prohibited consent bypass" in item for item in self.module.validate()))

    def test_duplicate_policy_key_fails_closed(self) -> None:
        self.module.POLICY.write_text('{"policy_id":"x","policy_id":"y"}', encoding="utf-8")
        self.assertTrue(any("duplicate JSON key" in item for item in self.module.validate()))

    def test_automatic_unlock_must_remain_false(self) -> None:
        value = policy()
        value["lock_response"]["automatic_unlock"] = True
        self.write_policy(value)
        self.assertIn("automatic unlock must be false", self.module.validate())


if __name__ == "__main__": unittest.main()
