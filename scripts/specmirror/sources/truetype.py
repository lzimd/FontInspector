"""Apple TrueType Reference Manual Chapter 6 adapter."""

from __future__ import annotations

import re
from urllib.parse import unquote, urlsplit

from ..dom import (
    DomDocument,
    DomElement,
    attribute_text,
    decode_utf8,
    find_all,
    h1_text,
    html_title,
    meta_content,
    parse_html,
    require_single_tag_by_id,
    text_content,
)
from ..errors import (
    DiscoveryError,
    PageValidationError,
    SchemaError,
    ValidationError,
)
from ..notice import Notice, NoticeKind
from ..schema import PageEntry, require_slug
from ..storage import pretty_json_bytes, sha256_bytes
from ..text import normalize_title
from ..urls import normalize_url, resolve_url, url_filename
from .base import (
    AuditFile,
    DiscoveryResult,
    FrontMatterField,
    FrontMatterSpec,
    PageCandidate,
    PageIdentity,
)

APPLEDEV_HOST = "developer.apple.com"
DISCOVERY_URL = (
    "https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6.html"
)
PAGE_PATH_PREFIX = "/fonts/TrueType-Reference-Manual/RM06/"
SECTION = ("Chapter 6",)

_CHAP6_FILENAME_RE = re.compile(r"^Chap6(.*)\.html$")

_FRONT_MATTER_SPEC = FrontMatterSpec(
    title_meta="omni_page",
    order=("title", "author", "last-modified"),
    text_fields=(FrontMatterField("author", "Author", "meta:author"),),
)


class TrueTypeSource:
    key = "truetype"
    display_name = "Apple TrueType Reference Manual, Chapter 6"
    readme_publication = "Chapter 6 of Apple's TrueType Reference Manual"
    readme_scope = (
        "the Chapter 6 pages matching `Chap6*.html`. The mirror excludes "
        "other chapters and site chrome."
    )
    discovery_url = DISCOVERY_URL
    discovery_raw_file = "pages/index.html"
    discovery_is_page = True
    readme_nested_sections = False

    @property
    def front_matter(self) -> FrontMatterSpec:
        return _FRONT_MATTER_SPEC

    def parse_discovery(
        self,
        raw: bytes,
        *,
        requested_url: str,
        content_type: str | None,
    ) -> DiscoveryResult:
        if content_type != "text/html":
            raise DiscoveryError(
                "TrueType discovery is not HTML: "
                f"{content_type or 'missing content type'}"
            )
        text = decode_utf8(raw, what="TrueType index page")
        document = parse_html(text)
        try:
            navigation = require_single_tag_by_id(
                document, "navBar", what="TrueType navigation"
            )
        except PageValidationError as error:
            raise DiscoveryError(str(error)) from error

        warnings: list[Notice] = []
        index_url = normalize_url(requested_url)
        index_title = _document_title(document)
        if index_title is None:
            index_title = "Chapter 6"
            warnings.append(
                Notice(
                    NoticeKind.MISSING_INDEX_TITLE,
                    "index page has no H1, omni_page, or title; using 'Chapter 6'",
                    url=index_url,
                )
            )
        candidates: list[PageCandidate] = [
            PageCandidate(title=index_title, section=SECTION, requested_url=index_url)
        ]
        seen: set[str] = {index_url}
        links: list[dict[str, object]] = []

        for anchor in find_all(navigation, "a"):
            href_value = attribute_text(anchor, "href")
            if href_value is None or not href_value.strip():
                continue
            raw_href = href_value.strip()
            title = normalize_title(text_content(anchor))
            resolved: str | None = None
            retained = False
            try:
                resolved = resolve_url(requested_url, raw_href)
            except ValidationError as error:
                warnings.append(
                    Notice(
                        NoticeKind.INVALID_NAVIGATION_HREF,
                        f"ignored navigation href {raw_href!r}: {error}",
                        url=index_url,
                    )
                )
            if resolved is not None:
                filename = unquote(url_filename(resolved))
                filename_match = _CHAP6_FILENAME_RE.fullmatch(filename)
                retained = filename_match is not None and self.scope_contains(resolved)
                if retained and resolved not in seen:
                    seen.add(resolved)
                    if not title:
                        title = _slug_for_filename(filename)
                        warnings.append(
                            Notice(
                                NoticeKind.MISSING_NAVIGATION_TITLE,
                                f"navigation link has no text; using {title!r}",
                                url=resolved,
                            )
                        )
                    candidates.append(
                        PageCandidate(
                            title=title,
                            section=SECTION,
                            requested_url=resolved,
                        )
                    )
            link_record: dict[str, object] = {
                "title": title,
                "href": raw_href,
                "resolved_url": resolved,
                "retained": retained,
            }
            links.append(link_record)

        if len(candidates) == 1:
            raise DiscoveryError("TrueType navigation has no Chapter 6 page links")

        audit: dict[str, object] = {
            "requested_url": index_url,
            "sha256": sha256_bytes(raw),
            "links": links,
        }
        return DiscoveryResult(
            candidates=tuple(candidates),
            audit_files=(AuditFile("toc/nav.json", pretty_json_bytes(audit)),),
            warnings=tuple(warnings),
        )

    def page_identity(
        self,
        document: DomDocument,
        *,
        requested_url: str,
    ) -> PageIdentity:
        del document
        if not self.scope_contains(requested_url):
            raise PageValidationError(
                f"TrueType page is outside Chapter 6: {requested_url}"
            )
        filename = unquote(url_filename(requested_url))
        slug = _slug_for_filename(filename)
        try:
            require_slug(slug, where="TrueType slug")
        except SchemaError as error:
            raise PageValidationError(str(error)) from error
        return PageIdentity(slug=slug, source_path=None)

    def article_roots(self, document: DomDocument) -> tuple[DomElement, ...]:
        content = require_single_tag_by_id(
            document, "chapterContent", what="TrueType chapter content"
        )
        return (content,)

    def scope_contains(self, url: str) -> bool:
        try:
            parts = urlsplit(normalize_url(url))
        except ValidationError:
            return False
        if parts.hostname != APPLEDEV_HOST:
            return False
        if not parts.path.startswith(PAGE_PATH_PREFIX):
            return False
        filename = unquote(parts.path.rsplit("/", 1)[-1])
        return _CHAP6_FILENAME_RE.fullmatch(filename) is not None

    def validate_page_entry(self, page: PageEntry) -> None:
        if page.content_type != "text/html":
            raise PageValidationError(
                f"TrueType page is not HTML: {page.requested_url}"
            )
        if not self.scope_contains(page.requested_url):
            raise PageValidationError(
                f"TrueType page is outside Chapter 6: {page.requested_url}"
            )
        if page.source_path is not None:
            raise PageValidationError("TrueType pages must not have source_path")
        slug = _slug_for_filename(unquote(url_filename(page.requested_url)))
        if page.slug != slug:
            raise PageValidationError(
                f"TrueType page slug {page.slug!r} does not match its URL"
            )
        if page.file != f"pages/{page.slug}.html":
            raise PageValidationError(
                f"TrueType page file {page.file!r} does not match its slug"
            )
        if page.section != SECTION:
            raise PageValidationError(
                f"TrueType page section must be {list(SECTION)!r}"
            )
        if not page.title:
            raise PageValidationError(
                f"TrueType page has no navigation title: {page.requested_url}"
            )


def _document_title(document: DomDocument) -> str | None:
    """The title of the index page, read from the heading or the metadata."""
    return (
        h1_text(document) or meta_content(document, "omni_page") or html_title(document)
    )


def _slug_for_filename(filename: str) -> str:
    match = _CHAP6_FILENAME_RE.fullmatch(filename)
    if match is None:
        raise PageValidationError(f"not a Chapter 6 page filename: {filename!r}")
    if filename == "Chap6.html":
        return "index"
    slug = match.group(1)
    if not slug:
        raise PageValidationError(f"Chapter 6 page has an empty slug: {filename!r}")
    return slug
