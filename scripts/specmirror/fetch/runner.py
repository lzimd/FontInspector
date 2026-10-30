"""Composition of the fetch pages and fetch images stages."""

from __future__ import annotations

from ..errors import FetchError, UsageError
from ..paths import SourcePaths
from ..progress import Log, noop_log
from ..sources import get_source
from .http import HttpClient
from .images import run_images
from .models import FetchOutcome, FetchStage, ImagesOutcome, PagesOutcome
from .pages import run_pages


def run_fetch(
    source: str,
    stage: str,
    *,
    dry_run: bool,
    refresh: bool,
    paths: SourcePaths,
    client: HttpClient,
    log: Log | None = None,
) -> FetchOutcome:
    requested = _parse_stage(stage)
    if source != paths.source:
        raise UsageError("source does not match the configured paths")
    adapter = get_source(source)
    logger = log or noop_log

    pages: PagesOutcome | None = None
    images: ImagesOutcome | None = None
    if requested in {FetchStage.PAGES, FetchStage.ALL}:
        pages = run_pages(
            adapter,
            paths,
            dry_run=dry_run,
            refresh=refresh,
            client=client,
            log=logger,
        )
    if requested is FetchStage.IMAGES:
        images = run_images(
            adapter,
            paths,
            dry_run=dry_run,
            refresh=refresh,
            client=client,
            log=logger,
        )
    elif requested is FetchStage.ALL:
        if pages is None:
            raise FetchError("pages stage did not produce a page plan")
        images = run_images(
            adapter,
            paths,
            dry_run=dry_run,
            refresh=refresh,
            client=client,
            log=logger,
            snapshot=pages.snapshot() if dry_run else None,
        )
    return FetchOutcome(source=source, pages=pages, images=images)


def _parse_stage(value: str) -> FetchStage:
    try:
        return FetchStage(value)
    except ValueError as error:
        raise UsageError(f"unknown fetch stage: {value}") from error
