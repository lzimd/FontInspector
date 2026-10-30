"""Fetch stage facts and outcomes shared by pages, images, and the runner."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum

from ..notice import Notice
from ..reports.fetch import ImageActionJson, ImageCountsJson, PageCountsJson
from ..schema import Manifest, PagePlan


class FetchStage(StrEnum):
    """The stage selection accepted by the fetch entry point."""

    ALL = "all"
    IMAGES = "images"
    PAGES = "pages"


class FetchAction(StrEnum):
    """What the fetch stage did with a page or an image."""

    DISCOVERY = "discovery"
    DOWNLOAD = "download"
    PENDING = "pending"
    REUSE = "reuse"


@dataclass(frozen=True, slots=True)
class PageCounts:
    total: int
    added: int
    removed: int
    reused: int
    downloaded: int

    def to_json(self) -> PageCountsJson:
        return {
            "total": self.total,
            "added": self.added,
            "removed": self.removed,
            "reused": self.reused,
            "downloaded": self.downloaded,
        }


@dataclass(frozen=True, slots=True)
class ImageCounts:
    total: int
    reused: int
    downloaded: int
    failed: int
    pending: int = 0

    def to_json(self) -> ImageCountsJson:
        return {
            "total": self.total,
            "reused": self.reused,
            "downloaded": self.downloaded,
            "pending": self.pending,
            "failed": self.failed,
        }


@dataclass(frozen=True, slots=True)
class ImageAction:
    requested_url: str
    file: str
    action: FetchAction
    sha256: str | None

    def to_json(self) -> ImageActionJson:
        return {
            "requested_url": self.requested_url,
            "file": self.file,
            "action": str(self.action),
            "sha256": self.sha256,
        }


@dataclass(frozen=True, slots=True)
class PageSnapshot:
    """The in-memory page result that a dry run passes to the image stage."""

    plan: PagePlan
    plan_sha256: str
    discovery_bytes: bytes
    page_payloads: Mapping[str, bytes]


@dataclass(frozen=True, slots=True)
class PagesOutcome:
    plan: PagePlan
    plan_bytes: bytes
    plan_sha256: str
    discovery_bytes: bytes
    page_payloads: Mapping[str, bytes]
    counts: PageCounts
    warnings: tuple[Notice, ...]
    dry_run: bool

    def snapshot(self) -> PageSnapshot:
        return PageSnapshot(
            plan=self.plan,
            plan_sha256=self.plan_sha256,
            discovery_bytes=self.discovery_bytes,
            page_payloads=self.page_payloads,
        )


@dataclass(frozen=True, slots=True)
class ImagesOutcome:
    plan_sha256: str
    manifest: Manifest | None
    manifest_sha256: str | None
    snapshot_sha256: str | None
    actions: tuple[ImageAction, ...]
    counts: ImageCounts
    warnings: tuple[Notice, ...]
    dry_run: bool


@dataclass(frozen=True, slots=True)
class FetchOutcome:
    source: str
    pages: PagesOutcome | None
    images: ImagesOutcome | None
