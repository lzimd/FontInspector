"""Shared source-adapter data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from ..dom import DomDocument, DomElement
from ..notice import Notice
from ..schema import PageEntry


@dataclass(frozen=True, slots=True)
class PageCandidate:
    title: str
    section: tuple[str, ...]
    requested_url: str


@dataclass(frozen=True, slots=True)
class PageIdentity:
    slug: str
    source_path: str | None


@dataclass(frozen=True, slots=True)
class AuditFile:
    path: str
    data: bytes


@dataclass(frozen=True, slots=True)
class DiscoveryResult:
    candidates: tuple[PageCandidate, ...]
    audit_files: tuple[AuditFile, ...] = ()
    warnings: tuple[Notice, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class FrontMatterField:
    """One metadata field that a source contributes to front matter."""

    field: str
    meta_name: str
    provenance: str


@dataclass(frozen=True, slots=True)
class FrontMatterSpec:
    """How one source fills the front matter of its pages."""

    title_meta: str
    order: tuple[str, ...]
    text_fields: tuple[FrontMatterField, ...] = ()
    timestamp_fields: tuple[FrontMatterField, ...] = ()
    gitcommit: bool = False


class SourceAdapter(Protocol):
    @property
    def key(self) -> str: ...

    @property
    def display_name(self) -> str: ...

    @property
    def readme_publication(self) -> str: ...

    @property
    def readme_scope(self) -> str: ...

    @property
    def discovery_url(self) -> str: ...

    @property
    def discovery_raw_file(self) -> str: ...

    @property
    def discovery_is_page(self) -> bool: ...

    @property
    def front_matter(self) -> FrontMatterSpec: ...

    @property
    def readme_nested_sections(self) -> bool: ...

    def parse_discovery(
        self,
        raw: bytes,
        *,
        requested_url: str,
        content_type: str | None,
    ) -> DiscoveryResult: ...

    def page_identity(
        self,
        document: DomDocument,
        *,
        requested_url: str,
    ) -> PageIdentity: ...

    def article_roots(self, document: DomDocument) -> tuple[DomElement, ...]: ...

    def scope_contains(self, url: str) -> bool: ...

    def validate_page_entry(self, page: PageEntry) -> None: ...
