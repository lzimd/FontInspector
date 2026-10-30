"""Front-matter extraction per source adapter."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta

from ..dom import DomDocument, h1_text, html_title, meta_content
from ..errors import BuildError
from ..schema import require_text
from ..sources.base import FrontMatterSpec
from ..text import normalize_whitespace

_ISO_TIMESTAMP = re.compile(
    r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    r"(?:[T ](?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})"
    r"(?:\.\d+)?"
    r"(?P<offset>Z|[+-]\d{2}:?\d{2})?)?$"
)
_SLASH_DATE = re.compile(r"^(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{4})$")
_GITCOMMIT = re.compile(
    r"^https://github\.com/(?P<owner>[^/\s]+)/(?P<repo>[^/\s]+)"
    r"/blob/(?P<commit>[0-9a-f]{7,64})/(?P<path>\S+)$"
)


@dataclass(frozen=True, slots=True)
class FrontMatterEntry:
    key: str
    value: str | None
    provenance: str


@dataclass(frozen=True, slots=True)
class FrontMatter:
    fields: tuple[FrontMatterEntry, ...]

    def to_yaml(self) -> str:
        lines = ["---"]
        for field in self.fields:
            if field.value is None:
                if field.key == "last-modified":
                    lines.append(f"{field.key}: null")
                continue
            lines.append(f'{field.key}: "{_yaml_quote(field.value)}"')
        lines.append("---")
        return "\n".join(lines)


def _yaml_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def extract_front_matter(
    document: DomDocument,
    *,
    spec: FrontMatterSpec,
    slug: str,
    last_modified: str | None,
) -> FrontMatter:
    fields: list[FrontMatterEntry] = []
    for key in spec.order:
        if key == "title":
            fields.append(_title_field(document, spec, slug))
        elif key == "last-modified":
            fields.append(
                FrontMatterEntry("last-modified", last_modified, "http:last-modified")
            )
        elif key == "upstream_gitcommit":
            fields.append(_gitcommit_field(document, slug))
        else:
            meta_field = next(
                (
                    item
                    for item in (*spec.text_fields, *spec.timestamp_fields)
                    if item.field == key
                ),
                None,
            )
            if meta_field is None:
                raise BuildError(
                    f"front matter field {key!r} is not defined for {slug}"
                )
            raw = meta_content(document, meta_field.meta_name)
            if raw is None:
                fields.append(FrontMatterEntry(key, None, meta_field.provenance))
                continue
            value = normalize_whitespace(raw)
            if any(item.field == key for item in spec.timestamp_fields):
                value = _normalize_timestamp(value, slug, key)
            fields.append(FrontMatterEntry(key, value or None, meta_field.provenance))
    return FrontMatter(fields=tuple(fields))


def _title_field(
    document: DomDocument, spec: FrontMatterSpec, slug: str
) -> FrontMatterEntry:
    h1 = h1_text(document)
    if h1:
        return FrontMatterEntry("title", h1, "h1")
    og = meta_content(document, spec.title_meta)
    if og:
        return FrontMatterEntry("title", og, f"meta:{spec.title_meta}")
    title = html_title(document)
    if title:
        return FrontMatterEntry("title", title, "title")
    raise BuildError(f"page {slug} has no title for front matter")


def _gitcommit_field(document: DomDocument, slug: str) -> FrontMatterEntry:
    raw = meta_content(document, "gitcommit")
    if raw is None:
        return FrontMatterEntry("upstream_gitcommit", None, "meta:gitcommit")
    value = normalize_whitespace(raw)
    if _GITCOMMIT.fullmatch(value) is None:
        raise BuildError(f"page {slug} has a malformed gitcommit URL: {value!r}")
    return FrontMatterEntry("upstream_gitcommit", value, "meta:gitcommit")


def _normalize_timestamp(value: str, slug: str, key: str) -> str:
    text = require_text(value, f"front matter {key} of {slug}")
    match = _ISO_TIMESTAMP.fullmatch(text)
    if match is not None:
        return _from_iso(match, key, slug)
    match = _SLASH_DATE.fullmatch(text)
    if match is not None:
        return (
            f"{match.group('year')}-{int(match.group('month')):02d}"
            f"-{int(match.group('day')):02d}T00:00:00Z"
        )
    raise BuildError(f"page {slug} has an invalid {key} value: {text!r}")


def _from_iso(match: re.Match[str], key: str, slug: str) -> str:
    year = int(match.group("year"))
    month = int(match.group("month"))
    day = int(match.group("day"))
    hour = int(match.group("hour") or 0)
    minute = int(match.group("minute") or 0)
    second = int(match.group("second") or 0)
    offset_text = match.group("offset")
    offset_minutes = 0
    if offset_text and offset_text != "Z":
        sign = 1 if offset_text[0] == "+" else -1
        digits = offset_text[1:].replace(":", "")
        offset_minutes = sign * (int(digits[:2]) * 60 + int(digits[2:]))
    try:
        moment = datetime(year, month, day, hour, minute, second)
    except ValueError as error:
        raise BuildError(
            f"page {slug} has an invalid {key} value: {match.group(0)!r}"
        ) from error
    moment -= timedelta(minutes=offset_minutes)
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")
