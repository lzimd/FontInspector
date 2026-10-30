from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import pytest
from helpers import (
    OPENTYPE_HEAD_URL,
    OPENTYPE_OTFF_URL,
    OPENTYPE_TOC_URL,
    make_page_entry,
)
from specmirror.errors import PageValidationError, SchemaError
from specmirror.fetch.page_plan import load_page_plan
from specmirror.manifest import load_manifest
from specmirror.paths import SourcePaths
from specmirror.schema import (
    SOURCE_KEYS,
    DiscoveryEntry,
    ImageEntry,
    Manifest,
    PageEntry,
    PagePlan,
    parse_json_bytes,
)
from specmirror.sources import get_source, source_keys

DIGEST = "a" * 64


def make_page(
    slug: str,
    url: str,
    *,
    title: str = "Title",
    section: tuple[str, ...] = ("OpenType spec",),
    last_modified: str | None = "2026-09-17T18:19:04Z",
) -> PageEntry:
    return make_page_entry(
        slug,
        source="opentype",
        title=title,
        section=section,
        last_modified=last_modified,
        sha256=DIGEST,
        requested_url=url,
    )


def make_manifest() -> Manifest:
    return Manifest(
        source="opentype",
        discovery=DiscoveryEntry(
            requested_url=OPENTYPE_TOC_URL,
            raw_file="toc/toc.json",
            sha256=DIGEST,
        ),
        pages=(
            make_page("otff", OPENTYPE_OTFF_URL),
            make_page("head", OPENTYPE_HEAD_URL, title="head"),
        ),
        images=(
            ImageEntry(
                requested_url="https://example.com/images/a.png",
                file="images/a.png",
                sha256=DIGEST,
                content_type="image/png",
            ),
        ),
    )


def test_manifest_snapshot_roundtrip_and_stability() -> None:
    manifest = make_manifest()
    first = manifest.snapshot_sha256()
    assert first == make_manifest().snapshot_sha256()
    data = manifest.to_dict()
    assert data["snapshot_sha256"] == first

    restored = Manifest.from_dict(data, expected_source="opentype")
    assert restored == manifest
    assert restored.snapshot_sha256() == first


def test_manifest_rejects_tampered_content_and_snapshot() -> None:
    data = make_manifest().to_dict()
    pages = cast("list[dict[str, object]]", data["pages"])
    pages[0]["title"] = "Changed"
    with pytest.raises(SchemaError):
        Manifest.from_dict(data, expected_source="opentype")

    data = make_manifest().to_dict()
    data["snapshot_sha256"] = "b" * 64
    with pytest.raises(SchemaError):
        Manifest.from_dict(data, expected_source="opentype")


def test_manifest_rejects_unknown_keys_and_wrong_source() -> None:
    data = make_manifest().to_dict()
    data["extra"] = True
    with pytest.raises(SchemaError):
        Manifest.from_dict(data, expected_source="opentype")

    with pytest.raises(SchemaError):
        Manifest.from_dict(make_manifest().to_dict(), expected_source="truetype")


def test_manifest_rejects_unsorted_images_and_slug_collisions() -> None:
    manifest = Manifest(
        source="opentype",
        discovery=make_manifest().discovery,
        pages=(),
        images=(
            ImageEntry(
                requested_url="https://example.com/images/z.png",
                file="images/z.png",
                sha256=DIGEST,
                content_type="image/png",
            ),
            ImageEntry(
                requested_url="https://example.com/images/a.png",
                file="images/a.png",
                sha256=DIGEST,
                content_type="image/png",
            ),
        ),
    )
    with pytest.raises(SchemaError):
        Manifest.from_dict(manifest.to_dict(), expected_source="opentype")

    colliding = Manifest(
        source="opentype",
        discovery=make_manifest().discovery,
        pages=(
            make_page("Foo", "https://example.com/Foo"),
            make_page("foo", "https://example.com/foo"),
        ),
        images=(),
    )
    with pytest.raises(SchemaError):
        Manifest.from_dict(colliding.to_dict(), expected_source="opentype")


def test_page_entry_rejects_parameterized_media_type() -> None:
    data = make_page("otff", OPENTYPE_OTFF_URL).to_dict()
    data["content_type"] = "text/html; charset=utf-8"
    with pytest.raises(SchemaError):
        PageEntry.from_dict(data)


def test_page_entry_rejects_parameterized_last_modified() -> None:
    data = make_page("otff", OPENTYPE_OTFF_URL).to_dict()
    data["last_modified"] = "2026-09-17T18:19:04+00:00"
    with pytest.raises(SchemaError):
        PageEntry.from_dict(data)


def test_opentype_adapter_rejects_bad_source_path() -> None:
    page = make_page("otff", OPENTYPE_OTFF_URL)
    bad = PageEntry(
        title=page.title,
        section=page.section,
        requested_url=page.requested_url,
        source_path="elsewhere/otff.md",
        slug=page.slug,
        file=page.file,
        sha256=page.sha256,
        content_type=page.content_type,
        last_modified=page.last_modified,
    )
    with pytest.raises(PageValidationError):
        get_source("opentype").validate_page_entry(bad)


def test_page_plan_roundtrip_and_sorted_image_urls() -> None:
    plan = PagePlan(
        source="opentype",
        discovery=make_manifest().discovery,
        pages=make_manifest().pages,
        image_urls=(
            "https://example.com/images/a.png",
            "https://example.com/images/b.png",
        ),
    )
    restored = PagePlan.from_dict(plan.to_dict(), expected_source="opentype")
    assert restored == plan

    data = plan.to_dict()
    data["image_urls"] = [
        "https://example.com/images/b.png",
        "https://example.com/images/a.png",
    ]
    with pytest.raises(SchemaError):
        PagePlan.from_dict(data, expected_source="opentype")


def test_page_plan_loader_rejects_noncanonical_json(tmp_path: Path) -> None:
    paths = SourcePaths(root=tmp_path, source="opentype")
    plan = PagePlan(
        source="opentype",
        discovery=make_manifest().discovery,
        pages=make_manifest().pages,
        image_urls=(),
    )
    paths.plan_path.parent.mkdir(parents=True)
    paths.plan_path.write_text(
        json.dumps(plan.to_dict(), indent=2) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(SchemaError):
        load_page_plan(
            paths.plan_path,
            expected_source="opentype",
            required=True,
        )


def test_manifest_loader_verifies_snapshot(tmp_path: Path) -> None:
    paths = SourcePaths(root=tmp_path, source="opentype")
    manifest = make_manifest()
    paths.manifest_path.parent.mkdir(parents=True)
    paths.manifest_path.write_bytes(manifest.to_bytes())
    loaded = load_manifest(
        paths.manifest_path,
        expected_source="opentype",
        required=True,
    )
    assert loaded is not None
    assert loaded.manifest == manifest

    data = manifest.to_dict()
    data["snapshot_sha256"] = "b" * 64
    paths.manifest_path.write_bytes(
        (json.dumps(data, separators=(",", ":")) + "\n").encode()
    )
    with pytest.raises(SchemaError):
        load_manifest(
            paths.manifest_path,
            expected_source="opentype",
            required=True,
        )


def test_parse_json_bytes_rejects_invalid_utf8_and_json() -> None:
    with pytest.raises(SchemaError):
        parse_json_bytes(b"\xff", what="test")
    with pytest.raises(SchemaError):
        parse_json_bytes(b"{", what="test")


def test_source_keys_match_the_adapter_registry() -> None:
    assert source_keys() == SOURCE_KEYS
