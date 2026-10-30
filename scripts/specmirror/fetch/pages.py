"""The fetch pages stage: discovery, page downloads, and the page plan."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..errors import FetchError, SpecMirrorError
from ..paths import SourcePaths
from ..progress import Log, noop_log
from ..reports.fetch import DownloadFailure
from ..schema import DiscoveryEntry, PageEntry, PagePlan
from ..sources.base import DiscoveryResult, PageCandidate, SourceAdapter
from ..storage import list_tree_files, sha256_bytes, write_bytes_if_changed
from ..urls import normalize_url
from .http import HttpClient, HttpResponse
from .models import FetchAction, PageCounts, PagesOutcome
from .page_content import (
    ValidatedPage,
    build_page_entry,
    check_slug_collisions,
    validate_page,
)
from .page_plan import write_page_plan
from .reuse import (
    PreviousState,
    ReusablePages,
    load_previous_state,
    reusable_pages,
    reuse_page,
)
from .stage import (
    FetchReportDraft,
    append_redirects,
    download_failure,
    parse_last_modified,
    stage_report,
)


@dataclass(frozen=True, slots=True)
class _PreloadedPage:
    body: bytes
    content_type: str | None
    last_modified: str | None


@dataclass(frozen=True, slots=True)
class _DiscoveryState:
    response: HttpResponse
    discovery: DiscoveryResult
    sha256: str
    preloaded: _PreloadedPage | None


def run_pages(
    adapter: SourceAdapter,
    paths: SourcePaths,
    *,
    dry_run: bool,
    refresh: bool,
    client: HttpClient,
    log: Log | None = None,
) -> PagesOutcome:
    logger = log or noop_log
    with stage_report(
        paths, adapter.key, "pages", dry_run=dry_run, log=logger
    ) as report:
        return _run_pages(
            adapter,
            paths,
            dry_run=dry_run,
            refresh=refresh,
            client=client,
            log=logger,
            report=report,
        )


def _run_pages(
    adapter: SourceAdapter,
    paths: SourcePaths,
    *,
    dry_run: bool,
    refresh: bool,
    client: HttpClient,
    log: Log,
    report: FetchReportDraft,
) -> PagesOutcome:
    notices = report.notices
    previous = load_previous_state(paths, adapter)
    notices.extend(previous.notices)
    reusable = reusable_pages(previous)

    log(f"{adapter.key} pages: refreshing discovery")
    discovery = _refresh_discovery(
        adapter,
        paths,
        client,
        dry_run=dry_run,
        log=log,
        report=report,
    )
    index_url = normalize_url(adapter.discovery_url)
    candidates = _dedupe_candidates(discovery.discovery.candidates)
    effective = _resolve_pages(
        adapter,
        paths,
        candidates,
        index_url=index_url,
        preloaded=discovery.preloaded,
        reusable=reusable,
        refresh=refresh,
        client=client,
        log=log,
        report=report,
    )
    for page in effective:
        notices.extend(page.notices)

    check_slug_collisions(effective)
    pages = tuple(build_page_entry(adapter, page) for page in effective)
    image_urls = tuple(sorted({url for page in effective for url in page.image_urls}))
    plan = PagePlan(
        source=adapter.key,
        discovery=DiscoveryEntry(
            requested_url=adapter.discovery_url,
            raw_file=adapter.discovery_raw_file,
            sha256=discovery.sha256,
        ),
        pages=pages,
        image_urls=image_urls,
    )
    PagePlan.from_dict(plan.to_dict(), expected_source=adapter.key)
    plan_bytes, plan_sha256 = _publish_pages(
        paths,
        plan,
        effective,
        dry_run=dry_run,
        log=log,
    )
    counts = _page_counts(previous, pages, effective)
    report.counts = counts.to_json()
    report.image_candidate_count = len(image_urls)
    report.page_plan = {
        "file": paths.plan_relative_path,
        "sha256": plan_sha256,
    }
    report.orphan_page_files = _orphan_page_files(paths, pages)

    return PagesOutcome(
        plan=plan,
        plan_bytes=plan_bytes,
        plan_sha256=plan_sha256,
        discovery_bytes=discovery.response.body,
        page_payloads={page.candidate.requested_url: page.body for page in effective},
        counts=counts,
        warnings=tuple(notices),
        dry_run=dry_run,
    )


def _refresh_discovery(
    adapter: SourceAdapter,
    paths: SourcePaths,
    client: HttpClient,
    *,
    dry_run: bool,
    log: Log,
    report: FetchReportDraft,
) -> _DiscoveryState:
    response = client.fetch(adapter.discovery_url)
    append_redirects(report.redirects, response)
    if not response.body:
        raise FetchError("discovery response is empty")
    digest = sha256_bytes(response.body)
    report.discovery = {
        "requested_url": adapter.discovery_url,
        "raw_file": adapter.discovery_raw_file,
        "sha256": digest,
        "content_type": response.content_type,
    }
    discovery = adapter.parse_discovery(
        response.body,
        requested_url=adapter.discovery_url,
        content_type=response.content_type,
    )
    report.notices.extend(discovery.warnings)
    if not dry_run:
        _write_cache_file(
            paths.cache_path(adapter.discovery_raw_file),
            response.body,
            log,
        )
        for audit_file in discovery.audit_files:
            _write_cache_file(paths.cache_path(audit_file.path), audit_file.data, log)

    last_modified = parse_last_modified(
        response.last_modified,
        report.notices,
        adapter.discovery_url,
    )
    preloaded: _PreloadedPage | None = None
    index_url = normalize_url(adapter.discovery_url)
    if adapter.discovery_is_page:
        if not any(
            candidate.requested_url == index_url for candidate in discovery.candidates
        ):
            raise FetchError("discovery page is missing from the page candidates")
        preloaded = _PreloadedPage(
            body=response.body,
            content_type=response.content_type,
            last_modified=last_modified,
        )
    return _DiscoveryState(
        response=response,
        discovery=discovery,
        sha256=digest,
        preloaded=preloaded,
    )


def _resolve_pages(
    adapter: SourceAdapter,
    paths: SourcePaths,
    candidates: list[PageCandidate],
    *,
    index_url: str,
    preloaded: _PreloadedPage | None,
    reusable: ReusablePages,
    refresh: bool,
    client: HttpClient,
    log: Log,
    report: FetchReportDraft,
) -> list[ValidatedPage]:
    for candidate in candidates:
        if not adapter.scope_contains(candidate.requested_url):
            raise FetchError(
                f"discovery returned an out-of-scope page: {candidate.requested_url}"
            )
        if not candidate.title:
            raise FetchError(
                f"discovery returned a page without a title: {candidate.requested_url}"
            )
        if any(not title for title in candidate.section):
            raise FetchError(
                f"discovery returned an empty section title: {candidate.requested_url}"
            )

    effective: list[ValidatedPage] = []
    for candidate in candidates:
        if preloaded is not None and candidate.requested_url == index_url:
            try:
                effective.append(
                    validate_page(
                        adapter,
                        candidate,
                        preloaded.body,
                        content_type=preloaded.content_type,
                        last_modified=preloaded.last_modified,
                        action=FetchAction.DISCOVERY,
                    )
                )
            except SpecMirrorError as error:
                report.failures.append(
                    DownloadFailure(candidate.requested_url, None, str(error))
                )
            continue

        if not refresh:
            reused = reuse_page(
                adapter,
                paths,
                candidate,
                reusable,
                report.notices,
            )
            if reused is not None:
                effective.append(reused)
                continue

        downloaded = _download_page(
            adapter,
            candidate,
            client,
            log=log,
            report=report,
        )
        if downloaded is not None:
            effective.append(downloaded)

    if report.failures:
        first = report.failures[0]
        raise FetchError(
            f"{len(report.failures)} page(s) failed; first failure: {first.message}"
        )
    return effective


def _download_page(
    adapter: SourceAdapter,
    candidate: PageCandidate,
    client: HttpClient,
    *,
    log: Log,
    report: FetchReportDraft,
) -> ValidatedPage | None:
    log(f"{adapter.key} pages: downloading {candidate.requested_url}")
    try:
        response = client.fetch(candidate.requested_url)
        append_redirects(report.redirects, response)
        last_modified = parse_last_modified(
            response.last_modified,
            report.notices,
            candidate.requested_url,
        )
        return validate_page(
            adapter,
            candidate,
            response.body,
            content_type=response.content_type,
            last_modified=last_modified,
            action=FetchAction.DOWNLOAD,
        )
    except SpecMirrorError as error:
        report.failures.append(download_failure(candidate.requested_url, error))
        return None


def _publish_pages(
    paths: SourcePaths,
    plan: PagePlan,
    pages: list[ValidatedPage],
    *,
    dry_run: bool,
    log: Log,
) -> tuple[bytes, str]:
    if dry_run:
        data = plan.to_bytes()
        return data, sha256_bytes(data)
    for page, entry in zip(pages, plan.pages, strict=True):
        _write_cache_file(paths.cache_path(entry.file), page.body, log)
    loaded = write_page_plan(paths, plan)
    return loaded.data, loaded.file_sha256


def _page_counts(
    previous: PreviousState,
    pages: tuple[PageEntry, ...],
    effective: list[ValidatedPage],
) -> PageCounts:
    previous_urls: set[str] = set()
    if previous.plan is not None:
        previous_urls = {page.requested_url for page in previous.plan.plan.pages}
    elif previous.manifest is not None:
        previous_urls = {
            page.requested_url for page in previous.manifest.manifest.pages
        }
    current_urls = {page.requested_url for page in pages}
    return PageCounts(
        total=len(pages),
        added=len(current_urls - previous_urls),
        removed=len(previous_urls - current_urls),
        reused=sum(1 for page in effective if page.action == FetchAction.REUSE),
        downloaded=sum(
            1
            for page in effective
            if page.action in {FetchAction.DOWNLOAD, FetchAction.DISCOVERY}
        ),
    )


def _orphan_page_files(
    paths: SourcePaths,
    pages: tuple[PageEntry, ...],
) -> list[str]:
    known = {page.file for page in pages}
    return [
        relative
        for relative in list_tree_files(paths.cache_root)
        if relative.startswith("pages/") and relative not in known
    ]


def _dedupe_candidates(candidates: tuple[PageCandidate, ...]) -> list[PageCandidate]:
    seen: set[str] = set()
    result: list[PageCandidate] = []
    for candidate in candidates:
        if candidate.requested_url in seen:
            continue
        seen.add(candidate.requested_url)
        result.append(candidate)
    return result


def _write_cache_file(path: Path, data: bytes, log: Log) -> None:
    if write_bytes_if_changed(path, data):
        log(f"wrote {path}")
