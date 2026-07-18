from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class QSOEnvelope:
    sender_id: str
    recipient_id: str
    message_type: str
    payload: dict[str, Any]
    nonce: str
    created_at: str
    signature: str


class EnvelopeCodec:
    @staticmethod
    def _body(sender_id: str, recipient_id: str, message_type: str, payload: dict[str, Any], nonce: str, created_at: str) -> bytes:
        return json.dumps(
            {
                "sender_id": sender_id,
                "recipient_id": recipient_id,
                "message_type": message_type,
                "payload": payload,
                "nonce": nonce,
                "created_at": created_at,
            },
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")

    @classmethod
    def create(
        cls,
        sender_id: str,
        recipient_id: str,
        message_type: str,
        payload: dict[str, Any],
        secret: bytes,
        *,
        nonce: str,
    ) -> QSOEnvelope:
        if len(secret) < 32:
            raise ValueError("secret must be at least 32 bytes")
        if not all(value.strip() for value in (sender_id, recipient_id, message_type, nonce)):
            raise ValueError("sender, recipient, message type, and nonce are required")
        created_at = datetime.now(timezone.utc).isoformat()
        signature = hmac.new(
            secret,
            cls._body(sender_id, recipient_id, message_type, payload, nonce, created_at),
            hashlib.sha256,
        ).hexdigest()
        return QSOEnvelope(sender_id, recipient_id, message_type, payload, nonce, created_at, signature)

    @classmethod
    def verify(cls, envelope: QSOEnvelope, secret: bytes) -> bool:
        expected = hmac.new(
            secret,
            cls._body(
                envelope.sender_id,
                envelope.recipient_id,
                envelope.message_type,
                envelope.payload,
                envelope.nonce,
                envelope.created_at,
            ),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(envelope.signature, expected)

    @staticmethod
    def serialize(envelope: QSOEnvelope) -> str:
        return json.dumps(asdict(envelope), sort_keys=True, separators=(",", ":"), default=str)
