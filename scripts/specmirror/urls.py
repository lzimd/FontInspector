"""URL normalization, resolution, and lookups without network I/O."""

from __future__ import annotations

import urllib.parse
from collections.abc import Iterable

from .errors import ValidationError


class UrlIndex[T]:
    """A lookup from a normalized URL to a snapshot entry."""

    def __init__(self, entries: Iterable[tuple[str, T]]) -> None:
        self._entries: dict[str, T] = {}
        for url, entry in entries:
            try:
                self._entries[normalize_url(url)] = entry
            except ValidationError:
                continue

    def get(self, url: str) -> T | None:
        """The entry for a URL, or None when the URL is unusable or unknown."""
        try:
            return self._entries.get(normalize_url(url))
        except ValidationError:
            return None


def normalize_url(url: str) -> str:
    try:
        parts = urllib.parse.urlsplit(url)
    except ValueError as error:
        raise ValidationError(f"invalid URL: {url!r}") from error
    scheme = parts.scheme.lower()
    if scheme not in {"http", "https"}:
        raise ValidationError(f"unsupported URL scheme: {url!r}")
    if parts.username is not None or parts.password is not None:
        raise ValidationError(f"URL credentials are not supported: {url!r}")
    try:
        host = parts.hostname
        port = parts.port
    except ValueError as error:
        raise ValidationError(f"invalid URL authority: {url!r}") from error
    if host is None or not host:
        raise ValidationError(f"URL has no host: {url!r}")
    normalized_host = host.lower()
    if ":" in normalized_host:
        normalized_host = f"[{normalized_host}]"
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        port = None
    netloc = normalized_host if port is None else f"{normalized_host}:{port}"
    path = _remove_dot_segments(parts.path)
    if not path:
        path = "/"
    return urllib.parse.urlunsplit((scheme, netloc, path, parts.query, ""))


def resolve_url(base: str, reference: str) -> str:
    return normalize_url(urllib.parse.urljoin(base, reference))


def resolve_link_reference(page_url: str, reference: str) -> str:
    """Resolve a link reference against the page that carries it."""
    value = reference.strip()
    if not value:
        return page_url
    try:
        parts = urllib.parse.urlsplit(value)
    except ValueError as error:
        raise ValidationError(f"invalid link target: {value!r}") from error
    if parts.scheme and parts.scheme.casefold() not in {"http", "https"}:
        return value
    joined = urllib.parse.urljoin(page_url, value)
    try:
        split = urllib.parse.urlsplit(joined)
        base = urllib.parse.urlunsplit(
            (split.scheme, split.netloc, split.path, split.query, "")
        )
        normalized = normalize_url(base)
    except ValueError as error:
        raise ValidationError(f"invalid link target: {value!r}") from error
    fragment = split.fragment
    return f"{normalized}#{fragment}" if fragment else normalized


def url_filename(url: str) -> str:
    return urllib.parse.urlsplit(url).path.rsplit("/", 1)[-1]


def _remove_dot_segments(path: str) -> str:
    remaining = path
    output: list[str] = []
    while remaining:
        if remaining in {".", ".."}:
            remaining = ""
        elif remaining.startswith("../"):
            remaining = remaining[3:]
        elif remaining.startswith("./"):
            remaining = remaining[2:]
        elif remaining.startswith("/./"):
            remaining = "/" + remaining[3:]
        elif remaining == "/.":
            remaining = "/"
        elif remaining.startswith("/../"):
            remaining = "/" + remaining[4:]
            if output:
                output.pop()
        elif remaining == "/..":
            remaining = "/"
            if output:
                output.pop()
        else:
            if remaining.startswith("/"):
                separator = remaining.find("/", 1)
            else:
                separator = remaining.find("/")
            if separator == -1:
                output.append(remaining)
                remaining = ""
            else:
                output.append(remaining[:separator])
                remaining = remaining[separator:]
    return "".join(output)
