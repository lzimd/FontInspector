"""HTTP transport and URL normalization tests."""

from __future__ import annotations

import socket
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest
from specmirror.errors import HttpStatusError, HttpTransportError, ValidationError
from specmirror.fetch.http import UrllibHttpClient
from specmirror.urls import normalize_url, resolve_url, url_filename

LAST_MODIFIED = "Wed, 17 Sep 2026 18:19:04 GMT"


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        """The base class names the handler method this way."""
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/target")
            self.end_headers()
            return
        if self.path == "/missing":
            self.send_response(404)
            self.end_headers()
            return
        body = b"redirected" if self.path == "/target" else b"hello"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Last-Modified", LAST_MODIFIED)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        del format, args


@pytest.fixture
def server() -> Iterator[str]:
    httpd = HTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{httpd.server_port}"
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=5)


def _closed_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def test_client_reads_the_body_and_the_headers(server: str) -> None:
    response = UrllibHttpClient(timeout=5).fetch(f"{server}/page")
    assert response.status == 200
    assert response.body == b"hello"
    assert response.content_type == "text/html"
    assert response.last_modified == LAST_MODIFIED
    assert response.redirects == ()


def test_client_follows_a_redirect_and_records_the_chain(server: str) -> None:
    response = UrllibHttpClient(timeout=5).fetch(f"{server}/redirect")
    assert response.status == 200
    assert response.body == b"redirected"
    assert [redirect.url for redirect in response.redirects] == [f"{server}/target"]
    assert [redirect.status for redirect in response.redirects] == [302]


def test_client_raises_on_a_missing_page(server: str) -> None:
    with pytest.raises(HttpStatusError) as error:
        UrllibHttpClient(timeout=5).fetch(f"{server}/missing")
    assert error.value.status == 404
    assert error.value.url == f"{server}/missing"


def test_client_reports_a_transport_failure() -> None:
    port = _closed_port()
    with pytest.raises(HttpTransportError):
        UrllibHttpClient(timeout=5).fetch(f"http://127.0.0.1:{port}/nothing")


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("https://Example.COM/a", "https://example.com/a"),
        ("https://example.com:443/a", "https://example.com/a"),
        ("http://example.com:80/a", "http://example.com/a"),
        ("https://example.com", "https://example.com/"),
        ("https://example.com/a/../b", "https://example.com/b"),
        ("https://example.com/a/./b", "https://example.com/a/b"),
        ("https://example.com/a#frag", "https://example.com/a"),
    ],
)
def test_normalize_url_canonicalizes(raw: str, expected: str) -> None:
    assert normalize_url(raw) == expected


@pytest.mark.parametrize(
    "raw",
    [
        "ftp://example.com/a",
        "https://user:pass@example.com/",
        "https://",
        "mailto:a@example.com",
        "example.com/a",
    ],
)
def test_normalize_url_rejects_unsupported_urls(raw: str) -> None:
    with pytest.raises(ValidationError):
        normalize_url(raw)


def test_resolve_url_joins_against_the_base() -> None:
    assert (
        resolve_url("https://example.com/docs/a", "b.html")
        == "https://example.com/docs/b.html"
    )
    assert (
        resolve_url("https://example.com/docs/a", "/b.html")
        == "https://example.com/b.html"
    )


def test_url_filename_returns_the_last_path_segment() -> None:
    assert url_filename("https://example.com/docs/a.html") == "a.html"
