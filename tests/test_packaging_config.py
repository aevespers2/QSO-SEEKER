from __future__ import annotations

import fnmatch
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_setuptools_discovery_is_scoped_to_runtime_package() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    include = data["tool"]["setuptools"]["packages"]["find"]["include"]

    assert include == ["unicernal_search*"]
    assert fnmatch.fnmatch("unicernal_search", include[0])
    for non_package in ("contracts", "schemas", "tests", "tools"):
        assert not fnmatch.fnmatch(non_package, include[0])
