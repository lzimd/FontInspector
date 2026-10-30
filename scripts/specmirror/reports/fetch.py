"""Fetch report contracts, failure records, and writers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

from ..notice import Notice, NoticeJson
from ..paths import SourcePaths
from ..progress import Log
from ..storage import write_json_document


class PageCountsJson(TypedDict):
    """The serialized page counts of a fetch stage."""

    total: int
    added: int
    removed: int
    reused: int
    downloaded: int


class ImageCountsJson(TypedDict):
    """The serialized image counts of a fetch stage."""

    total: int
    reused: int
    downloaded: int
    pending: int
    failed: int


class DiscoveryJson(TypedDict):
    """The discovery document fetched at the start of a stage."""

    requested_url: str
    raw_file: str
    sha256: str
    content_type: str | None


class PagePlanRefJson(TypedDict):
    """The page plan file and its digest."""

    file: str
    sha256: str


class PageVerificationJson(TypedDict):
    """The outcome of re-verifying a cached page plan."""

    pages: int
    image_urls: int
    matched: bool


class ManifestRefJson(TypedDict):
    """The manifest digests recorded by the image stage."""

    old_sha256: str | None
    new_sha256: str
    snapshot_sha256: str


class RedirectJson(TypedDict):
    """The redirect chain followed for one requested URL."""

    url: str
    chain: list[dict[str, object]]


class ImageActionJson(TypedDict):
    """The planned or completed work for one image."""

    requested_url: str
    file: str
    action: str
    sha256: str | None


class DownloadFailureJson(TypedDict):
    """The serialized form of a download failure."""

    url: str
    status: int | None
    message: str
    redirects: list[str]


class FetchReport(TypedDict, total=False):
    """The JSON report written by a fetch stage."""

    source: str
    stage: str
    dry_run: bool
    success: bool
    error: str | None
    discovery: DiscoveryJson | None
    counts: PageCountsJson | ImageCountsJson | None
    image_candidate_count: int
    page_plan: PagePlanRefJson | None
    page_verification: PageVerificationJson | None
    orphan_page_files: list[str]
    orphan_image_files: list[str]
    manifest: ManifestRefJson | None
    failures: list[DownloadFailureJson]
    redirects: list[RedirectJson]
    warnings: list[NoticeJson]


@dataclass(frozen=True, slots=True)
class DownloadFailure:
    url: str
    status: int | None
    message: str
    redirects: tuple[str, ...] = ()

    def to_json(self) -> DownloadFailureJson:
        return {
            "url": self.url,
            "status": self.status,
            "message": self.message,
            "redirects": list(self.redirects),
        }


def notices_json(notices: tuple[Notice, ...]) -> list[NoticeJson]:
    return [notice.to_json() for notice in notices]


def failures_json(failures: list[DownloadFailure]) -> list[DownloadFailureJson]:
    return [failure.to_json() for failure in failures]


def write_fetch_report(
    paths: SourcePaths,
    report: FetchReport,
    *,
    dry_run: bool,
    log: Log,
) -> None:
    """Write a fetch report unless the stage was a dry run."""
    if dry_run:
        return
    stage = str(report.get("stage", "unknown"))
    try:
        write_json_document(paths.report_path(stage), report)
    except OSError as error:
        log(f"warning: could not write fetch report: {error}")
