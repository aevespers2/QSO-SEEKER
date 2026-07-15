from pathlib import Path

from unicernal_search.report import write_pdf_report


def test_pdf_report_is_created(tmp_path: Path):
    output = tmp_path / "report.pdf"
    write_pdf_report(
        {
            "event_id": "QSO-TEST-1",
            "generated_at": "2026-07-15T00:00:00+00:00",
            "repository": "example/project",
            "scan_mode": "test",
            "summary_sha256": "0" * 64,
            "summary": {"flagged_records": 1},
            "findings": [
                {
                    "repository": "example/project",
                    "path": "README.md",
                    "score": 80,
                    "flags": ["prompt_injection"],
                    "content_sha256": "1" * 64,
                }
            ],
        },
        output,
    )
    data = output.read_bytes()
    assert data.startswith(b"%PDF-1.4")
    assert b"QSO-SEEKER Evidence Report" in data
    assert data.rstrip().endswith(b"%%EOF")
