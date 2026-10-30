"""Link, image, and fragment mapping over the page AST."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from ..convert.ast import (
    Block,
    BlockQuote,
    Code,
    Emphasis,
    Heading,
    Image,
    Inline,
    Link,
    List,
    PageAst,
    Paragraph,
    RawHtml,
    Strikethrough,
    Strong,
    Table,
    Text,
)
from ..errors import BuildError, ValidationError
from ..schema import Manifest
from ..urls import normalize_url


@dataclass(slots=True)
class LinkRecord:
    page: str
    href: str
    outcome: str  # `external`, `externalized`, or `missing-fragment`
    detail: str


def _new_link_records() -> list[LinkRecord]:
    return []


def _new_alias_hits() -> list[str]:
    return []


@dataclass(slots=True)
class PageMaps:
    """Cross-page lookups shared by every page of one build."""

    page_by_url: dict[str, str]
    fragment_maps: dict[str, dict[str, str]]
    images: dict[str, str]
    link_records: list[LinkRecord] = field(default_factory=_new_link_records)
    alias_hits: list[str] = field(default_factory=_new_alias_hits)


def build_page_maps(manifest: Manifest, asts: dict[str, PageAst]) -> PageMaps:
    page_by_url = {
        normalize_url(page.requested_url): page.slug for page in manifest.pages
    }
    fragment_maps = {slug: ast.fragment_map for slug, ast in asts.items()}
    images = {
        normalize_url(image.requested_url): image.file for image in manifest.images
    }
    return PageMaps(
        page_by_url=page_by_url,
        fragment_maps=fragment_maps,
        images=images,
    )


def map_page_links(
    blocks: list[Block],
    page_ast: PageAst,
    *,
    page: str,
    scope_contains: Callable[[str], bool],
    maps: PageMaps,
) -> None:
    del page_ast
    _rewrite_blocks(blocks, page=page, scope_contains=scope_contains, maps=maps)


def check_anchor_uniqueness(
    page_ast: PageAst, document_blocks: list[Block], page: str
) -> None:
    seen: dict[str, str] = {}
    for group in page_ast.anchor_groups:
        if group.canonical_id is None:
            continue
        if group.canonical_id in seen:
            raise BuildError(f"anchor collision {group.canonical_id!r} on page {page}")
        seen[group.canonical_id] = "anchor"
    for anchor in _nested_anchor_ids(document_blocks):
        if anchor in seen:
            raise BuildError(f"nested anchor collision {anchor!r} on page {page}")
        seen[anchor] = "nested"


def _nested_anchor_ids(blocks: list[Block]) -> list[str]:
    anchors: list[str] = []
    for block in blocks:
        if isinstance(block, Table):
            for nested in block.nested_tables:
                anchors.append(nested.anchor_id)
                anchors.extend(_nested_anchor_ids([nested.table]))
    return anchors


def _rewrite_blocks(
    blocks: list[Block],
    *,
    page: str,
    scope_contains: Callable[[str], bool],
    maps: PageMaps,
) -> None:
    for block in blocks:
        if isinstance(block, (Paragraph, Heading)):
            _rewrite_inlines(
                block.inlines, page=page, scope_contains=scope_contains, maps=maps
            )
        elif isinstance(block, BlockQuote):
            _rewrite_blocks(
                block.blocks, page=page, scope_contains=scope_contains, maps=maps
            )
        elif isinstance(block, List):
            for item in block.items:
                _rewrite_blocks(
                    item.blocks, page=page, scope_contains=scope_contains, maps=maps
                )
        elif isinstance(block, Table):
            if block.caption is not None:
                _rewrite_inlines(
                    block.caption,
                    page=page,
                    scope_contains=scope_contains,
                    maps=maps,
                )
            for row in [*block.header.rows, *block.rows]:
                for cell in row.cells:
                    _rewrite_blocks(
                        cell.blocks, page=page, scope_contains=scope_contains, maps=maps
                    )
            for nested in block.nested_tables:
                _rewrite_blocks(
                    [nested.table], page=page, scope_contains=scope_contains, maps=maps
                )


def _rewrite_inlines(
    inlines: list[Inline],
    *,
    page: str,
    scope_contains: Callable[[str], bool],
    maps: PageMaps,
) -> None:
    for inline in inlines:
        if isinstance(inline, Link):
            inline.href = _rewrite_link(
                inline.href, page=page, scope_contains=scope_contains, maps=maps
            )
        elif isinstance(inline, Image):
            inline.src = _rewrite_image(inline.src, page=page, maps=maps)
        elif isinstance(inline, (Emphasis, Strong, Strikethrough)):
            _rewrite_inlines(
                inline.inlines, page=page, scope_contains=scope_contains, maps=maps
            )
        elif isinstance(inline, (Text, Code, RawHtml)):
            continue


def _rewrite_link(
    href: str,
    *,
    page: str,
    scope_contains: Callable[[str], bool],
    maps: PageMaps,
) -> str:
    if href.startswith("#"):
        return href
    parts = urlsplit(href)
    base = href.split("#", 1)[0]
    fragment = parts.fragment
    slug = _page_for(base, maps)
    if slug is not None:
        if fragment:
            local = maps.fragment_maps.get(slug, {}).get(fragment)
            if local is None:
                maps.link_records.append(
                    LinkRecord(
                        page=page,
                        href=href,
                        outcome="missing-fragment",
                        detail=f"fragment {fragment!r} has no local anchor on {slug}",
                    )
                )
                return f"{slug}.md"
            if slug == page:
                return f"#{local}"
            return f"{slug}.md#{local}"
        if slug != page:
            return f"{slug}.md"
        maps.link_records.append(
            LinkRecord(
                page=page,
                href=href,
                outcome="external",
                detail="same-page link without a fragment",
            )
        )
        return f"{page}.md"
    if scope_contains(base):
        maps.link_records.append(
            LinkRecord(
                page=page,
                href=href,
                outcome="externalized",
                detail="in-scope URL is missing from the manifest",
            )
        )
        return base
    maps.link_records.append(
        LinkRecord(page=page, href=href, outcome="external", detail="")
    )
    return href


def _rewrite_image(src: str, *, page: str, maps: PageMaps) -> str:
    if "://" not in src:
        return src
    try:
        normalized = normalize_url(src)
    except ValidationError as error:
        raise BuildError(f"image URL is invalid: {src} on page {page}") from error
    file = maps.images.get(normalized)
    if file is None:
        raise BuildError(f"image is missing from the manifest: {src} on page {page}")
    return file


def _page_for(base: str, maps: PageMaps) -> str | None:
    if not base:
        return None
    parts = urlsplit(base)
    if parts.scheme and parts.scheme.casefold() not in {"http", "https"}:
        return None
    try:
        normalized = normalize_url(base)
    except ValidationError:
        return None
    slug = maps.page_by_url.get(normalized)
    if slug is not None:
        return slug
    alias = normalized[:-1] if normalized.endswith("/") else normalized + "/"
    slug = maps.page_by_url.get(alias)
    if slug is not None:
        maps.alias_hits.append(normalized)
        return slug
    return None


__all__ = [
    "LinkRecord",
    "PageMaps",
    "build_page_maps",
    "check_anchor_uniqueness",
    "map_page_links",
]
