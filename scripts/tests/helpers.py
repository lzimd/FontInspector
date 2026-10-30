"""Shared test fixtures and fake HTTP transport."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass

from specmirror.errors import (
    HttpStatusError,
    HttpTransportError,
    SpecMirrorError,
)
from specmirror.fetch.http import HttpResponse, Redirect
from specmirror.schema import PageEntry
from specmirror.urls import normalize_url

OPENTYPE_TOC_URL = "https://learn.microsoft.com/en-us/typography/toc.json"
OPENTYPE_LANDING_URL = "https://learn.microsoft.com/en-us/typography/opentype/spec/"
OPENTYPE_OTFF_URL = "https://learn.microsoft.com/en-us/typography/opentype/spec/otff"
OPENTYPE_HEAD_URL = "https://learn.microsoft.com/en-us/typography/opentype/spec/head"
OPENTYPE_IMAGE_URL = (
    "https://learn.microsoft.com/en-us/typography/opentype/spec/images/fig.png"
)

TRUETYPE_RM06_URL = "https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/"
TRUETYPE_INDEX_URL = f"{TRUETYPE_RM06_URL}Chap6.html"
TRUETYPE_AAT_URL = (
    "https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/"
    "Chap6AATIntro.html"
)
TRUETYPE_OS2_URL = (
    "https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6OS2.html"
)
TRUETYPE_CVT_URL = (
    "https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6cvt.html"
)
TRUETYPE_IMAGE_URL = (
    "https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/images/fig.png"
)

OPEN_TYPE_LAST_MODIFIED = "Thu, 17 Sep 2026 18:19:04 GMT"
OPEN_TYPE_LAST_MODIFIED_ISO = "2026-09-17T18:19:04Z"
TRUETYPE_LAST_MODIFIED = "Fri, 30 Jan 2026 23:10:21 GMT"
TRUETYPE_LAST_MODIFIED_ISO = "2026-01-30T23:10:21Z"


def make_page_entry(
    slug: str,
    *,
    source: str = "opentype",
    title: str = "Title",
    section: tuple[str, ...] = (),
    last_modified: str | None = OPEN_TYPE_LAST_MODIFIED_ISO,
    sha256: str = "0" * 64,
    requested_url: str | None = None,
) -> PageEntry:
    """A page entry for the schema tests, without a cached snapshot behind it."""
    if requested_url is None:
        if source == "opentype":
            suffix = "" if slug == "index" else slug
            requested_url = f"{OPENTYPE_LANDING_URL}{suffix}"
        else:
            filename = "Chap6.html" if slug == "index" else f"Chap6{slug}.html"
            requested_url = f"{TRUETYPE_RM06_URL}{filename}"
    return PageEntry(
        title=title,
        section=section,
        requested_url=requested_url,
        source_path=(
            f"typographydocs/opentype/spec/{slug}.md" if source == "opentype" else None
        ),
        slug=slug,
        file=f"pages/{slug}.html",
        sha256=sha256,
        content_type="text/html",
        last_modified=last_modified,
    )


@dataclass(frozen=True, slots=True)
class FakeResponse:
    body: bytes
    content_type: str | None = "text/html"
    last_modified: str | None = None
    redirects: tuple[Redirect, ...] = ()
    status: int = 200


class FakeClient:
    def __init__(self) -> None:
        self.responses: dict[str, FakeResponse] = {}
        self.errors: dict[str, SpecMirrorError] = {}
        self.calls: list[str] = []

    def add(
        self,
        url: str,
        body: bytes,
        *,
        content_type: str | None = "text/html",
        last_modified: str | None = None,
        redirects: tuple[Redirect, ...] = (),
        status: int = 200,
    ) -> None:
        self.responses[normalize_url(url)] = FakeResponse(
            body=body,
            content_type=content_type,
            last_modified=last_modified,
            redirects=redirects,
            status=status,
        )

    def add_error(self, url: str, error: SpecMirrorError) -> None:
        self.errors[normalize_url(url)] = error

    def fail(self, url: str, status: int = 500) -> None:
        normalized = normalize_url(url)
        self.add_error(
            normalized,
            HttpStatusError(normalized, status, f"HTTP {status} for {normalized}"),
        )

    def fetch(self, url: str) -> HttpResponse:
        normalized = normalize_url(url)
        self.calls.append(normalized)
        error = self.errors.get(normalized)
        if error is not None:
            raise error
        response = self.responses.get(normalized)
        if response is None:
            raise HttpTransportError(normalized, f"unexpected request: {normalized}")
        headers: dict[str, str] = {}
        if response.content_type is not None:
            headers["content-type"] = response.content_type
        if response.last_modified is not None:
            headers["last-modified"] = response.last_modified
        return HttpResponse(
            requested_url=normalized,
            final_url=normalized,
            status=response.status,
            headers=headers,
            body=response.body,
            redirects=response.redirects,
        )


def opentype_toc(
    *,
    include_landing: bool = True,
    extraitems: Sequence[dict[str, object]] = (),
) -> bytes:
    spec_children: list[dict[str, object]] = [
        {
            "toc_title": "The OpenType font file",
            "href": "opentype/spec/otff",
        },
        {
            "toc_title": "Tables",
            "children": [
                {
                    "toc_title": "head",
                    "href": "opentype/spec/head",
                }
            ],
        },
        {
            "toc_title": "Archived versions",
            "children": [
                {
                    "toc_title": "OpenType Version 1.9",
                    "href": "opentype/otspec190/",
                }
            ],
        },
    ]
    spec_node: dict[str, object] = {
        "toc_title": "OpenType spec",
        "children": spec_children,
    }
    if include_landing:
        spec_node["href"] = "opentype/spec/"
    items: list[dict[str, object]] = [
        {
            "toc_title": "Fonts and typefaces",
            "children": [
                {
                    "toc_title": "Windows 11 font list",
                    "href": "fonts/windows-11",
                }
            ],
        },
        spec_node,
        *extraitems,
    ]
    return json.dumps({"metadata": {}, "items": items}).encode("utf-8")


def opentype_page_html(
    source_path: str,
    title: str,
    *,
    body: str = "<p>Body text.</p>",
    images: Sequence[str] = (),
) -> bytes:
    image_markup = "".join(f'<img src="{src}">' for src in images)
    return (
        "<!DOCTYPE html><html><head>"
        f'<meta name="source_path" content="{source_path}">'
        "</head><body>"
        f'<div class="content"><h1>{title}</h1></div>'
        f'<div class="content">{body}{image_markup}</div>'
        "</body></html>"
    ).encode()


def add_opentype_pages(
    client: FakeClient,
    *,
    otff_images: Sequence[str] = (),
    include_landing: bool = True,
    toc: bytes | None = None,
) -> None:
    client.add(OPENTYPE_TOC_URL, toc or opentype_toc())
    if include_landing:
        client.add(
            OPENTYPE_LANDING_URL,
            opentype_page_html(
                "typographydocs/opentype/spec/index.md",
                "OpenType",
            ),
            last_modified=OPEN_TYPE_LAST_MODIFIED,
        )
    client.add(
        OPENTYPE_OTFF_URL,
        opentype_page_html(
            "typographydocs/opentype/spec/otff.md",
            "The OpenType Font File",
            images=otff_images,
        ),
        last_modified=OPEN_TYPE_LAST_MODIFIED,
    )
    client.add(
        OPENTYPE_HEAD_URL,
        opentype_page_html(
            "typographydocs/opentype/spec/head.md",
            "head",
        ),
        last_modified=OPEN_TYPE_LAST_MODIFIED,
    )


def truetype_index_html(*, images: Sequence[str] = ()) -> bytes:
    image_markup = "".join(f'<img src="{src}">' for src in images)
    return (
        "<!DOCTYPE html><html><head>"
        "<title>Font Tables - TrueType Reference Manual - Apple Developer</title>"
        '<meta name="omni_page" content="TrueType Reference Manual - Font Tables">'
        "</head><body>"
        '<div id="navBar"><ul>'
        '<li><a href="../RM01/Chap1.html">Digitizing Letterforms</a></li>'
        '<li><a href="Chap6AATIntro.html">About AAT</a></li>'
        "<li><a href=\"Chap6OS2.html\"><code>'OS/2'</code></a></li>"
        "<li><a href=\"Chap6OS2.html\"><code>'OS/2'</code></a></li>"
        "<li><a href=\"Chap6cvt.html\"><code>'cvt '</code></a></li>"
        '<li><a href="../RM07/appendixA.html">Instruction Set Summary</a></li>'
        "</ul></div>"
        f'<div id="chapterContent"><header><h1>Font Tables</h1></header>'
        f"<p>Index body.</p>{image_markup}</div>"
        "</body></html>"
    ).encode()


def truetype_page_html(title: str) -> bytes:
    return (
        "<!DOCTYPE html><html><head><title>"
        f"{title} - TrueType Reference Manual - Apple Developer</title>"
        "</head><body>"
        f'<div id="chapterContent"><h1>{title}</h1><p>Body text.</p></div>'
        "</body></html>"
    ).encode()


def add_truetype_pages(
    client: FakeClient,
    *,
    index_images: Sequence[str] = (),
) -> None:
    client.add(
        TRUETYPE_INDEX_URL,
        truetype_index_html(images=index_images),
        last_modified=TRUETYPE_LAST_MODIFIED,
    )
    client.add(
        TRUETYPE_AAT_URL,
        truetype_page_html("About AAT"),
    )
    client.add(
        TRUETYPE_OS2_URL,
        truetype_page_html("OS/2"),
    )
    client.add(
        TRUETYPE_CVT_URL,
        truetype_page_html("cvt"),
    )
