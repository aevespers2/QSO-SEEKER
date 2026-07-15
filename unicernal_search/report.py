from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any

PAGE_WIDTH = 612
PAGE_HEIGHT = 792
LEFT = 54
TOP = 738
BOTTOM = 54
LINE_HEIGHT = 13
FONT_SIZE = 9


def _pdf_escape(text: str) -> str:
    safe = text.encode("latin-1", "replace").decode("latin-1")
    return safe.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _flatten_report(report: dict[str, Any]) -> list[str]:
    lines = ["QSO-SEEKER Evidence Report", ""]
    for key in ("event_id", "generated_at", "repository", "scan_mode", "summary_sha256"):
        if key in report:
            lines.append(f"{key.replace('_', ' ').title()}: {report[key]}")
    lines.append("")
    summary = report.get("summary", {})
    if isinstance(summary, dict):
        lines.append("Summary")
        for key, value in sorted(summary.items()):
            lines.append(f"- {key}: {value}")
        lines.append("")
    findings = report.get("findings", [])
    lines.append(f"Findings ({len(findings) if isinstance(findings, list) else 0})")
    if isinstance(findings, list):
        for index, finding in enumerate(findings, start=1):
            if not isinstance(finding, dict):
                continue
            lines.append(f"{index}. Repository: {finding.get('repository', 'unknown')}")
            lines.append(f"   Resource: {finding.get('path', finding.get('source_kind', 'unknown'))}")
            lines.append(f"   Score: {finding.get('score', 0)}")
            flags = finding.get("flags", [])
            lines.append(f"   Flags: {', '.join(flags) if isinstance(flags, list) else flags}")
            lines.append(f"   SHA-256: {finding.get('content_sha256', '')}")
            lines.append("   Classification: signal requiring review; not proof of compromise.")
            lines.append("")
    lines.append("Integrity Note")
    lines.append("This PDF is a human-readable rendering of the JSON evidence report. The JSON output remains the canonical machine-readable record.")
    return lines


def write_pdf_report(report: dict[str, Any], output: Path) -> None:
    wrapped: list[str] = []
    for line in _flatten_report(report):
        if not line:
            wrapped.append("")
        else:
            wrapped.extend(textwrap.wrap(str(line), width=92, replace_whitespace=False, drop_whitespace=True) or [""])

    lines_per_page = max(1, int((TOP - BOTTOM) / LINE_HEIGHT))
    pages = [wrapped[i:i + lines_per_page] for i in range(0, len(wrapped), lines_per_page)] or [[]]

    objects: list[bytes] = []
    catalog_id = 1
    pages_id = 2
    font_id = 3
    page_ids: list[int] = []
    content_ids: list[int] = []

    next_id = 4
    for _ in pages:
        page_ids.append(next_id)
        content_ids.append(next_id + 1)
        next_id += 2

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode("ascii"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>")

    for page_lines, page_id, content_id in zip(pages, page_ids, content_ids):
        stream_lines = ["BT", f"/F1 {FONT_SIZE} Tf", f"{LEFT} {TOP} Td", f"{LINE_HEIGHT} TL"]
        for index, line in enumerate(page_lines):
            if index:
                stream_lines.append("T*")
            stream_lines.append(f"({_pdf_escape(line)}) Tj")
        stream_lines.append("ET")
        stream = "\n".join(stream_lines).encode("latin-1", "replace")
        page_obj = f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] /Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>".encode("ascii")
        content_obj = b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream"
        objects.append(page_obj)
        objects.append(content_obj)

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as handle:
        handle.write(b"%PDF-1.4\n%QSO-SEEKER\n")
        offsets = [0]
        for object_id, payload in enumerate(objects, start=1):
            offsets.append(handle.tell())
            handle.write(f"{object_id} 0 obj\n".encode("ascii"))
            handle.write(payload)
            handle.write(b"\nendobj\n")
        xref = handle.tell()
        handle.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        handle.write(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            handle.write(f"{offset:010d} 00000 n \n".encode("ascii"))
        handle.write(f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii"))


def load_json_report(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("report JSON must be an object")
    return data
