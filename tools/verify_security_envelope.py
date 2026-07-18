from __future__ import annotations

import ast
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = [ROOT / "unicernal_search", ROOT / "experimental" / "qso_spawn", ROOT / "tools"]
FORBIDDEN_CALLS = {"eval", "exec", "compile", "__import__"}
FORBIDDEN_IMPORTS = {"subprocess", "socket", "requests", "httpx", "urllib.request"}
FORBIDDEN_ATTRS = {
    "os.system",
    "os.popen",
    "subprocess.run",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
}
ALLOWED_DEPENDENCIES = {"pydantic>=2.6"}


def dotted_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return None


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in FORBIDDEN_IMPORTS:
                    findings.append(f"{path.relative_to(ROOT)}:{node.lineno}: forbidden import {alias.name}")
        elif isinstance(node, ast.ImportFrom) and node.module in FORBIDDEN_IMPORTS:
            findings.append(f"{path.relative_to(ROOT)}:{node.lineno}: forbidden import {node.module}")
        elif isinstance(node, ast.Call):
            name = dotted_name(node.func)
            if name in FORBIDDEN_CALLS or name in FORBIDDEN_ATTRS:
                findings.append(f"{path.relative_to(ROOT)}:{node.lineno}: forbidden call {name}")
    return findings


def verify_dependencies() -> list[str]:
    try:
        document = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return [f"pyproject.toml: unable to parse dependencies: {exc}"]

    dependencies = document.get("project", {}).get("dependencies")
    if not isinstance(dependencies, list) or not all(isinstance(item, str) for item in dependencies):
        return ["pyproject.toml: project.dependencies must be an array of strings"]

    declared = set(dependencies)
    findings: list[str] = []
    if declared - ALLOWED_DEPENDENCIES:
        findings.append(f"pyproject.toml: unexpected dependencies: {sorted(declared - ALLOWED_DEPENDENCIES)}")
    if ALLOWED_DEPENDENCIES - declared:
        findings.append(f"pyproject.toml: required dependencies missing: {sorted(ALLOWED_DEPENDENCIES - declared)}")
    return findings


def main() -> int:
    findings: list[str] = []
    for directory in SCAN_DIRS:
        if directory.exists():
            for path in sorted(directory.rglob("*.py")):
                if path.resolve() != Path(__file__).resolve():
                    findings.extend(scan_file(path))
    findings.extend(verify_dependencies())
    print(json.dumps({"status": "pass" if not findings else "fail", "findings": findings}, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
