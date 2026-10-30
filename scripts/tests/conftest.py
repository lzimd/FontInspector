"""Fixtures shared by the SpecMirror test modules."""

from __future__ import annotations

from pathlib import Path

import pytest
from specmirror.paths import SourcePaths


@pytest.fixture
def opentype_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> SourcePaths:
    monkeypatch.setattr(
        "specmirror.build.pipeline.CORRECTIONS_ROOT", tmp_path / "corrections"
    )
    return SourcePaths(root=tmp_path, source="opentype")


@pytest.fixture
def truetype_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> SourcePaths:
    monkeypatch.setattr(
        "specmirror.build.pipeline.CORRECTIONS_ROOT", tmp_path / "corrections"
    )
    return SourcePaths(root=tmp_path, source="truetype")
