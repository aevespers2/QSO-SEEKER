from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import asdict
from typing import Any

from .models import Genome


class GenomeManifest:
    """Create portable, tamper-evident genome manifests.

    HMAC is used for the first implementation because it is available in the
    Python standard library. Production cross-repository publication should
    replace or supplement it with asymmetric signatures and key rotation.
    """

    @staticmethod
    def payload(genome: Genome) -> dict[str, Any]:
        return {
            "manifest_version": 1,
            "target_repository": "aevespers2/QSO-GENOMES",
            "genome": asdict(genome),
        }

    @classmethod
    def canonical_bytes(cls, genome: Genome) -> bytes:
        return json.dumps(cls.payload(genome), sort_keys=True, separators=(",", ":")).encode("utf-8")

    @classmethod
    def sign(cls, genome: Genome, secret: bytes) -> dict[str, Any]:
        if len(secret) < 32:
            raise ValueError("signing secret must be at least 32 bytes")
        body = cls.payload(genome)
        signature = hmac.new(secret, cls.canonical_bytes(genome), hashlib.sha256).hexdigest()
        return {**body, "signature": {"algorithm": "HMAC-SHA256", "value": signature}}

    @classmethod
    def verify(cls, manifest: dict[str, Any], secret: bytes) -> bool:
        signature = manifest.get("signature", {})
        if signature.get("algorithm") != "HMAC-SHA256":
            return False
        unsigned = {key: value for key, value in manifest.items() if key != "signature"}
        encoded = json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode("utf-8")
        expected = hmac.new(secret, encoded, hashlib.sha256).hexdigest()
        return hmac.compare_digest(str(signature.get("value", "")), expected)
