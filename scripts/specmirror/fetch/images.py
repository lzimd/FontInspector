"""The fetch images stage: plan verification, image downloads, and the manifest."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..errors import FetchError, SpecMirrorError, UsageError
from ..manifest import write_manifest
from ..notice import Notice, NoticeKind
from ..paths import SourcePaths
from ..progress import Log, noop_log
from ..schema import ImageEntry, Manifest, PageEntry, PagePlan, require_media_type
from ..sources.base import SourceAdapter
from ..storage import (
    atomic_copy,
    file_matches_hash,
    list_tree_files,
    sha256_bytes,
    sha256_file,
    write_bytes_if_changed,
)
from .http import HttpClient
from .models import (
    FetchAction,
    ImageAction,
    ImageCounts,
    ImagesOutcome,
    PageSnapshot,
)
from .naming import assign_image_names
from .page_content import parse_page
from .page_plan import load_page_plan
from .reuse import load_previous_manifest, reusable_image
from .stage import (
    FetchReportDraft,
    append_redirects,
    download_failure,
    stage_report,
)


@dataclass(frozen=True, slots=True)
class _ImageWork:
    requested_url: str
    file: str
    action: FetchAction
    sha256: str | None
    content_type: str | None
    body: bytes | None
    source_path: Path | None


def run_images(
    adapter: SourceAdapter,
    paths: SourcePaths,
    *,
    dry_run: bool,
    refresh: bool,
    client: HttpClient,
    log: Log | None = None,
    snapshot: PageSnapshot | None = None,
) -> ImagesOutcome:
    logger = log or noop_log
    if snapshot is not None and not dry_run:
        raise UsageError("in-memory fetch inputs are only valid for dry runs")
    with stage_report(
        paths, adapter.key, "images", dry_run=dry_run, log=logger
    ) as report:
        return _run_images(
            adapter,
            paths,
            dry_run=dry_run,
            refresh=refresh,
            client=client,
            log=logger,
            report=report,
            snapshot=snapshot,
        )


def _run_images(
    adapter: SourceAdapter,
    paths: SourcePaths,
    *,
    dry_run: bool,
    refresh: bool,
    client: HttpClient,
    log: Log,
    report: FetchReportDraft,
    snapshot: PageSnapshot | None,
) -> ImagesOutcome:
    page_plan, plan_sha256 = _load_plan(paths, adapter, snapshot)
    report.page_plan = {
        "file": paths.plan_relative_path,
        "sha256": plan_sha256,
    }
    report.notices.extend(_verify_plan(adapter, paths, page_plan, snapshot=snapshot))
    report.page_verification = {
        "pages": len(page_plan.pages),
        "image_urls": len(page_plan.image_urls),
        "matched": True,
    }

    old_manifest_sha256 = (
        sha256_file(paths.manifest_path) if paths.manifest_path.is_file() else None
    )
    previous_manifest = load_previous_manifest(
        paths,
        adapter,
        report.notices,
        purpose="image reuse",
    )
    previous_images: dict[str, ImageEntry] = {}
    if previous_manifest is not None:
        previous_images = {
            image.requested_url: image for image in previous_manifest.manifest.images
        }

    works, actions = _plan_image_work(
        adapter,
        paths,
        page_plan,
        previous_images,
        report=report,
        refresh=refresh,
        dry_run=dry_run,
        client=client,
        log=log,
    )
    counts = ImageCounts(
        total=len(page_plan.image_urls),
        reused=sum(1 for work in works if work.action == FetchAction.REUSE),
        downloaded=sum(1 for work in works if work.action == FetchAction.DOWNLOAD),
        pending=sum(1 for work in works if work.action == FetchAction.PENDING),
        failed=len(report.failures),
    )
    report.counts = counts.to_json()
    if report.failures:
        first = report.failures[0]
        raise FetchError(
            f"{len(report.failures)} image(s) failed; first failure: {first.message}"
        )
    if dry_run:
        return ImagesOutcome(
            plan_sha256=plan_sha256,
            manifest=None,
            manifest_sha256=None,
            snapshot_sha256=None,
            actions=actions,
            counts=counts,
            warnings=tuple(report.notices),
            dry_run=True,
        )

    _write_image_cache(works, paths, log)
    manifest = _build_manifest(adapter, page_plan, works)
    _verify_snapshot_on_disk(page_plan, manifest, paths)
    loaded_manifest = write_manifest(paths, manifest)

    report.orphan_image_files = _orphan_image_files(paths, manifest)
    report.manifest = {
        "old_sha256": old_manifest_sha256,
        "new_sha256": loaded_manifest.file_sha256,
        "snapshot_sha256": manifest.snapshot_sha256(),
    }
    return ImagesOutcome(
        plan_sha256=plan_sha256,
        manifest=manifest,
        manifest_sha256=loaded_manifest.file_sha256,
        snapshot_sha256=manifest.snapshot_sha256(),
        actions=actions,
        counts=counts,
        warnings=tuple(report.notices),
        dry_run=False,
    )


def _load_plan(
    paths: SourcePaths,
    adapter: SourceAdapter,
    snapshot: PageSnapshot | None,
) -> tuple[PagePlan, str]:
    if snapshot is not None:
        if snapshot.plan.source != adapter.key:
            raise FetchError("page plan source does not match the fetch source")
        return snapshot.plan, snapshot.plan_sha256
    loaded = load_page_plan(
        paths.plan_path,
        expected_source=adapter.key,
        required=True,
    )
    if loaded is None:
        raise FetchError("page plan is missing")
    return loaded.plan, loaded.file_sha256


def _verify_plan(
    adapter: SourceAdapter,
    paths: SourcePaths,
    plan: PagePlan,
    *,
    snapshot: PageSnapshot | None,
) -> tuple[Notice, ...]:
    if (
        plan.discovery.requested_url != adapter.discovery_url
        or plan.discovery.raw_file != adapter.discovery_raw_file
    ):
        raise FetchError(
            "page plan discovery does not belong to this source; "
            f"rerun 'fetch pages' for {adapter.key}"
        )
    if snapshot is not None:
        discovery_body = snapshot.discovery_bytes
    else:
        discovery_path = paths.cache_path(plan.discovery.raw_file)
        if not discovery_path.is_file():
            raise FetchError(
                f"discovery cache is missing; rerun 'fetch pages' for {adapter.key}"
            )
        discovery_body = discovery_path.read_bytes()
    if sha256_bytes(discovery_body) != plan.discovery.sha256:
        raise FetchError(
            "discovery cache does not match the page plan; "
            f"rerun 'fetch pages' for {adapter.key}"
        )

    notices: list[Notice] = []
    derived_image_urls: set[str] = set()
    for page in plan.pages:
        adapter.validate_page_entry(page)
        body = _verified_page_body(page, paths, plan, snapshot)
        parsed = parse_page(adapter, body, page_url=page.requested_url)
        if (
            parsed.identity.slug != page.slug
            or parsed.identity.source_path != page.source_path
        ):
            raise FetchError(
                f"page identity does not match the page plan: {page.file}; "
                f"rerun 'fetch pages' for {adapter.key}"
            )
        derived_image_urls.update(parsed.image_urls)
        notices.extend(parsed.notices)

    if tuple(sorted(derived_image_urls)) != plan.image_urls:
        raise FetchError(
            "page image candidates do not match the page plan; "
            f"rerun 'fetch pages' for {adapter.key}"
        )
    return tuple(notices)


def _verified_page_body(
    page_entry: PageEntry,
    paths: SourcePaths,
    plan: PagePlan,
    snapshot: PageSnapshot | None,
) -> bytes:
    if snapshot is not None and page_entry.requested_url in snapshot.page_payloads:
        body = snapshot.page_payloads[page_entry.requested_url]
    else:
        page_path = paths.cache_path(page_entry.file)
        if not page_path.is_file():
            raise FetchError(
                f"page cache is missing: {page_entry.file}; "
                f"rerun 'fetch pages' for {plan.source}"
            )
        body = page_path.read_bytes()
    if sha256_bytes(body) != page_entry.sha256:
        raise FetchError(
            f"page cache does not match the page plan: {page_entry.file}; "
            f"rerun 'fetch pages' for {plan.source}"
        )
    return body


def _plan_image_work(
    adapter: SourceAdapter,
    paths: SourcePaths,
    page_plan: PagePlan,
    previous_images: dict[str, ImageEntry],
    *,
    report: FetchReportDraft,
    refresh: bool,
    dry_run: bool,
    client: HttpClient,
    log: Log,
) -> tuple[list[_ImageWork], tuple[ImageAction, ...]]:
    names = assign_image_names(page_plan.image_urls)
    works: list[_ImageWork] = []
    actions: list[ImageAction] = []
    for url in page_plan.image_urls:
        file = f"images/{names[url]}"
        previous = previous_images.get(url)
        if not refresh and previous is not None:
            reused = _reuse_image_work(url, file, previous, paths)
            if reused is not None:
                works.append(reused)
                actions.append(
                    ImageAction(url, file, FetchAction.REUSE, previous.sha256)
                )
                continue
            report.notices.append(
                Notice(
                    NoticeKind.CACHE_IMAGE_REJECTED,
                    f"image cache is missing or corrupt: {previous.file}",
                    url=url,
                )
            )

        if dry_run:
            works.append(
                _ImageWork(
                    requested_url=url,
                    file=file,
                    action=FetchAction.PENDING,
                    sha256=None,
                    content_type=None,
                    body=None,
                    source_path=None,
                )
            )
            actions.append(ImageAction(url, file, FetchAction.PENDING, None))
            continue

        downloaded = _download_image(
            adapter,
            url,
            file,
            client,
            log=log,
            report=report,
        )
        if downloaded is not None:
            works.append(downloaded)
            actions.append(
                ImageAction(url, file, FetchAction.DOWNLOAD, downloaded.sha256)
            )
    return works, tuple(actions)


def _reuse_image_work(
    url: str,
    file: str,
    previous: ImageEntry,
    paths: SourcePaths,
) -> _ImageWork | None:
    source_path = paths.cache_path(previous.file)
    if not reusable_image(source_path, previous):
        return None
    return _ImageWork(
        requested_url=url,
        file=file,
        action=FetchAction.REUSE,
        sha256=previous.sha256,
        content_type=previous.content_type,
        body=None,
        source_path=source_path,
    )


def _download_image(
    adapter: SourceAdapter,
    url: str,
    file: str,
    client: HttpClient,
    *,
    log: Log,
    report: FetchReportDraft,
) -> _ImageWork | None:
    log(f"{adapter.key} images: downloading {url}")
    try:
        response = client.fetch(url)
        append_redirects(report.redirects, response)
        content_type = require_media_type(
            response.content_type or "",
            where=f"image {url}",
        )
        if not content_type.startswith("image/"):
            raise FetchError(f"response is not an image: {url}")
        if not response.body:
            raise FetchError(f"image response is empty: {url}")
        digest = sha256_bytes(response.body)
    except SpecMirrorError as error:
        report.failures.append(download_failure(url, error))
        return None
    return _ImageWork(
        requested_url=url,
        file=file,
        action=FetchAction.DOWNLOAD,
        sha256=digest,
        content_type=content_type,
        body=response.body,
        source_path=None,
    )


def _write_image_cache(
    works: list[_ImageWork],
    paths: SourcePaths,
    log: Log,
) -> None:
    for work in works:
        target = paths.cache_path(work.file)
        if work.action == FetchAction.REUSE:
            if work.source_path is None or work.sha256 is None:
                raise FetchError(
                    f"reused image has no cache source: {work.requested_url}"
                )
            if work.source_path != target:
                atomic_copy(work.source_path, target)
            if not file_matches_hash(target, work.sha256):
                raise FetchError(
                    f"image cache does not match its expected hash: {work.file}"
                )
            continue
        if work.body is None or work.sha256 is None:
            raise FetchError(f"downloaded image has no bytes: {work.requested_url}")
        if write_bytes_if_changed(target, work.body):
            log(f"wrote {target}")
        if not file_matches_hash(target, work.sha256):
            raise FetchError(
                f"image cache does not match its expected hash: {work.file}"
            )


def _build_manifest(
    adapter: SourceAdapter,
    plan: PagePlan,
    works: list[_ImageWork],
) -> Manifest:
    manifest = Manifest(
        source=adapter.key,
        discovery=plan.discovery,
        pages=plan.pages,
        images=tuple(
            ImageEntry(
                requested_url=work.requested_url,
                file=work.file,
                sha256=_required(work.sha256, "image hash"),
                content_type=_required(work.content_type, "image content type"),
            )
            for work in works
        ),
    )
    Manifest.from_dict(manifest.to_dict(), expected_source=adapter.key)
    return manifest


def _verify_snapshot_on_disk(
    plan: PagePlan,
    manifest: Manifest,
    paths: SourcePaths,
) -> None:
    discovery_path = paths.cache_path(plan.discovery.raw_file)
    if not file_matches_hash(discovery_path, plan.discovery.sha256):
        raise FetchError(
            "discovery cache changed during the images stage; "
            f"rerun 'fetch pages' for {paths.source}"
        )
    for page in plan.pages:
        if not file_matches_hash(paths.cache_path(page.file), page.sha256):
            raise FetchError(
                f"page cache changed during the images stage: {page.file}; "
                f"rerun 'fetch pages' for {paths.source}"
            )
    for image in manifest.images:
        if not file_matches_hash(paths.cache_path(image.file), image.sha256):
            raise FetchError(f"image cache is incomplete: {image.file}")


def _orphan_image_files(paths: SourcePaths, manifest: Manifest) -> list[str]:
    known = {image.file for image in manifest.images}
    return [
        relative
        for relative in list_tree_files(paths.cache_root)
        if relative.startswith("images/") and relative not in known
    ]


def _required(value: str | None, what: str) -> str:
    if value is None:
        raise FetchError(f"missing {what}")
    return value
