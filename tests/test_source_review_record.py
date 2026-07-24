from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_source_review_record.py"
FIXTURE_PATH = ROOT / "docs" / "examples" / "source-review-record-v1.json"

SPEC = importlib.util.spec_from_file_location("validate_source_review_record", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SourceReviewRecordTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def assert_invalid(self, record: dict, expected: str) -> None:
        with self.assertRaisesRegex(MODULE.RecordValidationError, expected):
            MODULE.validate_record(record)

    def test_valid_synthetic_fixture(self) -> None:
        MODULE.validate_record(
            self.record,
            now=datetime.fromisoformat("2026-07-24T00:00:00+00:00"),
        )

    def test_expired_record_requires_expired_state(self) -> None:
        with self.assertRaisesRegex(
            MODULE.RecordValidationError, "EXPIRED_STATE_REQUIRED"
        ):
            MODULE.validate_record(
                self.record,
                now=datetime.fromisoformat("2026-08-24T00:00:00+00:00"),
            )

    def test_withdrawal_timestamp_requires_withdrawn_state(self) -> None:
        record = copy.deepcopy(self.record)
        record["decision"]["withdrawn_at"] = "2026-07-24T01:00:00-07:00"
        self.assert_invalid(record, "withdrawn_at requires WITHDRAWN state")

    def test_wrong_purpose_fails_closed(self) -> None:
        record = copy.deepcopy(self.record)
        record["request"]["purpose"] = "different-purpose"
        self.assert_invalid(record, "PURPOSE_MISMATCH")

    def test_wrong_consumer_fails_closed(self) -> None:
        record = copy.deepcopy(self.record)
        record["request"]["consumer"] = "unapproved-consumer"
        self.assert_invalid(record, "CONSUMER_MISMATCH")

    def test_privacy_downgrade_fails_closed(self) -> None:
        record = copy.deepcopy(self.record)
        record["request"]["requested_privacy_class"] = "RESTRICTED"
        record["decision"]["output_privacy_class"] = "PUBLIC_SYNTHETIC"
        self.assert_invalid(record, "PRIVACY_DOWNGRADE")

    def test_publication_without_approval_fails_closed(self) -> None:
        record = copy.deepcopy(self.record)
        record["request"]["operation"] = "publish"
        record["request"]["publication_requested"] = True
        self.assert_invalid(record, "PUBLICATION_NOT_APPROVED")

    def test_authority_gain_is_rejected(self) -> None:
        record = copy.deepcopy(self.record)
        record["authority"]["network"] = True
        self.assert_invalid(record, "deny every authority flag")

    def test_inactive_state_cannot_retain_operation(self) -> None:
        record = copy.deepcopy(self.record)
        record["decision"]["allowed_operations"] = ["sanitize"]
        self.assert_invalid(record, "REVIEW_REQUIRED must not retain allowed operations")


if __name__ == "__main__":
    unittest.main()
