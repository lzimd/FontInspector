"""HTTP transport. Network I/O lives only in this module."""

from __future__ import annotations

import http.client
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC
from email.message import Message
from email.utils import parsedate_to_datetime
from typing import IO, Protocol

from ..errors import HttpStatusError, HttpTransportError
from ..urls import normalize_url

DEFAULT_TIMEOUT_SECONDS = 30.0
USER_AGENT = "SpecMirror/1.0"


@dataclass(frozen=True, slots=True)
class Redirect:
    status: int
    url: str

    def to_json(self) -> dict[str, object]:
        return {"status": self.status, "url": self.url}


@dataclass(frozen=True, slots=True)
class HttpResponse:
    requested_url: str
    final_url: str
    status: int
    headers: Mapping[str, str]
    body: bytes
    redirects: tuple[Redirect, ...]

    @property
    def content_type(self) -> str | None:
        value = self.headers.get("content-type")
        if value is None:
            return None
        return parse_content_type(value)

    @property
    def last_modified(self) -> str | None:
        return self.headers.get("last-modified")


class HttpClient(Protocol):
    def fetch(self, url: str) -> HttpResponse: ...


class _RecordingRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, redirects: list[Redirect]) -> None:
        super().__init__()
        self._redirects = redirects

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: IO[bytes],
        code: int,
        msg: str,
        headers: http.client.HTTPMessage,
        newurl: str,
    ) -> urllib.request.Request | None:
        resolved = normalize_url(urllib.parse.urljoin(req.full_url, newurl))
        self._redirects.append(Redirect(status=code, url=resolved))
        return super().redirect_request(req, fp, code, msg, headers, resolved)


class UrllibHttpClient:
    def __init__(self, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> None:
        self.timeout = timeout

    def fetch(self, url: str) -> HttpResponse:
        requested_url = normalize_url(url)
        redirects: list[Redirect] = []
        handler = _RecordingRedirectHandler(redirects)
        opener = urllib.request.build_opener(handler)
        request = urllib.request.Request(
            requested_url,
            headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
            method="GET",
        )
        try:
            with opener.open(request, timeout=self.timeout) as response:
                body = response.read()
                status = response.status
                final_url = normalize_url(response.url)
                headers = _lowercase_headers(response.headers)
        except urllib.error.HTTPError as error:
            body = error.read()
            error.close()
            status = error.code
            final_url = normalize_url(error.url)
            headers = _lowercase_headers(error.headers)
            raise HttpStatusError(
                requested_url,
                status,
                f"HTTP {status} for {requested_url}",
                tuple(redirect.url for redirect in redirects),
            ) from error
        except (urllib.error.URLError, http.client.HTTPException, OSError) as error:
            reason = error.reason if isinstance(error, urllib.error.URLError) else error
            raise HttpTransportError(
                requested_url,
                f"request failed for {requested_url}: {reason}",
                tuple(redirect.url for redirect in redirects),
            ) from error

        if not 200 <= status < 300:
            raise HttpStatusError(
                requested_url,
                status,
                f"HTTP {status} for {requested_url}",
                tuple(redirect.url for redirect in redirects),
            )
        if urllib.parse.urlsplit(final_url).scheme not in {"http", "https"}:
            raise HttpStatusError(
                requested_url,
                status,
                f"redirected to unsupported URL: {final_url}",
                tuple(redirect.url for redirect in redirects),
            )
        return HttpResponse(
            requested_url=requested_url,
            final_url=final_url,
            status=status,
            headers=headers,
            body=body,
            redirects=tuple(redirects),
        )


def _lowercase_headers(headers: Message | None) -> dict[str, str]:
    if headers is None:
        return {}
    return {key.lower(): value for key, value in headers.items()}


def parse_content_type(value: str) -> str | None:
    media_type = value.split(";", 1)[0].strip().lower()
    return media_type or None


def parse_http_date(value: str | None) -> str | None:
    """Parse an HTTP date header into a UTC timestamp."""
    if value is None:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
