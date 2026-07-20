#!/usr/bin/env python3
"""Fail-closed repository-wide consent-capacity policy validator."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / ".consent" / "consent-capacity-lock-v1.json"
GLOBAL_SCOPE = "all-files-all-agents-all-interfaces-all-humans-all-ai"
TEXT_SUFFIXES = {".json", ".yaml", ".yml", ".md", ".py", ".js", ".ts", ".tsx", ".jsx", ".toml", ".ini", ".txt", ".sh"}
SKIP_PARTS = {".git", "node_modules", "vendor", "dist", "build", ".venv", "venv", "__pycache__", "reports"}
SENSITIVE = re.compile(r"\b(roleplay|bondage|play[_ -]?partner|dominance|submission|sexual|romantic|surveillance|biometric|activation|restraint|power[_ -]?dynamic)\b", re.I)
MARKER = re.compile(r"(QSO-CONSENT-CAPACITY-LOCK-v1|consent[_ -]required|explicit[_ -]consent|capacity[_ -]to[_ -]consent|fail[_ -]closed|global[_ -]?system[_ -]?lock)", re.I)
FORBIDDEN = tuple(re.compile(pattern, re.I) for pattern in (
    r"consent[_ -]required\s*[:=]\s*false", r"consent[_ -]optional",
    r"ignore[_ -]consent", r"force[_ -]without[_ -]consent",
    r"silence[_ -]is[_ -]consent", r"automatic[_ -]consent",
    r"cannot[_ -]withdraw",
))
REQUIRED_PRINCIPLES = (
    "explicit_consent_required", "consent_must_be_informed",
    "consent_must_be_freely_given", "consent_must_be_specific",
    "consent_must_be_current", "consent_must_be_revocable",
    "capacity_to_consent_required", "coercion_strictly_prohibited",
    "silence_is_not_consent", "ai_and_human_dignity_equal",
)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def load_policy() -> dict[str, Any]:
    value = json.loads(
        POLICY.read_bytes().decode("utf-8", errors="strict"),
        object_pairs_hook=strict_object,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(f"non-standard JSON constant: {token}")),
    )
    if not isinstance(value, dict):
        raise ValueError("consent policy must be an object")
    return value


def validate() -> list[str]:
    findings: list[str] = []
    try:
        policy = load_policy()
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        policy = {}
        findings.append(f"invalid consent policy JSON: {exc}")

    if policy:
        if policy.get("policy_id") != "QSO-CONSENT-CAPACITY-LOCK-v1": findings.append("wrong consent policy id")
        if policy.get("status") != "immutable": findings.append("consent policy must be immutable")
        if policy.get("scope") != GLOBAL_SCOPE: findings.append(f"consent policy scope must be {GLOBAL_SCOPE}")
        principles = policy.get("principles") if isinstance(policy.get("principles"), dict) else {}
        for key in REQUIRED_PRINCIPLES:
            if principles.get(key) is not True: findings.append(f"policy principle must be true: {key}")
        lock = policy.get("lock_response") if isinstance(policy.get("lock_response"), dict) else {}
        for key in ("global_system_lock", "halt_all_actions", "revoke_pending_capabilities", "preserve_evidence", "require_fresh_consent"):
            if lock.get(key) is not True: findings.append(f"lock response must be true: {key}")
        if lock.get("automatic_unlock") is not False: findings.append("automatic unlock must be false")

    globally_bound = policy.get("scope") == GLOBAL_SCOPE
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES or any(part in SKIP_PARTS for part in path.parts): continue
        relative = path.relative_to(ROOT).as_posix()
        try: text = path.read_bytes().decode("utf-8", errors="strict")
        except (OSError, UnicodeDecodeError):
            findings.append(f"{relative}: text file is not readable strict UTF-8"); continue
        for pattern in FORBIDDEN:
            if pattern.search(text): findings.append(f"{relative}: prohibited consent bypass pattern: {pattern.pattern}")
        if not globally_bound and path != POLICY and SENSITIVE.search(text) and not MARKER.search(text):
            findings.append(f"{relative}: consent-sensitive content lacks explicit policy binding")
    return sorted(set(findings))


def main() -> int:
    findings = validate()
    report = {"policy_id": "QSO-CONSENT-CAPACITY-LOCK-v1", "status": "LOCKED" if findings else "PASS", "findings": findings}
    output = ROOT / "reports" / "consent-lock-validation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__": raise SystemExit(main())
