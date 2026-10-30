from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest
from helpers import (
    OPENTYPE_IMAGE_URL,
    TRUETYPE_IMAGE_URL,
    FakeClient,
    add_opentype_pages,
    add_truetype_pages,
)
from specmirror.errors import FetchError
from specmirror.fetch import run_fetch
from specmirror.fetch.naming import assign_image_names
from specmirror.fetch.page_plan import load_page_plan, write_page_plan
from specmirror.manifest import load_manifest
from specmirror.paths import SourcePaths
from specmirror.schema import PagePlan, parse_json_bytes


def prepare_opentype_pages(
    paths: SourcePaths,
    *,
    otff_images: tuple[str, ...] = (),
) -> None:
    client = FakeClient()
    add_opentype_pages(client, otff_images=otff_images)
    run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=paths,
        client=client,
    )


def prepare_truetype_pages(
    paths: SourcePaths,
    *,
    index_images: tuple[str, ...] = (),
) -> None:
    client = FakeClient()
    add_truetype_pages(client, index_images=index_images)
    run_fetch(
        "truetype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=paths,
        client=client,
    )


def test_images_stage_publishes_manifest_without_page_network(
    opentype_paths: SourcePaths,
) -> None:
    prepare_opentype_pages(opentype_paths, otff_images=("images/fig.png",))
    plan_before = opentype_paths.plan_path.read_bytes()
    plan = load_page_plan(
        opentype_paths.plan_path,
        expected_source="opentype",
        required=True,
    )
    assert plan is not None

    client = FakeClient()
    client.add(OPENTYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    outcome = run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    images = outcome.images
    assert images is not None
    assert images.manifest is not None
    assert client.calls == [OPENTYPE_IMAGE_URL]
    assert opentype_paths.plan_path.read_bytes() == plan_before
    assert opentype_paths.manifest_path.is_file()
    assert opentype_paths.cache_path("images/fig.png").read_bytes() == b"\x89PNG\r\n"
    assert images.counts.downloaded == 1
    assert images.counts.reused == 0

    loaded = load_manifest(
        opentype_paths.manifest_path,
        expected_source="opentype",
        required=True,
    )
    assert loaded is not None
    manifest = loaded.manifest
    assert manifest.pages == plan.plan.pages
    assert len(manifest.images) == 1
    assert manifest.images[0].file == "images/fig.png"
    assert manifest.images[0].content_type == "image/png"
    assert manifest.snapshot_sha256() == images.snapshot_sha256

    report = parse_json_bytes(
        opentype_paths.report_path("images").read_bytes(),
        what="images report",
    )
    assert report["success"] is True
    verification = cast("dict[str, object]", report["page_verification"])
    assert verification["matched"] is True


def test_images_stage_reuses_cached_images(opentype_paths: SourcePaths) -> None:
    prepare_opentype_pages(opentype_paths, otff_images=("images/fig.png",))
    client = FakeClient()
    client.add(OPENTYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    first = run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert first.images is not None
    manifest_before = opentype_paths.manifest_path.read_bytes()

    client.calls.clear()
    second = run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert second.images is not None
    assert client.calls == []
    assert second.images.counts.reused == 1
    assert second.images.counts.downloaded == 0
    assert opentype_paths.manifest_path.read_bytes() == manifest_before


def test_images_refresh_downloads_every_image(opentype_paths: SourcePaths) -> None:
    prepare_opentype_pages(opentype_paths, otff_images=("images/fig.png",))
    client = FakeClient()
    client.add(OPENTYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    client.calls.clear()
    outcome = run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=True,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.images is not None
    assert outcome.images.counts.downloaded == 1
    assert client.calls == [OPENTYPE_IMAGE_URL]


def test_images_dry_run_makes_no_network_requests_or_writes(
    opentype_paths: SourcePaths,
) -> None:
    prepare_opentype_pages(opentype_paths, otff_images=("images/fig.png",))
    client = FakeClient()
    outcome = run_fetch(
        "opentype",
        "images",
        dry_run=True,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.images is not None
    assert outcome.images.manifest is None
    assert outcome.images.actions[0].action == "pending"
    assert outcome.images.counts.pending == 1
    assert outcome.images.counts.downloaded == 0
    assert client.calls == []
    assert not opentype_paths.report_path("images").exists()
    assert not opentype_paths.manifest_path.exists()


def test_images_dry_run_reports_reuse_without_network(
    opentype_paths: SourcePaths,
) -> None:
    prepare_opentype_pages(opentype_paths, otff_images=("images/fig.png",))
    client = FakeClient()
    client.add(OPENTYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    manifest_before = opentype_paths.manifest_path.read_bytes()
    client.calls.clear()
    outcome = run_fetch(
        "opentype",
        "images",
        dry_run=True,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.images is not None
    assert outcome.images.actions[0].action == "reuse"
    assert outcome.images.counts.reused == 1
    assert outcome.images.counts.pending == 0
    assert client.calls == []
    assert opentype_paths.manifest_path.read_bytes() == manifest_before


def test_images_redownload_corrupt_or_missing_cache(
    opentype_paths: SourcePaths,
) -> None:
    prepare_opentype_pages(opentype_paths, otff_images=("images/fig.png",))
    client = FakeClient()
    client.add(OPENTYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    manifest_before = opentype_paths.manifest_path.read_bytes()
    image_path = opentype_paths.cache_path("images/fig.png")

    image_path.write_bytes(b"corrupt")
    client.calls.clear()
    second = run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert second.images is not None
    assert client.calls == [OPENTYPE_IMAGE_URL]
    assert second.images.counts.downloaded == 1
    assert opentype_paths.manifest_path.read_bytes() == manifest_before

    image_path.unlink()
    client.calls.clear()
    third = run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert third.images is not None
    assert client.calls == [OPENTYPE_IMAGE_URL]
    assert third.images.counts.downloaded == 1
    assert opentype_paths.manifest_path.read_bytes() == manifest_before


def test_images_require_a_page_plan(opentype_paths: SourcePaths) -> None:
    client = FakeClient()
    with pytest.raises(FetchError):
        run_fetch(
            "opentype",
            "images",
            dry_run=False,
            refresh=False,
            paths=opentype_paths,
            client=client,
        )
    assert client.calls == []
    assert not opentype_paths.manifest_path.exists()


def test_images_reject_stale_page_cache_before_network(
    opentype_paths: SourcePaths,
) -> None:
    prepare_opentype_pages(opentype_paths, otff_images=("images/fig.png",))
    client = FakeClient()
    client.add(OPENTYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    manifest_before = opentype_paths.manifest_path.read_bytes()

    opentype_paths.cache_path("pages/otff.html").write_bytes(b"stale")
    stale_client = FakeClient()
    with pytest.raises(FetchError):
        run_fetch(
            "opentype",
            "images",
            dry_run=False,
            refresh=False,
            paths=opentype_paths,
            client=stale_client,
        )
    assert stale_client.calls == []
    assert opentype_paths.manifest_path.read_bytes() == manifest_before


def test_images_reject_plan_with_mismatched_image_set(
    opentype_paths: SourcePaths,
) -> None:
    prepare_opentype_pages(opentype_paths, otff_images=("images/fig.png",))
    loaded = load_page_plan(
        opentype_paths.plan_path,
        expected_source="opentype",
        required=True,
    )
    assert loaded is not None
    extra_url = "https://learn.microsoft.com/en-us/typography/opentype/spec/other.png"
    modified = PagePlan(
        source=loaded.plan.source,
        discovery=loaded.plan.discovery,
        pages=loaded.plan.pages,
        image_urls=tuple(sorted((*loaded.plan.image_urls, extra_url))),
    )
    write_page_plan(opentype_paths, modified)

    client = FakeClient()
    with pytest.raises(FetchError):
        run_fetch(
            "opentype",
            "images",
            dry_run=False,
            refresh=False,
            paths=opentype_paths,
            client=client,
        )
    assert client.calls == []
    assert not opentype_paths.manifest_path.exists()


def test_images_reject_non_image_and_empty_responses(
    opentype_paths: SourcePaths,
) -> None:
    prepare_opentype_pages(opentype_paths, otff_images=("images/fig.png",))

    client = FakeClient()
    client.add(OPENTYPE_IMAGE_URL, b"not an image", content_type="text/html")
    with pytest.raises(FetchError):
        run_fetch(
            "opentype",
            "images",
            dry_run=False,
            refresh=False,
            paths=opentype_paths,
            client=client,
        )
    assert not opentype_paths.manifest_path.exists()

    empty_client = FakeClient()
    empty_client.add(OPENTYPE_IMAGE_URL, b"", content_type="image/png")
    with pytest.raises(FetchError):
        run_fetch(
            "opentype",
            "images",
            dry_run=False,
            refresh=False,
            paths=opentype_paths,
            client=empty_client,
        )
    assert not opentype_paths.manifest_path.exists()


def test_images_with_failing_download_preserve_manifest(
    opentype_paths: SourcePaths,
) -> None:
    prepare_opentype_pages(opentype_paths, otff_images=("images/fig.png",))
    client = FakeClient()
    client.add(OPENTYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    manifest_before = opentype_paths.manifest_path.read_bytes()

    failing = FakeClient()
    failing.fail(OPENTYPE_IMAGE_URL, 503)
    with pytest.raises(FetchError):
        run_fetch(
            "opentype",
            "images",
            dry_run=False,
            refresh=True,
            paths=opentype_paths,
            client=failing,
        )
    assert opentype_paths.manifest_path.read_bytes() == manifest_before
    report = parse_json_bytes(
        opentype_paths.report_path("images").read_bytes(),
        what="images report",
    )
    assert report["success"] is False


def test_image_name_collisions_get_deterministic_suffixes(
    opentype_paths: SourcePaths,
) -> None:
    prepare_opentype_pages(
        opentype_paths,
        otff_images=("images/fig.png", "other/fig.png"),
    )
    loaded = load_page_plan(
        opentype_paths.plan_path,
        expected_source="opentype",
        required=True,
    )
    assert loaded is not None
    assert len(loaded.plan.image_urls) == 2

    client = FakeClient()
    client.add(
        "https://learn.microsoft.com/en-us/typography/opentype/spec/images/fig.png",
        b"first",
        content_type="image/png",
    )
    client.add(
        "https://learn.microsoft.com/en-us/typography/opentype/spec/other/fig.png",
        b"second",
        content_type="image/png",
    )
    outcome = run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.images is not None
    assert outcome.images.manifest is not None
    files = {image.file for image in outcome.images.manifest.images}
    assert len(files) == 2
    assert all(file.startswith("images/fig-") for file in files)


def test_fetch_all_matches_two_stage_fetch(
    opentype_paths: SourcePaths,
    tmp_path: Path,
) -> None:
    other_paths = SourcePaths(root=tmp_path / "other", source="opentype")
    other_paths.root.mkdir()

    staged = FakeClient()
    add_opentype_pages(staged, otff_images=("images/fig.png",))
    run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=staged,
    )
    staged.add(OPENTYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=staged,
    )

    combined = FakeClient()
    add_opentype_pages(combined, otff_images=("images/fig.png",))
    combined.add(OPENTYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    run_fetch(
        "opentype",
        "all",
        dry_run=False,
        refresh=False,
        paths=other_paths,
        client=combined,
    )
    assert (
        opentype_paths.manifest_path.read_bytes()
        == other_paths.manifest_path.read_bytes()
    )


def test_fetch_all_dry_run_chains_plans_without_image_network(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client, otff_images=("images/fig.png",))
    outcome = run_fetch(
        "opentype",
        "all",
        dry_run=True,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.pages is not None
    assert outcome.images is not None
    assert outcome.images.manifest is None
    assert outcome.images.actions[0].action == "pending"
    assert outcome.images.counts.pending == 1
    assert outcome.images.counts.downloaded == 0
    assert OPENTYPE_IMAGE_URL not in client.calls
    assert not opentype_paths.scratch_root.exists()


def test_truetype_images_stage_uses_cached_snapshot(
    truetype_paths: SourcePaths,
) -> None:
    prepare_truetype_pages(truetype_paths, index_images=("images/fig.png",))
    client = FakeClient()
    client.add(TRUETYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    outcome = run_fetch(
        "truetype",
        "images",
        dry_run=False,
        refresh=False,
        paths=truetype_paths,
        client=client,
    )
    assert outcome.images is not None
    assert outcome.images.manifest is not None
    assert client.calls == [TRUETYPE_IMAGE_URL]
    assert truetype_paths.cache_path("images/fig.png").is_file()
    loaded = load_manifest(
        truetype_paths.manifest_path,
        expected_source="truetype",
        required=True,
    )
    assert loaded is not None
    assert loaded.manifest.images[0].requested_url == TRUETYPE_IMAGE_URL


def test_assign_image_names_sanitizes_and_handles_collisions() -> None:
    names = assign_image_names(("https://example.com/a%20b.png",))
    assert names == {"https://example.com/a%20b.png": "a_b.png"}
    assert assign_image_names(("https://example.com/",)) == {
        "https://example.com/": "image"
    }

    urls = (
        "https://example.com/one/fig.png",
        "https://example.com/two/fig.png",
    )
    first = assign_image_names(urls)
    second = assign_image_names(urls)
    assert first == second
    assert len(set(first.values())) == 2
    assert all(name.startswith("fig-") for name in first.values())
