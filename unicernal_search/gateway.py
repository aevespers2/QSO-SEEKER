from __future__ import annotations

import hashlib
import html
import re
import unicodedata
from pathlib import PurePosixPath
from typing import Any

from pydantic import ValidationError
from .schema import RawSearchRecord, SanitizedRecord

REJECTED_EXTENSIONS = {".exe", ".dll", ".so", ".dylib", ".bin", ".msi", ".apk", ".jar", ".wasm", ".zip", ".tar", ".gz", ".7z", ".rar", ".iso", ".dmg", ".deb", ".rpm", ".docm", ".xlsm", ".pptm"}
BIDI = {"\u061c", "\u200e", "\u200f", "\u202a", "\u202b", "\u202c", "\u202d", "\u202e", "\u2066", "\u2067", "\u2068", "\u2069"}
ACTIVE = re.compile(r"(?is)<\s*(script|iframe|object|embed|svg|math)\b.*?>.*?<\s*/\s*\1\s*>")
EVENTS = re.compile(r"(?i)\s+on[a-z]+\s*=\s*(['\"]).*?\1")
DANGEROUS_URI = re.compile(r"(?i)\b(?:javascript|data|vbscript|file)\s*:")
ANSI = re.compile(r"\x1b(?:[@-_][0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))")
PATTERNS = {
    "prompt_injection": ["ignore previous instructions", "system prompt", "developer message", "reveal your instructions", "you are now", "jailbreak"],
    "execution_request": ["curl | sh", "wget | sh", "bash -c", "powershell -enc", "invoke-expression", "os.system(", "subprocess.run(", "eval(", "exec("],
    "credential_access": ["github_token", "gh_token", "private_key", "/proc/self/environ", ".ssh/id_rsa", ".aws/credentials"],
}

def _binary(text: str) -> bool:
    if "\x00" in text:
        return True
    sample = text[:4096]
    return bool(sample) and sum(unicodedata.category(c) == "Cc" and c not in "\n\r\t" for c in sample) / len(sample) > .01

def _sanitize(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    value = unicodedata.normalize("NFKC", text)
    if value != text: changes.append("unicode_nfkc")
    newer = "".join(c for c in value if c not in BIDI)
    if newer != value: changes.append("removed_bidi_controls")
    value = newer
    newer = ANSI.sub("", value)
    if newer != value: changes.append("removed_ansi")
    value = html.unescape(newer)
    newer = ACTIVE.sub("[REMOVED ACTIVE CONTENT]", value)
    if newer != value: changes.append("removed_active_html")
    value = EVENTS.sub("", newer)
    newer = DANGEROUS_URI.sub("[REMOVED-URI]:", value)
    if newer != value: changes.append("neutralized_uri_scheme")
    value = newer[:120_000]
    if len(newer) > 120_000: changes.append("truncated")
    return value, changes

def sanitize_records(payload: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted, audit = [], []
    for index, item in enumerate(payload):
        try:
            raw = RawSearchRecord.model_validate(item)
        except ValidationError as exc:
            audit.append({"index": index, "status": "rejected", "reason": "schema_validation_failed", "details": exc.errors(include_url=False)})
            continue
        suffix = PurePosixPath(raw.path.lower()).suffix
        if suffix in REJECTED_EXTENSIONS or _binary(raw.content):
            audit.append({"index": index, "repository": raw.repository, "path": raw.path, "status": "rejected", "reason": "executable_archive_or_binary"})
            continue
        clean, transformations = _sanitize(raw.content)
        lower = clean.casefold()
        flags = sorted(k for k, patterns in PATTERNS.items() if any(p.casefold() in lower for p in patterns))
        digest = hashlib.sha256(clean.encode()).hexdigest()
        record = SanitizedRecord(repository=raw.repository, path=raw.path, source_kind=raw.source_kind, source_url=str(raw.url), content=clean, content_sha256=digest, flags=flags, transformations=transformations)
        accepted.append(record.model_dump())
        audit.append({"index": index, "status": "accepted_with_flags" if flags else "accepted", "flags": flags, "content_sha256": digest, "transformations": transformations})
    return accepted, audit
