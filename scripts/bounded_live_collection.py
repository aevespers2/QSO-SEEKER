"""Bounded read-only HTTPS collector for QSO-SEEKER."""
from __future__ import annotations
import argparse, hashlib, json, urllib.error, urllib.parse, urllib.request
from pathlib import Path
from typing import Any

MAX_BYTES = 1_000_000
ALLOWED_TYPES = {"text/plain", "text/html", "text/markdown", "application/json", "application/ld+json", "text/csv", "application/xml", "text/xml"}

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        raise urllib.error.HTTPError(req.full_url, code, "redirects disabled", headers, fp)

def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def run(config_path: Path, output_dir: Path, enable_network: bool) -> dict[str, Any]:
    registry = json.loads(config_path.read_text(encoding="utf-8"))
    if registry.get("mode") != "live-bounded" or registry.get("network_enabled") is not True or not enable_network:
        raise ValueError("live collection requires mode=live-bounded, network_enabled=true, and --enable-network")
    hosts = {str(h).lower() for h in registry.get("allowlisted_hosts", [])}
    if not hosts:
        raise ValueError("allowlisted_hosts is required")
    max_bytes = min(int(registry.get("max_response_bytes", MAX_BYTES)), MAX_BYTES)
    timeout = min(int(registry.get("timeout_seconds", 15)), 30)
    sources = registry.get("sources", [])
    if not sources:
        raise ValueError("at least one source is required")
    output_dir.mkdir(parents=True, exist_ok=True)
    records_dir = output_dir / "retrieval-records"
    records_dir.mkdir(exist_ok=True)
    opener = urllib.request.build_opener(NoRedirect)
    results = []
    for source in sources:
        url = str(source["url"])
        parsed = urllib.parse.urlsplit(url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or host not in hosts or parsed.username or parsed.password or parsed.port not in (None, 443):
            raise ValueError(f"disallowed source URL: {url}")
        request = urllib.request.Request(url, method="GET", headers={"User-Agent": "QSO-SEEKER/1.0 bounded-read-only", "Accept": "text/plain,text/html,application/json;q=0.9,*/*;q=0.1"})
        with opener.open(request, timeout=timeout) as response:
            content_type = response.headers.get_content_type().lower()
            if content_type not in ALLOWED_TYPES:
                raise ValueError(f"disallowed content type: {content_type}")
            body = response.read(max_bytes + 1)
            if len(body) > max_bytes:
                raise ValueError(f"response exceeded {max_bytes} bytes")
            record = {
                "schema_version": "qso-seeker-retrieval-v1",
                "source_id": source["source_id"],
                "url": url,
                "topic": source["topic"],
                "purpose": source["purpose"],
                "status": int(response.status),
                "content_type": content_type,
                "body_utf8": body.decode("utf-8", errors="replace"),
                "body_sha256": sha256(body),
                "network_used": True,
                "read_only": True,
                "untrusted_text": True,
                "executable": False,
            }
            record_hash = sha256(canonical(record).encode("utf-8"))
            record["record_sha256"] = record_hash
            (records_dir / f"{record_hash}.json").write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
            results.append(record_hash)
    summary = {"status": "checkpoint-ready", "mode": "live-bounded", "network_used": True, "source_count": len(results), "record_hashes": results, "checkpoint": 1, "automatic_release": False, "human_review_required": True}
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    return summary

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--enable-network", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.config, args.output, args.enable_network), sort_keys=True))

if __name__ == "__main__":
    main()
