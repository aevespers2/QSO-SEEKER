from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .gateway import sanitize_records
from .report import load_json_report, write_pdf_report


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _build_report(accepted: list[dict[str, Any]], audit: list[dict[str, Any]], source: Path) -> dict[str, Any]:
    findings = []
    for record in accepted:
        flags = record.get("flags", [])
        if not flags:
            continue
        score = min(100, 20 * len(flags))
        findings.append({
            "repository": record.get("repository"),
            "path": record.get("path"),
            "source_kind": record.get("source_kind"),
            "score": score,
            "flags": flags,
            "content_sha256": record.get("content_sha256"),
        })
    canonical = json.dumps({"accepted": accepted, "audit": audit}, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "event_id": f"QSO-LOCAL-{hashlib.sha256(canonical).hexdigest()[:16]}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": "local-input",
        "scan_mode": "sanitization",
        "source_file": str(source),
        "summary_sha256": hashlib.sha256(canonical).hexdigest(),
        "summary": {
            "accepted_records": len(accepted),
            "audit_records": len(audit),
            "flagged_records": len(findings),
            "rejected_records": sum(1 for item in audit if item.get("status") == "rejected"),
        },
        "findings": findings,
    }


def sanitize_command(args: argparse.Namespace) -> int:
    payload = _read_json(args.input)
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise ValueError("input must be a JSON array of objects")
    accepted, audit = sanitize_records(payload)
    _write_json(args.output, accepted)
    _write_json(args.audit, audit)
    report = _build_report(accepted, audit, args.input)
    if args.report:
        _write_json(args.report, report)
    if args.pdf:
        write_pdf_report(report, args.pdf)
    return 0


def pdf_command(args: argparse.Namespace) -> int:
    write_pdf_report(load_json_report(args.report), args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="unicernal-search", description="QSO-SEEKER inert repository input gateway")
    subparsers = parser.add_subparsers(dest="command")

    sanitize = subparsers.add_parser("sanitize", help="sanitize JSON records and emit audit/evidence reports")
    sanitize.add_argument("input", type=Path)
    sanitize.add_argument("--output", type=Path, required=True)
    sanitize.add_argument("--audit", type=Path, required=True)
    sanitize.add_argument("--report", type=Path)
    sanitize.add_argument("--pdf", type=Path)
    sanitize.set_defaults(func=sanitize_command)

    pdf = subparsers.add_parser("pdf", help="render an existing JSON evidence report as PDF")
    pdf.add_argument("report", type=Path)
    pdf.add_argument("--output", type=Path, required=True)
    pdf.set_defaults(func=pdf_command)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "command", None):
        parser.print_help()
        raise SystemExit(2)
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
