"""Report lifecycle and small diagnostics shared by both fetch stages."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass, field

from ..errors import FetchError, HttpError, HttpStatusError, SpecMirrorError
from ..notice import Notice, NoticeKind
from ..paths import SourcePaths
from ..progress import Log
from ..reports.fetch import (
    DiscoveryJson,
    DownloadFailure,
    FetchReport,
    ImageCountsJson,
    ManifestRefJson,
    PageCountsJson,
    PagePlanRefJson,
    PageVerificationJson,
    RedirectJson,
    failures_json,
    notices_json,
    write_fetch_report,
)
from .http import HttpResponse, parse_http_date


@dataclass(slots=True)
class FetchReportDraft:
    """The state one fetch stage accumulates before it writes its report."""

    source: str
    stage: str
    dry_run: bool
    success: bool = False
    error: str | None = None
    discovery: DiscoveryJson | None = None
    counts: PageCountsJson | ImageCountsJson | None = None
    image_candidate_count: int = 0
    page_plan: PagePlanRefJson | None = None
    page_verification: PageVerificationJson | None = None
    orphan_page_files: list[str] = field(default_factory=list[str])
    orphan_image_files: list[str] = field(default_factory=list[str])
    manifest: ManifestRefJson | None = None
    notices: list[Notice] = field(default_factory=list[Notice])
    failures: list[DownloadFailure] = field(default_factory=list[DownloadFailure])
    redirects: list[RedirectJson] = field(default_factory=list[RedirectJson])

    def to_report(self) -> FetchReport:
        """The JSON report for the stage as it stands right now."""
        return {
            "source": self.source,
            "stage": self.stage,
            "dry_run": self.dry_run,
            "success": self.success,
            "error": self.error,
            "discovery": self.discovery,
            "counts": self.counts,
            "image_candidate_count": self.image_candidate_count,
            "page_plan": self.page_plan,
            "page_verification": self.page_verification,
            "orphan_page_files": list(self.orphan_page_files),
            "orphan_image_files": list(self.orphan_image_files),
            "manifest": self.manifest,
            "failures": failures_json(self.failures),
            "redirects": list(self.redirects),
            "warnings": notices_json(tuple(self.notices)),
        }


@contextmanager
def stage_report(
    paths: SourcePaths,
    source: str,
    stage: str,
    *,
    dry_run: bool,
    log: Log,
) -> Generator[FetchReportDraft]:
    """Write the stage report on success and on controlled failure."""
    draft = FetchReportDraft(source=source, stage=stage, dry_run=dry_run)
    try:
        yield draft
    except OSError as error:
        message = f"I/O failure: {error}"
        draft.error = message
        write_fetch_report(paths, draft.to_report(), dry_run=dry_run, log=log)
        raise FetchError(message) from error
    except Exception as error:
        draft.error = _error_text(error)
        write_fetch_report(paths, draft.to_report(), dry_run=dry_run, log=log)
        raise
    else:
        draft.success = True
        draft.error = None
        write_fetch_report(paths, draft.to_report(), dry_run=dry_run, log=log)


def append_redirects(
    records: list[RedirectJson],
    response: HttpResponse,
) -> None:
    if not response.redirects:
        return
    records.append(
        {
            "url": response.requested_url,
            "chain": [redirect.to_json() for redirect in response.redirects],
        }
    )


def parse_last_modified(
    value: str | None,
    notices: list[Notice],
    url: str,
) -> str | None:
    if value is None:
        return None
    parsed = parse_http_date(value)
    if parsed is None:
        notices.append(
            Notice(
                NoticeKind.INVALID_LAST_MODIFIED,
                f"invalid Last-Modified header {value!r}",
                url=url,
            )
        )
    return parsed


def download_failure(url: str, error: SpecMirrorError) -> DownloadFailure:
    status = error.status if isinstance(error, HttpStatusError) else None
    redirects = error.redirects if isinstance(error, HttpError) else ()
    return DownloadFailure(url, status, str(error), redirects)


def _error_text(error: Exception) -> str:
    if isinstance(error, SpecMirrorError):
        return str(error)
    return f"{type(error).__name__}: {error}"
