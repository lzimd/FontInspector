from __future__ import annotations

import pytest
from specmirror.errors import ValidationError
from specmirror.fetch.http import parse_content_type, parse_http_date
from specmirror.urls import normalize_url, resolve_url, url_filename


def test_normalize_url_lowercases_and_removes_default_port() -> None:
    assert (
        normalize_url("HTTPS://Learn.Microsoft.com:443/en-us/typography/./toc.json#x")
        == "https://learn.microsoft.com/en-us/typography/toc.json"
    )


def test_normalize_url_preserves_query_and_trailing_slash() -> None:
    assert (
        normalize_url("https://example.com/a/../b/?x=1#frag")
        == "https://example.com/b/?x=1"
    )


def test_normalize_url_removes_dot_segments_but_preserves_double_slash() -> None:
    assert normalize_url("https://example.com/a//b/../c") == "https://example.com/a//c"


def test_normalize_url_rejects_relative_and_non_http_urls() -> None:
    with pytest.raises(ValidationError):
        normalize_url("/relative")
    with pytest.raises(ValidationError):
        normalize_url("mailto:test@example.com")


def test_resolve_url_and_filename() -> None:
    assert (
        resolve_url(
            "https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6.html",
            "Chap6OS2.html#OS2",
        )
        == "https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6OS2.html"
    )
    assert url_filename("https://example.com/a/fig%20one.png?x=1") == "fig%20one.png"


def test_parse_content_type_strips_parameters_and_lowercases() -> None:
    assert parse_content_type("Text/HTML; Charset=UTF-8") == "text/html"
    assert parse_content_type("") is None


def test_parse_http_date_normalizes_to_utc() -> None:
    assert parse_http_date("Thu, 17 Sep 2026 18:19:04 GMT") == "2026-09-17T18:19:04Z"
    assert parse_http_date("Fri, 30 Jan 2026 23:10:21 +0100") == "2026-01-30T22:10:21Z"
    assert parse_http_date("not a date") is None
    assert parse_http_date(None) is None
