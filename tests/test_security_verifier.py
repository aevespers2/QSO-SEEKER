from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "verify_security_envelope.py"
spec = importlib.util.spec_from_file_location("verify_security_envelope", MODULE_PATH)
assert spec and spec.loader
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


def test_dependency_parser_accepts_one_line_array(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\ndependencies = ["pydantic>=2.6"]\n', encoding="utf-8")
    assert verifier.verify_dependencies(pyproject) == []


def test_dependency_parser_rejects_unapproved_dependency(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[project]\ndependencies = ["pydantic>=2.6", "requests>=2"]\n',
        encoding="utf-8",
    )
    findings = verifier.verify_dependencies(pyproject)
    assert findings == ["pyproject.toml: unexpected dependencies: ['requests>=2']"]
