"""Cache-reuse policy shared by the page and image stages."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ..errors import FetchError, SpecMirrorError
from ..manifest import LoadedManifest, load_manifest
from ..notice import Notice, NoticeKind
from ..paths import SourcePaths
from ..schema import DiscoveryEntry, ImageEntry, PageEntry
from ..sources.base import PageCandidate, SourceAdapter
from ..storage import sha256_bytes, sha256_file
from ..urls import UrlIndex
from .models import FetchAction
from .page_content import ValidatedPage, validate_page
from .page_plan import LoadedPagePlan, load_page_plan


@dataclass(frozen=True, slots=True)
class PreviousState:
    manifest: LoadedManifest | None
    plan: LoadedPagePlan | None
    notices: tuple[Notice, ...]


@dataclass(frozen=True, slots=True)
class ReusablePages:
    """The cached pages that a fetch stage can reuse."""

    manifest: UrlIndex[PageEntry]
    plan: UrlIndex[PageEntry]


class _PreviousSnapshot(Protocol):
    """The manifest and page plan shapes shared by the cache-reuse checks."""

    @property
    def source(self) -> str: ...

    @property
    def discovery(self) -> DiscoveryEntry: ...

    @property
    def pages(self) -> tuple[PageEntry, ...]: ...


def load_previous_state(paths: SourcePaths, adapter: SourceAdapter) -> PreviousState:
    notices: list[Notice] = []
    manifest = load_previous_manifest(
        paths,
        adapter,
        notices,
        purpose="cache reuse",
    )
    plan = _load_previous_plan(
        paths,
        adapter,
        notices,
        purpose="cache reuse",
    )
    return PreviousState(
        manifest=manifest,
        plan=plan,
        notices=tuple(notices),
    )


def reusable_pages(previous: PreviousState) -> ReusablePages:
    """Index the cached pages that a fetch stage can reuse."""
    manifest_pages = (
        previous.manifest.manifest.pages if previous.manifest is not None else ()
    )
    plan_pages = previous.plan.plan.pages if previous.plan is not None else ()
    return ReusablePages(
        manifest=UrlIndex((page.requested_url, page) for page in manifest_pages),
        plan=UrlIndex((page.requested_url, page) for page in plan_pages),
    )


def reuse_page(
    adapter: SourceAdapter,
    paths: SourcePaths,
    candidate: PageCandidate,
    reusable: ReusablePages,
    notices: list[Notice],
) -> ValidatedPage | None:
    entries: list[tuple[str, PageEntry]] = []
    manifest_page = reusable.manifest.get(candidate.requested_url)
    if manifest_page is not None:
        entries.append(("manifest", manifest_page))
    plan_page = reusable.plan.get(candidate.requested_url)
    if plan_page is not None:
        entries.append(("plan", plan_page))

    for origin, entry in entries:
        cache_path = paths.cache_path(entry.file)
        if not cache_path.is_file():
            notices.append(
                Notice(
                    NoticeKind.CACHE_MISS,
                    f"{origin} page cache is missing: {entry.file}",
                    page=entry.slug,
                    url=candidate.requested_url,
                )
            )
            continue
        try:
            body = cache_path.read_bytes()
        except OSError as error:
            notices.append(
                Notice(
                    NoticeKind.CACHE_READ_FAILED,
                    f"cannot read {origin} page cache {entry.file}: {error}",
                    page=entry.slug,
                    url=candidate.requested_url,
                )
            )
            continue
        if sha256_bytes(body) != entry.sha256:
            notices.append(
                Notice(
                    NoticeKind.CACHE_HASH_MISMATCH,
                    f"{origin} page cache does not match its hash: {entry.file}",
                    page=entry.slug,
                    url=candidate.requested_url,
                )
            )
            continue
        try:
            validated = validate_page(
                adapter,
                candidate,
                body,
                content_type=entry.content_type,
                last_modified=entry.last_modified,
                action=FetchAction.REUSE,
            )
        except SpecMirrorError as error:
            notices.append(
                Notice(
                    NoticeKind.CACHE_PAGE_INVALID,
                    f"{origin} page cache is not a valid page: {error}",
                    page=entry.slug,
                    url=candidate.requested_url,
                )
            )
            continue
        if (
            validated.identity.slug != entry.slug
            or validated.identity.source_path != entry.source_path
        ):
            notices.append(
                Notice(
                    NoticeKind.CACHE_PAGE_IDENTITY_MISMATCH,
                    f"{origin} page cache identity does not match its entry",
                    page=entry.slug,
                    url=candidate.requested_url,
                )
            )
            continue
        return validated
    return None


def reusable_image(path: Path, entry: ImageEntry) -> bool:
    try:
        if not path.is_file() or path.stat().st_size == 0:
            return False
        return sha256_file(path) == entry.sha256
    except OSError:
        return False


def load_previous_manifest(
    paths: SourcePaths,
    adapter: SourceAdapter,
    notices: list[Notice],
    *,
    purpose: str,
) -> LoadedManifest | None:
    if not paths.manifest_path.is_file():
        return None
    try:
        manifest = load_manifest(
            paths.manifest_path,
            expected_source=adapter.key,
            required=False,
        )
        if manifest is None:
            return None
        _validate_previous_snapshot(manifest.manifest, adapter, label="manifest")
        return manifest
    except SpecMirrorError as error:
        notices.append(
            Notice(
                NoticeKind.INVALID_PREVIOUS_MANIFEST,
                f"ignoring previous manifest for {purpose}: {error}",
            )
        )
        return None


def _load_previous_plan(
    paths: SourcePaths,
    adapter: SourceAdapter,
    notices: list[Notice],
    *,
    purpose: str,
) -> LoadedPagePlan | None:
    if not paths.plan_path.is_file():
        return None
    try:
        plan = load_page_plan(
            paths.plan_path,
            expected_source=adapter.key,
            required=False,
        )
        if plan is None:
            return None
        _validate_previous_snapshot(plan.plan, adapter, label="page plan")
        return plan
    except SpecMirrorError as error:
        notices.append(
            Notice(
                NoticeKind.INVALID_PREVIOUS_PLAN,
                f"ignoring previous page plan for {purpose}: {error}",
            )
        )
        return None


def _validate_previous_snapshot(
    snapshot: _PreviousSnapshot,
    adapter: SourceAdapter,
    *,
    label: str,
) -> None:
    if snapshot.source != adapter.key:
        raise FetchError(f"previous {label} source does not match")
    if snapshot.discovery.requested_url != adapter.discovery_url:
        raise FetchError(f"previous {label} discovery URL does not match")
    if snapshot.discovery.raw_file != adapter.discovery_raw_file:
        raise FetchError(f"previous {label} discovery file does not match")
    for page in snapshot.pages:
        adapter.validate_page_entry(page)
