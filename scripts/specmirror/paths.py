"""Repository, scratch, and output paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .errors import UsageError
from .schema import SOURCE_KEYS
from .storage import safe_relative_path


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class SourcePaths:
    root: Path
    source: str

    def __post_init__(self) -> None:
        if self.source not in SOURCE_KEYS:
            raise UsageError(f"unknown source: {self.source}")

    @property
    def scratch_root(self) -> Path:
        return self.root / ".scratch" / "specmirror"

    @property
    def cache_root(self) -> Path:
        return self.scratch_root / self.source

    @property
    def reports_root(self) -> Path:
        return self.scratch_root / "reports"

    @property
    def output_root(self) -> Path:
        return self.root / "docs" / "references" / self.source

    @property
    def plan_relative_path(self) -> str:
        return "staging/page-plan.json"

    @property
    def plan_path(self) -> Path:
        return self.cache_root.joinpath(*PurePosixPath(self.plan_relative_path).parts)

    @property
    def manifest_path(self) -> Path:
        return self.cache_root / "manifest.json"

    def cache_path(self, relative: str) -> Path:
        pure = safe_relative_path(relative, where="cache path")
        return self.cache_root.joinpath(*pure.parts)

    def report_path(self, stage: str) -> Path:
        return self.reports_root / f"fetch-{self.source}-{stage}.json"

    @property
    def build_report_path(self) -> Path:
        return self.reports_root / f"build-{self.source}.json"
