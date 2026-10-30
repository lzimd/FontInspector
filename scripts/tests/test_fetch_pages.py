from __future__ import annotations

from typing import cast

import pytest
from helpers import (
    OPEN_TYPE_LAST_MODIFIED_ISO,
    OPENTYPE_HEAD_URL,
    OPENTYPE_IMAGE_URL,
    OPENTYPE_LANDING_URL,
    OPENTYPE_OTFF_URL,
    OPENTYPE_TOC_URL,
    TRUETYPE_AAT_URL,
    TRUETYPE_CVT_URL,
    TRUETYPE_IMAGE_URL,
    TRUETYPE_INDEX_URL,
    TRUETYPE_LAST_MODIFIED_ISO,
    TRUETYPE_OS2_URL,
    FakeClient,
    add_opentype_pages,
    add_truetype_pages,
    opentype_page_html,
    opentype_toc,
)
from specmirror.errors import FetchError
from specmirror.fetch import run_fetch
from specmirror.fetch.page_plan import load_page_plan
from specmirror.paths import SourcePaths
from specmirror.schema import parse_json_bytes

OPENTYPE_NEW_URL = "https://learn.microsoft.com/en-us/typography/opentype/spec/newpage"


def test_pages_stage_writes_plan_and_pages_but_not_manifest(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client, otff_images=("images/fig.png",))
    outcome = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    pages = outcome.pages
    assert pages is not None
    assert pages.plan.pages[0].slug == "index"
    assert pages.plan.pages[0].source_path == "typographydocs/opentype/spec/index.md"
    assert [page.slug for page in pages.plan.pages] == ["index", "otff", "head"]
    assert pages.plan.image_urls == (OPENTYPE_IMAGE_URL,)
    assert pages.plan.pages[1].last_modified == OPEN_TYPE_LAST_MODIFIED_ISO
    assert pages.counts.downloaded == 3
    assert pages.counts.reused == 0

    assert opentype_paths.plan_path.is_file()
    assert not opentype_paths.manifest_path.exists()
    assert opentype_paths.cache_path("pages/otff.html").is_file()
    assert opentype_paths.cache_path("toc/toc.json").is_file()
    assert opentype_paths.report_path("pages").is_file()

    loaded = load_page_plan(
        opentype_paths.plan_path,
        expected_source="opentype",
        required=True,
    )
    assert loaded is not None
    assert loaded.plan == pages.plan
    assert loaded.data == pages.plan_bytes

    report = parse_json_bytes(
        opentype_paths.report_path("pages").read_bytes(),
        what="pages report",
    )
    assert report["success"] is True
    assert report["error"] is None
    assert report["image_candidate_count"] == 1
    counts = cast("dict[str, object]", report["counts"])
    assert counts["downloaded"] == 3
    assert counts["reused"] == 0

    assert OPENTYPE_IMAGE_URL not in client.calls
    assert set(client.calls) == {
        OPENTYPE_TOC_URL,
        OPENTYPE_LANDING_URL,
        OPENTYPE_OTFF_URL,
        OPENTYPE_HEAD_URL,
    }


def test_pages_stage_reuses_cache_without_revalidating_pages(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    first = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert first.pages is not None

    client.calls.clear()
    second = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    pages = second.pages
    assert pages is not None
    assert client.calls == [OPENTYPE_TOC_URL]
    assert pages.counts.reused == 3
    assert pages.counts.downloaded == 0
    assert pages.plan_bytes == first.pages.plan_bytes


def test_pages_reuse_from_manifest_when_plan_is_missing(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client, otff_images=("images/fig.png",))
    run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    client.add(OPENTYPE_IMAGE_URL, b"\x89PNG\r\n", content_type="image/png")
    run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert opentype_paths.manifest_path.is_file()
    opentype_paths.plan_path.unlink()

    client.calls.clear()
    outcome = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.pages is not None
    assert client.calls == [OPENTYPE_TOC_URL]
    assert outcome.pages.counts.reused == 3
    assert outcome.pages.counts.downloaded == 0
    assert opentype_paths.plan_path.is_file()


def test_pages_reuse_matches_plan_when_manifest_is_stale(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    run_fetch(
        "opentype",
        "images",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert opentype_paths.manifest_path.is_file()

    client.add(
        OPENTYPE_OTFF_URL,
        opentype_page_html(
            "typographydocs/opentype/spec/otff.md",
            "The OpenType Font File, revised",
        ),
    )
    run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=True,
        paths=opentype_paths,
        client=client,
    )

    client.calls.clear()
    outcome = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.pages is not None
    assert client.calls == [OPENTYPE_TOC_URL]
    assert outcome.pages.counts.reused == 3
    assert outcome.pages.counts.downloaded == 0


def test_pages_redownload_corrupt_or_missing_cache(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    first = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert first.pages is not None

    opentype_paths.cache_path("pages/otff.html").write_bytes(b"corrupt")
    client.calls.clear()
    second = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert second.pages is not None
    assert set(client.calls) == {OPENTYPE_TOC_URL, OPENTYPE_OTFF_URL}
    assert second.pages.counts.downloaded == 1
    assert second.pages.counts.reused == 2
    assert second.pages.plan_bytes == first.pages.plan_bytes

    opentype_paths.cache_path("pages/head.html").unlink()
    client.calls.clear()
    third = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert third.pages is not None
    assert set(client.calls) == {OPENTYPE_TOC_URL, OPENTYPE_HEAD_URL}
    assert third.pages.counts.downloaded == 1
    assert third.pages.counts.reused == 2


def test_pages_refresh_downloads_every_page(opentype_paths: SourcePaths) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    client.calls.clear()
    outcome = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=True,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.pages is not None
    assert outcome.pages.counts.downloaded == 3
    assert outcome.pages.counts.reused == 0
    assert set(client.calls) == {
        OPENTYPE_TOC_URL,
        OPENTYPE_LANDING_URL,
        OPENTYPE_OTFF_URL,
        OPENTYPE_HEAD_URL,
    }


def test_pages_dry_run_refreshes_discovery_and_writes_nothing(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    outcome = run_fetch(
        "opentype",
        "pages",
        dry_run=True,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.pages is not None
    assert outcome.pages.dry_run is True
    assert outcome.pages.plan.pages
    assert client.calls[0] == OPENTYPE_TOC_URL
    assert OPENTYPE_IMAGE_URL not in client.calls
    assert not opentype_paths.scratch_root.exists()
    assert not opentype_paths.report_path("pages").exists()


def test_failed_pages_stage_preserves_previous_plan(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    plan_before = opentype_paths.plan_path.read_bytes()

    client.add(
        OPENTYPE_TOC_URL,
        opentype_toc(
            extraitems=[
                {
                    "toc_title": "New page",
                    "href": "opentype/spec/newpage",
                }
            ]
        ),
        content_type="application/json",
    )
    client.fail(OPENTYPE_NEW_URL, 500)
    client.calls.clear()
    with pytest.raises(FetchError):
        run_fetch(
            "opentype",
            "pages",
            dry_run=False,
            refresh=False,
            paths=opentype_paths,
            client=client,
        )
    assert opentype_paths.plan_path.read_bytes() == plan_before
    assert set(client.calls) == {OPENTYPE_TOC_URL, OPENTYPE_NEW_URL}

    report = parse_json_bytes(
        opentype_paths.report_path("pages").read_bytes(),
        what="pages report",
    )
    assert report["success"] is False
    failures = cast("list[object]", report["failures"])
    assert len(failures) == 1


def test_pages_stage_rejects_invalid_utf8(opentype_paths: SourcePaths) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    client.add(OPENTYPE_OTFF_URL, b"\xff\xfe<html>")
    with pytest.raises(FetchError):
        run_fetch(
            "opentype",
            "pages",
            dry_run=False,
            refresh=False,
            paths=opentype_paths,
            client=client,
        )
    assert not opentype_paths.plan_path.exists()


def test_pages_report_records_cache_warnings(opentype_paths: SourcePaths) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    opentype_paths.cache_path("pages/otff.html").write_bytes(b"corrupt")
    client.calls.clear()
    run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    report = parse_json_bytes(
        opentype_paths.report_path("pages").read_bytes(),
        what="pages report",
    )
    assert report["success"] is True
    warnings = cast("list[dict[str, object]]", report["warnings"])
    assert "cache_hash_mismatch" in {warning["kind"] for warning in warnings}


def test_pages_stage_tolerates_bom_and_preserves_cache_bytes(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    body = b"\xef\xbb\xbf" + opentype_page_html(
        "typographydocs/opentype/spec/otff.md",
        "The OpenType Font File",
    )
    client.add(OPENTYPE_OTFF_URL, body)
    outcome = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.pages is not None
    cached = opentype_paths.cache_path("pages/otff.html").read_bytes()
    assert cached == body
    assert cached.startswith(b"\xef\xbb\xbf")


def test_pages_stage_records_srcset_and_data_url_warnings(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    body = opentype_page_html(
        "typographydocs/opentype/spec/otff.md",
        "The OpenType Font File",
        body=(
            '<p>Body</p><img src="images/fig.png" srcset="images/fig2.png 2x">'
            '<img src="data:image/png;base64,AAAA">'
        ),
    )
    client.add(OPENTYPE_OTFF_URL, body)
    outcome = run_fetch(
        "opentype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=opentype_paths,
        client=client,
    )
    assert outcome.pages is not None
    kinds = {warning.kind for warning in outcome.pages.warnings}
    assert "srcset_ignored" in kinds
    assert "data_url_ignored" in kinds
    assert outcome.pages.plan.image_urls == (OPENTYPE_IMAGE_URL,)


def test_truetype_pages_stage_preloads_index_from_discovery(
    truetype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_truetype_pages(client, index_images=["images/fig.png"])
    outcome = run_fetch(
        "truetype",
        "pages",
        dry_run=False,
        refresh=False,
        paths=truetype_paths,
        client=client,
    )
    pages = outcome.pages
    assert pages is not None
    assert [page.slug for page in pages.plan.pages] == [
        "index",
        "AATIntro",
        "OS2",
        "cvt",
    ]
    assert pages.plan.pages[0].title == "Font Tables"
    assert pages.plan.pages[0].last_modified == TRUETYPE_LAST_MODIFIED_ISO
    assert pages.plan.discovery.raw_file == "pages/index.html"
    assert pages.plan.discovery.sha256 == pages.plan.pages[0].sha256
    assert pages.plan.image_urls == (TRUETYPE_IMAGE_URL,)
    assert pages.counts.downloaded == 4
    assert client.calls.count(TRUETYPE_INDEX_URL) == 1
    assert set(client.calls) == {
        TRUETYPE_INDEX_URL,
        TRUETYPE_AAT_URL,
        TRUETYPE_OS2_URL,
        TRUETYPE_CVT_URL,
    }
    assert truetype_paths.cache_path("pages/index.html").is_file()
    assert truetype_paths.cache_path("toc/nav.json").is_file()
    nav = parse_json_bytes(
        truetype_paths.cache_path("toc/nav.json").read_bytes(),
        what="nav audit",
    )
    assert nav["requested_url"] == TRUETYPE_INDEX_URL
