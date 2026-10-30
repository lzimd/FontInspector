"""Snapshot schema, canonical JSON, and strict artifact validation."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TypeGuard

from .errors import SchemaError, ValidationError
from .storage import (
    canonical_document_bytes,
    canonical_json_bytes,
    safe_relative_path,
    sha256_bytes,
)
from .urls import normalize_url

SCHEMA_VERSION = 1
SOURCE_KEYS: tuple[str, ...] = ("opentype", "truetype")

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_MEDIA_TYPE_RE = re.compile(r"^[a-z0-9][a-z0-9!#$&^_.+-]*/[a-z0-9][a-z0-9!#$&^_.+-]*$")
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def parse_json_bytes(data: bytes, *, what: str) -> dict[str, object]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise SchemaError(f"{what} is not valid UTF-8") from error
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise SchemaError(f"{what} is not valid JSON: {error}") from error
    return require_object(value, what)


def require_slug(value: object, *, where: str) -> str:
    slug = require_text(value, where)
    if not _SLUG_RE.fullmatch(slug):
        raise SchemaError(f"{where} is not a valid slug: {slug!r}")
    return slug


def _require_sha256(value: object, *, where: str) -> str:
    digest = require_text(value, where)
    if not _SHA256_RE.fullmatch(digest):
        raise SchemaError(f"{where} is not a lowercase SHA-256 digest")
    return digest


def _require_url(value: object, *, where: str) -> str:
    url = require_text(value, where)
    try:
        normalized = normalize_url(url)
    except ValidationError as error:
        raise SchemaError(f"{where}: {error}") from error
    if normalized != url:
        raise SchemaError(f"{where} is not a normalized absolute URL: {url!r}")
    return url


def require_text(value: object, where: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise SchemaError(f"{where} must be a string")
    if any(ord(character) < 0x20 or ord(character) == 0x7F for character in value):
        raise SchemaError(f"{where} contains a control character")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        raise SchemaError(f"{where} contains a surrogate code point")
    if not allow_empty and not value:
        raise SchemaError(f"{where} must not be empty")
    return value


def _require_int(value: object, where: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise SchemaError(f"{where} must be an integer")
    return value


def require_positive_int(value: object, where: str) -> int:
    number = _require_int(value, where)
    if number < 1:
        raise SchemaError(f"{where} must be a positive integer")
    return number


def _require_relative_path(
    value: object,
    where: str,
    *,
    prefix: str | None = None,
    single_component_after_prefix: bool = False,
) -> str:
    path = require_text(value, where)
    if path.endswith("/"):
        raise SchemaError(f"{where} must name a file")
    try:
        safe_relative_path(path, where=where)
    except ValidationError as error:
        raise SchemaError(str(error)) from error
    if prefix is not None:
        if not path.startswith(prefix):
            raise SchemaError(f"{where} must start with {prefix!r}")
        if single_component_after_prefix:
            remainder = path[len(prefix) :]
            if not remainder or "/" in remainder:
                raise SchemaError(f"{where} must name a single file under {prefix!r}")
    return path


def require_media_type(value: object, where: str) -> str:
    media_type = require_text(value, where)
    if not _MEDIA_TYPE_RE.fullmatch(media_type):
        raise SchemaError(f"{where} is not a bare media type: {media_type!r}")
    return media_type


def _require_timestamp(value: object, where: str) -> str:
    timestamp = require_text(value, where)
    if not _TIMESTAMP_RE.fullmatch(timestamp):
        raise SchemaError(f"{where} is not an RFC 3339 UTC timestamp")
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError as error:
        raise SchemaError(f"{where} is not a valid timestamp") from error
    return timestamp


def _optional_timestamp(value: object, where: str) -> str | None:
    if value is None:
        return None
    return _require_timestamp(value, where)


def _require_section(value: object, where: str) -> tuple[str, ...]:
    if not is_json_array(value):
        raise SchemaError(f"{where} must be an array")
    section: list[str] = []
    for index, item in enumerate(value):
        section.append(require_text(item, f"{where}[{index}]"))
    return tuple(section)


def is_json_object(value: object) -> TypeGuard[dict[str, object]]:
    """Whether the value is a JSON object."""
    return isinstance(value, dict)


def is_json_array(value: object) -> TypeGuard[list[object]]:
    """Whether the value is a JSON array."""
    return isinstance(value, list)


def require_object(value: object, where: str) -> dict[str, object]:
    """Decode a JSON object into a string-keyed mapping."""
    if not is_json_object(value):
        raise SchemaError(f"{where} must be an object")
    return value


def _require_array(value: object, where: str) -> list[object]:
    if not is_json_array(value):
        raise SchemaError(f"{where} must be an array")
    return value


def _check_keys(
    value: dict[str, object],
    *,
    where: str,
    required: set[str],
    optional: frozenset[str] = frozenset(),
) -> None:
    missing = sorted(required - value.keys())
    unknown = sorted(value.keys() - required - optional)
    if missing:
        raise SchemaError(f"{where} is missing keys: {', '.join(missing)}")
    if unknown:
        raise SchemaError(f"{where} has unknown keys: {', '.join(unknown)}")


@dataclass(frozen=True, slots=True)
class DiscoveryEntry:
    requested_url: str
    raw_file: str
    sha256: str

    def to_dict(self) -> dict[str, object]:
        return {
            "requested_url": self.requested_url,
            "raw_file": self.raw_file,
            "sha256": self.sha256,
        }

    @classmethod
    def from_dict(cls, value: object, *, where: str = "discovery") -> DiscoveryEntry:
        data = require_object(value, where)
        _check_keys(data, where=where, required={"requested_url", "raw_file", "sha256"})
        return cls(
            requested_url=_require_url(
                data["requested_url"], where=f"{where}.requested_url"
            ),
            raw_file=_require_relative_path(data["raw_file"], f"{where}.raw_file"),
            sha256=_require_sha256(data["sha256"], where=f"{where}.sha256"),
        )


@dataclass(frozen=True, slots=True)
class PageEntry:
    title: str
    section: tuple[str, ...]
    requested_url: str
    source_path: str | None
    slug: str
    file: str
    sha256: str
    content_type: str
    last_modified: str | None

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "title": self.title,
            "section": list(self.section),
            "requested_url": self.requested_url,
            "slug": self.slug,
            "file": self.file,
            "sha256": self.sha256,
            "content_type": self.content_type,
            "last_modified": self.last_modified,
        }
        if self.source_path is not None:
            result["source_path"] = self.source_path
        return result

    @classmethod
    def from_dict(cls, value: object, *, where: str = "page") -> PageEntry:
        data = require_object(value, where)
        _check_keys(
            data,
            where=where,
            required={
                "title",
                "section",
                "requested_url",
                "slug",
                "file",
                "sha256",
                "content_type",
                "last_modified",
            },
            optional=frozenset({"source_path"}),
        )
        slug = require_slug(data["slug"], where=f"{where}.slug")
        raw_source_path = data.get("source_path")
        source_path = (
            None
            if raw_source_path is None
            else _require_relative_path(raw_source_path, f"{where}.source_path")
        )
        content_type = require_media_type(data["content_type"], f"{where}.content_type")
        if content_type != "text/html":
            raise SchemaError(f"{where}.content_type must be text/html")
        return cls(
            title=require_text(data["title"], f"{where}.title"),
            section=_require_section(data["section"], f"{where}.section"),
            requested_url=_require_url(
                data["requested_url"], where=f"{where}.requested_url"
            ),
            source_path=source_path,
            slug=slug,
            file=_require_relative_path(
                data["file"],
                f"{where}.file",
                prefix="pages/",
                single_component_after_prefix=True,
            ),
            sha256=_require_sha256(data["sha256"], where=f"{where}.sha256"),
            content_type=content_type,
            last_modified=_optional_timestamp(
                data["last_modified"], f"{where}.last_modified"
            ),
        )


@dataclass(frozen=True, slots=True)
class ImageEntry:
    requested_url: str
    file: str
    sha256: str
    content_type: str

    def to_dict(self) -> dict[str, object]:
        return {
            "requested_url": self.requested_url,
            "file": self.file,
            "sha256": self.sha256,
            "content_type": self.content_type,
        }

    @classmethod
    def from_dict(cls, value: object, *, where: str = "image") -> ImageEntry:
        data = require_object(value, where)
        _check_keys(
            data,
            where=where,
            required={"requested_url", "file", "sha256", "content_type"},
        )
        content_type = require_media_type(data["content_type"], f"{where}.content_type")
        if not content_type.startswith("image/"):
            raise SchemaError(f"{where}.content_type must be an image media type")
        return cls(
            requested_url=_require_url(
                data["requested_url"], where=f"{where}.requested_url"
            ),
            file=_require_relative_path(
                data["file"],
                f"{where}.file",
                prefix="images/",
                single_component_after_prefix=True,
            ),
            sha256=_require_sha256(data["sha256"], where=f"{where}.sha256"),
            content_type=content_type,
        )


def _validate_page_collection(pages: tuple[PageEntry, ...], *, where: str) -> None:
    urls: set[str] = set()
    slugs: set[str] = set()
    files: set[str] = set()
    for page in pages:
        if page.requested_url in urls:
            raise SchemaError(f"{where} has duplicate page URL {page.requested_url}")
        urls.add(page.requested_url)
        folded_slug = page.slug.casefold()
        if folded_slug in slugs:
            raise SchemaError(f"{where} has colliding slug {page.slug!r}")
        slugs.add(folded_slug)
        if page.file in files:
            raise SchemaError(f"{where} has duplicate page file {page.file}")
        files.add(page.file)
        if page.file != f"pages/{page.slug}.html":
            raise SchemaError(f"{where} page file does not match its slug: {page.file}")


def _validate_image_collection(images: tuple[ImageEntry, ...], *, where: str) -> None:
    urls: set[str] = set()
    files: set[str] = set()
    previous_url: str | None = None
    for image in images:
        if image.requested_url in urls:
            raise SchemaError(f"{where} has duplicate image URL {image.requested_url}")
        if previous_url is not None and image.requested_url < previous_url:
            raise SchemaError(f"{where} images are not sorted by requested_url")
        previous_url = image.requested_url
        urls.add(image.requested_url)
        if image.file in files:
            raise SchemaError(f"{where} has duplicate image file {image.file}")
        files.add(image.file)


@dataclass(frozen=True, slots=True)
class Manifest:
    source: str
    discovery: DiscoveryEntry
    pages: tuple[PageEntry, ...]
    images: tuple[ImageEntry, ...]
    schema_version: int = SCHEMA_VERSION

    def to_dict(self, *, include_snapshot: bool = True) -> dict[str, object]:
        result: dict[str, object] = {
            "schema_version": self.schema_version,
            "source": self.source,
            "discovery": self.discovery.to_dict(),
            "pages": [page.to_dict() for page in self.pages],
            "images": [image.to_dict() for image in self.images],
        }
        if include_snapshot:
            result["snapshot_sha256"] = self.snapshot_sha256()
        return result

    def snapshot_sha256(self) -> str:
        return sha256_bytes(canonical_json_bytes(self.to_dict(include_snapshot=False)))

    def to_bytes(self) -> bytes:
        return canonical_document_bytes(self.to_dict())

    @classmethod
    def from_dict(
        cls,
        value: object,
        *,
        expected_source: str | None = None,
        where: str = "manifest",
    ) -> Manifest:
        data = require_object(value, where)
        _check_keys(
            data,
            where=where,
            required={
                "schema_version",
                "source",
                "discovery",
                "pages",
                "images",
                "snapshot_sha256",
            },
        )
        source = require_text(data["source"], f"{where}.source")
        if source not in SOURCE_KEYS:
            raise SchemaError(f"{where}.source is unknown: {source!r}")
        if expected_source is not None and source != expected_source:
            raise SchemaError(
                f"{where}.source is {source!r}, expected {expected_source!r}"
            )
        schema_version = _require_int(data["schema_version"], f"{where}.schema_version")
        if schema_version != SCHEMA_VERSION:
            raise SchemaError(f"{where}.schema_version is unsupported")
        discovery = DiscoveryEntry.from_dict(
            data["discovery"], where=f"{where}.discovery"
        )
        pages = tuple(
            PageEntry.from_dict(item, where=f"{where}.pages[{index}]")
            for index, item in enumerate(
                _require_array(data["pages"], f"{where}.pages")
            )
        )
        images = tuple(
            ImageEntry.from_dict(item, where=f"{where}.images[{index}]")
            for index, item in enumerate(
                _require_array(data["images"], f"{where}.images")
            )
        )
        _validate_page_collection(pages, where=f"{where}.pages")
        _validate_image_collection(images, where=f"{where}.images")
        manifest = cls(
            source=source,
            discovery=discovery,
            pages=pages,
            images=images,
            schema_version=schema_version,
        )
        recorded_snapshot = _require_sha256(
            data["snapshot_sha256"], where=f"{where}.snapshot_sha256"
        )
        if recorded_snapshot != manifest.snapshot_sha256():
            raise SchemaError(f"{where}.snapshot_sha256 does not match the manifest")
        return manifest


@dataclass(frozen=True, slots=True)
class PagePlan:
    source: str
    discovery: DiscoveryEntry
    pages: tuple[PageEntry, ...]
    image_urls: tuple[str, ...]
    schema_version: int = SCHEMA_VERSION

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "source": self.source,
            "discovery": self.discovery.to_dict(),
            "pages": [page.to_dict() for page in self.pages],
            "image_urls": list(self.image_urls),
        }

    def to_bytes(self) -> bytes:
        return canonical_document_bytes(self.to_dict())

    @classmethod
    def from_dict(
        cls,
        value: object,
        *,
        expected_source: str | None = None,
        where: str = "page plan",
    ) -> PagePlan:
        data = require_object(value, where)
        _check_keys(
            data,
            where=where,
            required={"schema_version", "source", "discovery", "pages", "image_urls"},
        )
        source = require_text(data["source"], f"{where}.source")
        if source not in SOURCE_KEYS:
            raise SchemaError(f"{where}.source is unknown: {source!r}")
        if expected_source is not None and source != expected_source:
            raise SchemaError(
                f"{where}.source is {source!r}, expected {expected_source!r}"
            )
        schema_version = _require_int(data["schema_version"], f"{where}.schema_version")
        if schema_version != SCHEMA_VERSION:
            raise SchemaError(f"{where}.schema_version is unsupported")
        discovery = DiscoveryEntry.from_dict(
            data["discovery"], where=f"{where}.discovery"
        )
        pages = tuple(
            PageEntry.from_dict(item, where=f"{where}.pages[{index}]")
            for index, item in enumerate(
                _require_array(data["pages"], f"{where}.pages")
            )
        )
        _validate_page_collection(pages, where=f"{where}.pages")
        raw_urls = _require_array(data["image_urls"], f"{where}.image_urls")
        image_urls = tuple(
            _require_url(item, where=f"{where}.image_urls[{index}]")
            for index, item in enumerate(raw_urls)
        )
        if len(set(image_urls)) != len(image_urls):
            raise SchemaError(f"{where}.image_urls contains duplicates")
        if list(image_urls) != sorted(image_urls):
            raise SchemaError(f"{where}.image_urls is not sorted")
        return cls(
            source=source,
            discovery=discovery,
            pages=pages,
            image_urls=image_urls,
            schema_version=schema_version,
        )
