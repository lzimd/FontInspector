from __future__ import annotations

import pytest
from helpers import (
    OPENTYPE_HEAD_URL,
    OPENTYPE_LANDING_URL,
    OPENTYPE_OTFF_URL,
    OPENTYPE_TOC_URL,
    TRUETYPE_AAT_URL,
    TRUETYPE_CVT_URL,
    TRUETYPE_INDEX_URL,
    TRUETYPE_OS2_URL,
    opentype_page_html,
    opentype_toc,
    truetype_index_html,
)
from specmirror.dom import parse_html
from specmirror.errors import DiscoveryError, PageValidationError
from specmirror.sources.opentype import FEATURELIST_URL, OpenTypeSource
from specmirror.sources.truetype import TrueTypeSource


def test_opentype_discovery_orders_retains_and_builds_sections() -> None:
    result = OpenTypeSource().parse_discovery(
        opentype_toc(),
        requested_url=OPENTYPE_TOC_URL,
        content_type="application/json",
    )
    assert [candidate.requested_url for candidate in result.candidates] == [
        OPENTYPE_LANDING_URL,
        OPENTYPE_OTFF_URL,
        OPENTYPE_HEAD_URL,
    ]
    assert [candidate.title for candidate in result.candidates] == [
        "OpenType spec",
        "The OpenType font file",
        "head",
    ]
    assert [candidate.section for candidate in result.candidates] == [
        (),
        ("OpenType spec",),
        ("OpenType spec", "Tables"),
    ]


def test_opentype_discovery_adds_featurelist_under_feature_tags() -> None:
    feature_tags: dict[str, object] = {
        "toc_title": "OpenType Layout Tag Registry",
        "children": [
            {
                "toc_title": "Feature tags",
                "href": "opentype/spec/featuretags",
                "children": [
                    {
                        "toc_title": "Feature tags, a-e",
                        "href": "opentype/spec/features_ae",
                    }
                ],
            },
            {
                "toc_title": "Baseline tags",
                "href": "opentype/spec/baselinetags",
            },
        ],
    }
    result = OpenTypeSource().parse_discovery(
        opentype_toc(extraitems=[feature_tags]),
        requested_url=OPENTYPE_TOC_URL,
        content_type="application/json",
    )
    urls = [candidate.requested_url for candidate in result.candidates]
    assert urls == [
        OPENTYPE_LANDING_URL,
        OPENTYPE_OTFF_URL,
        OPENTYPE_HEAD_URL,
        "https://learn.microsoft.com/en-us/typography/opentype/spec/featuretags",
        "https://learn.microsoft.com/en-us/typography/opentype/spec/features_ae",
        FEATURELIST_URL,
        "https://learn.microsoft.com/en-us/typography/opentype/spec/baselinetags",
    ]
    featurelist = next(
        candidate
        for candidate in result.candidates
        if candidate.requested_url == FEATURELIST_URL
    )
    assert featurelist.title == "Registered features"
    assert featurelist.section == ("OpenType Layout Tag Registry", "Feature tags")


def test_opentype_discovery_excludes_archived_subtree_by_title_and_path() -> None:
    extra: list[dict[str, object]] = [
        {
            "toc_title": "Archived versions",
            "children": [
                {
                    "toc_title": "Fake in-scope archive",
                    "href": "opentype/spec/archive/page",
                }
            ],
        },
        {
            "toc_title": "Archived versions",
            "href": "opentype/otspec190/",
        },
    ]
    result = OpenTypeSource().parse_discovery(
        opentype_toc(extraitems=extra),
        requested_url=OPENTYPE_TOC_URL,
        content_type="application/json",
    )
    urls = [candidate.requested_url for candidate in result.candidates]
    assert not any("archive" in url for url in urls)
    assert not any("otspec190" in url for url in urls)


def test_opentype_discovery_keeps_first_duplicate_url() -> None:
    extra: list[dict[str, object]] = [
        {
            "toc_title": "Duplicate otff",
            "href": "opentype/spec/otff",
        }
    ]
    result = OpenTypeSource().parse_discovery(
        opentype_toc(extraitems=extra),
        requested_url=OPENTYPE_TOC_URL,
        content_type="application/json",
    )
    otff = [c for c in result.candidates if c.requested_url == OPENTYPE_OTFF_URL]
    assert len(otff) == 1
    assert otff[0].title == "The OpenType font file"


def test_opentype_discovery_requires_landing_page() -> None:
    with pytest.raises(DiscoveryError):
        OpenTypeSource().parse_discovery(
            opentype_toc(include_landing=False),
            requested_url=OPENTYPE_TOC_URL,
            content_type="application/json",
        )


def test_opentype_page_identity_requires_source_path() -> None:
    adapter = OpenTypeSource()
    soup = parse_html(
        "<html><body><div class='content'><h1>Title</h1></div>"
        "<div class='content'><p>Body</p></div></body></html>"
    )
    with pytest.raises(PageValidationError):
        adapter.page_identity(soup, requested_url=OPENTYPE_OTFF_URL)


def test_opentype_page_identity_derives_index_and_regular_slugs() -> None:
    adapter = OpenTypeSource()
    landing = parse_html(
        opentype_page_html(
            "typographydocs/opentype/spec/index.md",
            "OpenType",
        ).decode()
    )
    identity = adapter.page_identity(landing, requested_url=OPENTYPE_LANDING_URL)
    assert identity.slug == "index"
    assert identity.source_path == "typographydocs/opentype/spec/index.md"

    otff = parse_html(
        opentype_page_html(
            "typographydocs/opentype/spec/otff.md",
            "The OpenType Font File",
        ).decode()
    )
    identity = adapter.page_identity(otff, requested_url=OPENTYPE_OTFF_URL)
    assert identity.slug == "otff"
    assert identity.source_path == "typographydocs/opentype/spec/otff.md"


def test_opentype_article_roots_accepts_two_blocks_and_one_combined_block() -> None:
    adapter = OpenTypeSource()
    two = parse_html(
        opentype_page_html("typographydocs/opentype/spec/otff.md", "Title").decode()
    )
    roots = adapter.article_roots(two)
    assert len(roots) == 2

    one = parse_html(
        "<html><body><div class='content'><h1>Title</h1><p>Body</p></div></body></html>"
    )
    roots = adapter.article_roots(one)
    assert len(roots) == 1


def test_opentype_article_roots_rejects_heading_only_and_multiple_blocks() -> None:
    adapter = OpenTypeSource()
    heading_only = parse_html(
        "<html><body><div class='content'><h1>Title</h1></div></body></html>"
    )
    with pytest.raises(PageValidationError):
        adapter.article_roots(heading_only)

    three = parse_html(
        "<html><body>"
        "<div class='content'><h1>Title</h1></div>"
        "<div class='content'><p>Body</p></div>"
        "<div class='content'><p>Extra</p></div>"
        "</body></html>"
    )
    with pytest.raises(PageValidationError):
        adapter.article_roots(three)


def test_truetype_discovery_adds_index_first_and_retains_chap6_links() -> None:
    result = TrueTypeSource().parse_discovery(
        truetype_index_html(),
        requested_url=TRUETYPE_INDEX_URL,
        content_type="text/html",
    )
    assert [candidate.requested_url for candidate in result.candidates] == [
        TRUETYPE_INDEX_URL,
        TRUETYPE_AAT_URL,
        TRUETYPE_OS2_URL,
        TRUETYPE_CVT_URL,
    ]
    assert [candidate.title for candidate in result.candidates] == [
        "Font Tables",
        "About AAT",
        "'OS/2'",
        "'cvt '",
    ]
    assert all(candidate.section == ("Chapter 6",) for candidate in result.candidates)
    assert len(result.audit_files) == 1
    assert result.audit_files[0].path == "toc/nav.json"


def test_truetype_discovery_requires_navigation() -> None:
    with pytest.raises(DiscoveryError):
        TrueTypeSource().parse_discovery(
            b"<html><body><div id='chapterContent'><h1>Index</h1></div></body></html>",
            requested_url=TRUETYPE_INDEX_URL,
            content_type="text/html",
        )


def test_opentype_discovery_decodes_entities_in_titles() -> None:
    result = OpenTypeSource().parse_discovery(
        opentype_toc(
            extraitems=[
                {
                    "toc_title": "AT&amp;T &quot;fonts&quot;",
                    "href": "opentype/spec/otff2",
                }
            ]
        ),
        requested_url=OPENTYPE_TOC_URL,
        content_type="application/json",
    )
    titles = [candidate.title for candidate in result.candidates]
    assert 'AT&T "fonts"' in titles


def test_truetype_discovery_decodes_entities_once() -> None:
    index = (
        b"<html><head><title>Font Tables</title></head><body>"
        b'<div id="navBar"><ul>'
        b'<li><a href="Chap6AATIntro.html">AT&amp;amp;T fonts</a></li>'
        b"</ul></div>"
        b'<div id="chapterContent"><h1>Font Tables</h1></div>'
        b"</body></html>"
    )
    result = TrueTypeSource().parse_discovery(
        index,
        requested_url=TRUETYPE_INDEX_URL,
        content_type="text/html",
    )
    titles = [candidate.title for candidate in result.candidates]
    assert "AT&amp;T fonts" in titles


def test_truetype_page_identity_preserves_case() -> None:
    adapter = TrueTypeSource()
    soup = parse_html("<html><body><div id='chapterContent'></div></body></html>")
    assert adapter.page_identity(soup, requested_url=TRUETYPE_INDEX_URL).slug == "index"
    assert adapter.page_identity(soup, requested_url=TRUETYPE_OS2_URL).slug == "OS2"
    assert (
        adapter.page_identity(soup, requested_url=TRUETYPE_AAT_URL).slug == "AATIntro"
    )
    assert (
        adapter.page_identity(soup, requested_url=TRUETYPE_CVT_URL).source_path is None
    )
