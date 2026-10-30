"""Page validation and image-candidate extraction shared by both stages."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..dom import (
    DomElement,
    attribute_text,
    decode_utf8,
    find_all,
    find_all_with_attribute,
    has_attribute,
    parse_html,
    text_content,
)
from ..errors import FetchError, PageValidationError, SpecMirrorError
from ..notice import Notice, NoticeKind
from ..schema import PageEntry
from ..sources.base import PageCandidate, PageIdentity, SourceAdapter
from ..storage import sha256_bytes
from ..urls import resolve_url
from .models import FetchAction

_BACKGROUND_IMAGE_RE = re.compile(r"background(?:-image)?\s*:[^;]*url\(", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class ParsedPage:
    identity: PageIdentity
    image_urls: tuple[str, ...]
    notices: tuple[Notice, ...]


@dataclass(frozen=True, slots=True)
class ValidatedPage:
    candidate: PageCandidate
    identity: PageIdentity
    body: bytes
    content_type: str
    last_modified: str | None
    image_urls: tuple[str, ...]
    notices: tuple[Notice, ...]
    action: FetchAction


def parse_page(adapter: SourceAdapter, body: bytes, *, page_url: str) -> ParsedPage:
    """Parse a page into its identity and image candidates."""
    text = decode_utf8(body, what=f"page {page_url}")
    document = parse_html(text)
    identity = adapter.page_identity(document, requested_url=page_url)
    roots = adapter.article_roots(document)
    image_urls, notices = _image_candidates(roots, page_url, identity.slug)
    return ParsedPage(
        identity=identity,
        image_urls=image_urls,
        notices=notices,
    )


def validate_page(
    adapter: SourceAdapter,
    candidate: PageCandidate,
    body: bytes,
    *,
    content_type: str | None,
    last_modified: str | None,
    action: FetchAction,
) -> ValidatedPage:
    """Validate the transport facts and content of one page."""
    if not body:
        raise PageValidationError(f"page is empty: {candidate.requested_url}")
    if content_type != "text/html":
        raise PageValidationError(
            f"page media type is {content_type or 'missing'}, expected text/html: "
            f"{candidate.requested_url}"
        )
    parsed = parse_page(adapter, body, page_url=candidate.requested_url)
    return ValidatedPage(
        candidate=candidate,
        identity=parsed.identity,
        body=body,
        content_type=content_type,
        last_modified=last_modified,
        image_urls=parsed.image_urls,
        notices=parsed.notices,
        action=action,
    )


def build_page_entry(adapter: SourceAdapter, page: ValidatedPage) -> PageEntry:
    entry = PageEntry(
        title=page.candidate.title,
        section=page.candidate.section,
        requested_url=page.candidate.requested_url,
        source_path=page.identity.source_path,
        slug=page.identity.slug,
        file=f"pages/{page.identity.slug}.html",
        sha256=sha256_bytes(page.body),
        content_type="text/html",
        last_modified=page.last_modified,
    )
    adapter.validate_page_entry(entry)
    return entry


def check_slug_collisions(pages: list[ValidatedPage]) -> None:
    slugs: dict[str, str] = {}
    for page in pages:
        folded = page.identity.slug.casefold()
        existing = slugs.get(folded)
        if existing is not None:
            raise FetchError(f"slug collision: {existing!r} and {page.identity.slug!r}")
        slugs[folded] = page.identity.slug


def _image_candidates(
    roots: tuple[DomElement, ...],
    page_url: str,
    page_slug: str,
) -> tuple[tuple[str, ...], tuple[Notice, ...]]:
    urls: set[str] = set()
    notices: list[Notice] = []
    style_notice = False
    inline_notice = False
    for root in roots:
        for style_tag in find_all(root, "style"):
            css = text_content(style_tag)
            has_background = (
                "background-image" in css.casefold() or _BACKGROUND_IMAGE_RE.search(css)
            )
            if has_background and not style_notice:
                style_notice = True
                notices.append(
                    Notice(
                        NoticeKind.CSS_BACKGROUND_IMAGE_IGNORED,
                        "CSS background images are not mirrored",
                        page=page_slug,
                        url=page_url,
                    )
                )
        styled = find_all_with_attribute(root, "style")
        for element in (root, *styled):
            style = attribute_text(element, "style")
            has_background = style is not None and _BACKGROUND_IMAGE_RE.search(style)
            if has_background and not inline_notice:
                inline_notice = True
                notices.append(
                    Notice(
                        NoticeKind.CSS_BACKGROUND_IMAGE_IGNORED,
                        "inline CSS background image is not mirrored",
                        page=page_slug,
                        url=page_url,
                    )
                )
        for image in find_all(root, "img"):
            if has_attribute(image, "srcset"):
                notices.append(
                    Notice(
                        NoticeKind.SRCSET_IGNORED,
                        "img srcset is not mirrored; only src is used",
                        page=page_slug,
                        url=page_url,
                    )
                )
            src = attribute_text(image, "src")
            if src is None or not src.strip():
                notices.append(
                    Notice(
                        NoticeKind.IMAGE_WITHOUT_SRC,
                        "img has no usable src",
                        page=page_slug,
                        url=page_url,
                    )
                )
                continue
            raw_src = src.strip()
            if raw_src.casefold().startswith("data:"):
                notices.append(
                    Notice(
                        NoticeKind.DATA_URL_IGNORED,
                        "data URL image is not mirrored",
                        page=page_slug,
                        url=page_url,
                    )
                )
                continue
            try:
                urls.add(resolve_url(page_url, raw_src))
            except SpecMirrorError as error:
                notices.append(
                    Notice(
                        NoticeKind.UNSUPPORTED_IMAGE_URL,
                        f"image src is not an absolute http(s) URL: {error}",
                        page=page_slug,
                        url=page_url,
                    )
                )
    return tuple(sorted(urls)), tuple(notices)
