"""Microsoft Learn OpenType specification adapter."""

from __future__ import annotations

import json
from urllib.parse import urlsplit

from ..dom import (
    DomDocument,
    DomElement,
    decode_utf8,
    find,
    find_all_with_class,
    has_content_beyond_h1,
    meta_content,
)
from ..errors import (
    DiscoveryError,
    PageValidationError,
    SchemaError,
    ValidationError,
)
from ..notice import Notice, NoticeKind
from ..schema import (
    PageEntry,
    is_json_array,
    is_json_object,
    require_object,
    require_slug,
)
from ..storage import safe_relative_path
from ..text import normalize_escaped_title
from ..urls import normalize_url, resolve_url
from .base import (
    DiscoveryResult,
    FrontMatterField,
    FrontMatterSpec,
    PageCandidate,
    PageIdentity,
)

MSDOC_HOST = "learn.microsoft.com"
DISCOVERY_URL = "https://learn.microsoft.com/en-us/typography/toc.json"
SPEC_PATH_PREFIX = "/en-us/typography/opentype/spec/"
SOURCE_PATH_PREFIX = "typographydocs/opentype/spec/"
FEATURELIST_URL = (
    "https://learn.microsoft.com/en-us/typography/opentype/spec/featurelist"
)
_FEATURE_TAGS_TITLE = "Feature tags"
_FEATURELIST_TITLE = "Registered features"

_ARCHIVE_PATH_TOKENS = ("/otspec", "/archive", "opentypeversions")

_FRONT_MATTER_SPEC = FrontMatterSpec(
    title_meta="og:title",
    order=(
        "title",
        "description",
        "author",
        "ms.date",
        "updated_at",
        "upstream_gitcommit",
        "last-modified",
    ),
    text_fields=(
        FrontMatterField("description", "description", "meta:description"),
        FrontMatterField("author", "author", "meta:author"),
    ),
    timestamp_fields=(
        FrontMatterField("ms.date", "ms.date", "meta:ms.date"),
        FrontMatterField("updated_at", "updated_at", "meta:updated_at"),
    ),
    gitcommit=True,
)


class OpenTypeSource:
    key = "opentype"
    display_name = "OpenType specification"
    readme_publication = (
        "the current OpenType specification published by Microsoft Learn"
    )
    readme_scope = (
        "the current specification pages under the "
        "`/en-us/typography/opentype/spec/` prefix. The mirror excludes "
        "archived versions and site chrome."
    )
    discovery_url = DISCOVERY_URL
    discovery_raw_file = "toc/toc.json"
    discovery_is_page = False
    readme_nested_sections = True

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
        del content_type
        text = decode_utf8(raw, what="OpenType TOC")
        try:
            root = json.loads(text)
        except json.JSONDecodeError as error:
            raise DiscoveryError(f"OpenType TOC is not valid JSON: {error}") from error
        nodes = _root_nodes(root)
        candidates: list[PageCandidate] = []
        seen: set[str] = set()
        warnings: list[Notice] = []

        def walk(
            entries: list[dict[str, object]],
            ancestors: tuple[str, ...],
        ) -> None:
            for node in entries:
                title_value = node.get("toc_title")
                title = (
                    normalize_escaped_title(title_value)
                    if isinstance(title_value, str)
                    else ""
                )
                href_value = node.get("href")
                url: str | None = None
                if isinstance(href_value, str) and href_value.strip():
                    try:
                        url = resolve_url(requested_url, href_value.strip())
                    except ValidationError as error:
                        warnings.append(
                            Notice(
                                NoticeKind.INVALID_TOC_HREF,
                                f"ignored TOC href {href_value!r}: {error}",
                            )
                        )
                path = urlsplit(url).path if url is not None else ""
                if _is_archived(title, path):
                    continue
                if url is not None and self.scope_contains(url):
                    if not title:
                        raise DiscoveryError(
                            f"retained OpenType TOC node has no title: {url}"
                        )
                    if url not in seen:
                        seen.add(url)
                        candidates.append(
                            PageCandidate(
                                title=title,
                                section=ancestors,
                                requested_url=url,
                            )
                        )
                children_value = node.get("children")
                if children_value is None:
                    continue
                children = _node_list(children_value, "TOC children")
                child_ancestors = ancestors + ((title,) if title else ())
                walk(children, child_ancestors)

        walk(nodes, ())
        if not any(
            _is_landing_url(candidate.requested_url) for candidate in candidates
        ):
            raise DiscoveryError(
                "OpenType specification landing page is missing from the TOC"
            )
        if FEATURELIST_URL not in seen:
            feature_tags = next(
                (
                    candidate
                    for candidate in candidates
                    if candidate.title.casefold() == _FEATURE_TAGS_TITLE.casefold()
                ),
                None,
            )
            if feature_tags is not None:
                child_section = (*feature_tags.section, feature_tags.title)
                insert_at = len(candidates)
                for index, candidate in enumerate(candidates):
                    if candidate.section == child_section:
                        insert_at = index + 1
                candidates.insert(
                    insert_at,
                    PageCandidate(
                        title=_FEATURELIST_TITLE,
                        section=child_section,
                        requested_url=FEATURELIST_URL,
                    ),
                )
        return DiscoveryResult(
            candidates=tuple(candidates),
            warnings=tuple(warnings),
        )

    def page_identity(
        self,
        document: DomDocument,
        *,
        requested_url: str,
    ) -> PageIdentity:
        if not self.scope_contains(requested_url):
            raise PageValidationError(
                f"OpenType page is outside the specification scope: {requested_url}"
            )
        source_path = meta_content(document, "source_path")
        if source_path is None:
            raise PageValidationError(
                f"OpenType page has no meta source_path: {requested_url}"
            )
        if not source_path.startswith(SOURCE_PATH_PREFIX):
            raise PageValidationError(
                "OpenType source_path is outside the specification scope: "
                f"{source_path}"
            )
        slug = _derive_slug_from_source_path(source_path, where="OpenType source_path")
        return PageIdentity(slug=slug, source_path=source_path)

    def article_roots(self, document: DomDocument) -> tuple[DomElement, ...]:
        blocks = find_all_with_class(document, "div", "content")
        if len(blocks) == 1:
            block = blocks[0]
            if find(block, "h1") is None or not has_content_beyond_h1(block):
                raise PageValidationError(
                    "OpenType content block must contain the H1 and the article body"
                )
            return (block,)
        if len(blocks) == 2:
            heading_blocks = [
                block for block in blocks if find(block, "h1") is not None
            ]
            if len(heading_blocks) != 1:
                raise PageValidationError(
                    "OpenType page must have exactly one H1-bearing content block"
                )
            heading_block = heading_blocks[0]
            body_block = blocks[1] if blocks[0] is heading_block else blocks[0]
            return (heading_block, body_block)
        raise PageValidationError(
            f"OpenType page has {len(blocks)} div.content blocks; expected one or two"
        )

    def scope_contains(self, url: str) -> bool:
        try:
            parts = urlsplit(normalize_url(url))
        except ValidationError:
            return False
        if parts.hostname != MSDOC_HOST:
            return False
        path = parts.path
        return path == SPEC_PATH_PREFIX.rstrip("/") or path.startswith(SPEC_PATH_PREFIX)

    def validate_page_entry(self, page: PageEntry) -> None:
        if page.content_type != "text/html":
            raise PageValidationError(
                f"OpenType page is not HTML: {page.requested_url}"
            )
        if not self.scope_contains(page.requested_url):
            raise PageValidationError(
                "OpenType page is outside the specification scope: "
                f"{page.requested_url}"
            )
        if page.source_path is None:
            raise PageValidationError(
                f"OpenType page has no source_path: {page.requested_url}"
            )
        if not page.source_path.startswith(SOURCE_PATH_PREFIX):
            raise PageValidationError(
                "OpenType source_path is outside the specification scope: "
                f"{page.source_path}"
            )
        expected_slug = _derive_slug_from_source_path(
            page.source_path, where="OpenType source_path"
        )
        if page.slug != expected_slug:
            raise PageValidationError(
                f"OpenType page slug {page.slug!r} does not match source_path"
            )
        if page.file != f"pages/{page.slug}.html":
            raise PageValidationError(
                f"OpenType page file {page.file!r} does not match its slug"
            )
        if not page.title:
            raise PageValidationError(
                f"OpenType page has no navigation title: {page.requested_url}"
            )


def _derive_slug_from_source_path(source_path: str, *, where: str) -> str:
    """Derive the page slug from the upstream source path."""
    path = source_path.strip()
    try:
        pure = safe_relative_path(path, where=where)
    except ValidationError as error:
        raise PageValidationError(str(error)) from error
    if not pure.name.endswith(".md"):
        raise PageValidationError(f"{where} must end with .md")
    slug = pure.name[: -len(".md")]
    if not slug:
        raise PageValidationError(f"{where} has an empty slug")
    try:
        return require_slug(slug, where=f"{where} slug")
    except SchemaError as error:
        raise PageValidationError(str(error)) from error


def _root_nodes(root: object) -> list[dict[str, object]]:
    if is_json_array(root):
        return _node_list(root, "TOC items")
    if is_json_object(root):
        data = _as_dict(root, "OpenType TOC")
        items = data.get("items")
        if is_json_array(items):
            return _node_list(items, "TOC items")
        children = data.get("children")
        if is_json_array(children):
            return _node_list(children, "TOC children")
        raise DiscoveryError("OpenType TOC has no items")
    raise DiscoveryError("OpenType TOC root must be an object or an array")


def _node_list(value: object, where: str) -> list[dict[str, object]]:
    if not is_json_array(value):
        raise DiscoveryError(f"{where} must be an array")
    result: list[dict[str, object]] = []
    for index, item in enumerate(value):
        result.append(_as_dict(item, f"{where}[{index}]"))
    return result


def _as_dict(value: object, where: str) -> dict[str, object]:
    try:
        return require_object(value, where)
    except SchemaError as error:
        raise DiscoveryError(str(error)) from error


def _is_archived(title: str, path: str) -> bool:
    folded_path = path.casefold()
    return "archived" in title.casefold() or any(
        token in folded_path for token in _ARCHIVE_PATH_TOKENS
    )


def _is_landing_url(url: str) -> bool:
    path = urlsplit(normalize_url(url)).path
    return path in {SPEC_PATH_PREFIX, SPEC_PATH_PREFIX.rstrip("/")}
