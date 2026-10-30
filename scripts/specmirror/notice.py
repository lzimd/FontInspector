"""The notices that a stage records about the material it handled."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TypedDict


class NoticeKind(StrEnum):
    """The kinds of notice that the fetch and build stages record."""

    CACHE_HASH_MISMATCH = "cache_hash_mismatch"
    CACHE_IMAGE_REJECTED = "cache_image_rejected"
    CACHE_MISS = "cache_miss"
    CACHE_PAGE_IDENTITY_MISMATCH = "cache_page_identity_mismatch"
    CACHE_PAGE_INVALID = "cache_page_invalid"
    CACHE_READ_FAILED = "cache_read_failed"
    CSS_BACKGROUND_IMAGE_IGNORED = "css_background_image_ignored"
    DATA_URL_IGNORED = "data_url_ignored"
    IGNORED_CSS_DECLARATION = "ignored_css_declaration"
    IMAGE_WITHOUT_SRC = "image_without_src"
    INVALID_LAST_MODIFIED = "invalid_last_modified"
    INVALID_NAVIGATION_HREF = "invalid_navigation_href"
    INVALID_PREVIOUS_MANIFEST = "invalid_previous_manifest"
    INVALID_PREVIOUS_PLAN = "invalid_previous_plan"
    INVALID_TOC_HREF = "invalid_toc_href"
    MISSING_INDEX_TITLE = "missing_index_title"
    MISSING_NAVIGATION_TITLE = "missing_navigation_title"
    SPAN_PLACEHOLDER_INSERTED = "span_placeholder_inserted"
    SRCSET_IGNORED = "srcset_ignored"
    STYLE_EMPHASIS_MAPPED = "style_emphasis_mapped"
    UNDERLINE_DISCARDED = "underline_discarded"
    UNSUPPORTED_IMAGE_URL = "unsupported_image_url"


class NoticeJson(TypedDict, total=False):
    """The serialized form of a notice."""

    kind: str
    message: str
    page: str
    url: str


@dataclass(frozen=True, slots=True)
class Notice:
    kind: NoticeKind
    message: str
    page: str | None = None
    url: str | None = None

    def to_json(self) -> NoticeJson:
        result: NoticeJson = {"kind": self.kind, "message": self.message}
        if self.page is not None:
            result["page"] = self.page
        if self.url is not None:
            result["url"] = self.url
        return result
